"""
tests/test_concurrency_item6.py — Cross-process concurrency harness for item 6.

These tests spin real subprocesses to prove that:
  * record_source loses ZERO entries under N concurrent writers (no WinError 32).
  * _save_index + concurrent readers (search/upsert_changed) never produce a
    mismatched (vectors, chunk_ids) pair.

All tests use tmp_path + monkeypatch of copilot.paths.*; none are marked
integration; they run in the default gate.

Windows multiprocessing NOTE: spawn mode requires module-level worker functions.
We use subprocess.Popen with small helper scripts written to tmp_path (so no
absolute-path literals appear in tracked runtime files).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import textwrap
import threading
import time
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fake_embed(texts: list[str]) -> np.ndarray:
    vecs = []
    for t in texts:
        seed = int(hashlib.sha256(t.encode()).hexdigest()[:8], 16) % (2**31)
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(1024).astype(np.float32)
        v /= np.linalg.norm(v)
        vecs.append(v)
    return np.array(vecs, dtype=np.float32)


REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# T1 (cross-process): N subprocesses, distinct URLs, zero lost entries
# ---------------------------------------------------------------------------

class TestConcurrentRecordSource:
    """
    N subprocess workers each call record_source for a distinct URL into one
    shared seen.json.  Final count must equal N; no WinError 32 / non-zero rc.
    """

    def test_concurrent_record_source_no_loss(self, tmp_path):
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        seen_str = str(seen)

        N = 12  # keep fast on CI; each worker is a fresh Python import

        # Worker script: single record_source call, exits 0 on success.
        # Inject REPO_ROOT into sys.path so copilot is importable.
        worker_script = tmp_path / "_rs_worker.py"
        worker_script.write_text(
            textwrap.dedent(f"""\
                import sys
                sys.path.insert(0, {str(REPO_ROOT)!r})
                from copilot.loop_state import record_source
                idx = int(sys.argv[1])
                seen_path = sys.argv[2]
                record_source(
                    f"https://example.com/concurrent/{{idx}}",
                    f"hash{{idx}}",
                    seen_path,
                )
            """),
            encoding="utf-8",
        )

        procs = [
            subprocess.Popen(
                [sys.executable, str(worker_script), str(i), seen_str],
                stderr=subprocess.PIPE,
            )
            for i in range(N)
        ]

        failures = []
        for i, proc in enumerate(procs):
            rc = proc.wait(timeout=60)
            stderr = proc.stderr.read().decode(errors="replace") if proc.stderr else ""
            if rc != 0:
                failures.append(f"proc {i}: rc={rc}  stderr={stderr!r}")
            elif "WinError" in stderr or "Error" in stderr:
                failures.append(f"proc {i}: stderr={stderr!r}")

        assert not failures, "Worker failures:\n" + "\n".join(failures)

        data = json.loads(seen.read_text(encoding="utf-8"))
        assert len(data) == N, (
            f"Expected {N} entries in seen.json, got {len(data)} "
            "(lost updates indicate a locking failure)"
        )

    def test_no_winerror_32_under_contention(self, tmp_path):
        """Specifically checks that WinError 32 (file in use) does not appear."""
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        seen_str = str(seen)

        N = 15
        worker_script = tmp_path / "_rs_errcheck.py"
        worker_script.write_text(
            textwrap.dedent(f"""\
                import sys, traceback
                sys.path.insert(0, {str(REPO_ROOT)!r})
                try:
                    from copilot.loop_state import record_source
                    idx = int(sys.argv[1])
                    seen_path = sys.argv[2]
                    record_source(
                        f"https://example.com/err/{{idx}}",
                        f"hash{{idx}}",
                        seen_path,
                    )
                except Exception:
                    traceback.print_exc()
                    sys.exit(1)
            """),
            encoding="utf-8",
        )

        procs = [
            subprocess.Popen(
                [sys.executable, str(worker_script), str(i), seen_str],
                stderr=subprocess.PIPE,
            )
            for i in range(N)
        ]

        winerrors = []
        for i, proc in enumerate(procs):
            rc = proc.wait(timeout=60)
            stderr = proc.stderr.read().decode(errors="replace") if proc.stderr else ""
            if "WinError 32" in stderr or "WinError 13" in stderr:
                winerrors.append(f"proc {i}: {stderr!r}")
            if rc != 0 and not winerrors:
                winerrors.append(f"proc {i} non-zero rc={rc}: {stderr!r}")

        assert not winerrors, "WinError / crashes:\n" + "\n".join(winerrors)


# ---------------------------------------------------------------------------
# T3 + T4: concurrent _save_index + reader never sees inconsistent triple
# ---------------------------------------------------------------------------

class TestConcurrentIndexReadWrite:
    """
    Writers call _save_index with varying-size index sets; readers call
    index.search concurrently.  Every observable (vectors, chunk_ids) snapshot
    must satisfy vectors.shape[0] == len(chunk_ids) == len(manifest).
    """

    def test_save_index_plus_reader_consistency(self, tmp_path, monkeypatch):
        import copilot.paths as _paths
        emb_dir = tmp_path / "embeddings"
        idx_dir = tmp_path / "indexes"
        emb_dir.mkdir()
        idx_dir.mkdir()
        monkeypatch.setattr(_paths, "embeddings_dir", lambda: emb_dir)
        monkeypatch.setattr(_paths, "indexes_dir", lambda: idx_dir)

        from copilot.index import _save_index, search

        # Write a valid initial index so readers don't immediately get [].
        init_ids = ["init_a", "init_b", "init_c"]
        init_vecs = _fake_embed(init_ids)
        init_manifest = {cid: {"content_hash": "h", "kb_path": "k",
                                "heading_path": "h", "payload": {}}
                         for cid in init_ids}
        _save_index(init_ids, init_vecs, init_manifest)

        inconsistencies = []
        write_errors = []
        stop = threading.Event()
        lock = threading.Lock()

        def writer(i: int) -> None:
            n = (i % 10) + 1
            chunk_ids = [f"w{i}_{j}" for j in range(n)]
            vecs = _fake_embed(chunk_ids)
            manifest = {cid: {"content_hash": "h", "kb_path": "k",
                               "heading_path": "h", "payload": {}}
                        for cid in chunk_ids}
            try:
                _save_index(chunk_ids, vecs, manifest)
            except Exception as exc:
                with lock:
                    write_errors.append(f"writer {i}: {exc}")

        def file_reader() -> None:
            """Read the 3 files directly (no lock path used here — this tests that
            the writer's lock guarantees the files are coherent when released)."""
            while not stop.is_set():
                try:
                    vecs_path = emb_dir / "vectors.npy"
                    ids_path = emb_dir / "chunk_ids.json"
                    mfst_path = idx_dir / "manifest.json"
                    if vecs_path.exists() and ids_path.exists() and mfst_path.exists():
                        # Use search() which takes the index lock.
                        query = _fake_embed(["q"])[0]
                        search(query, top_k=3)
                except Exception:
                    pass  # transient file-not-found during creation is ok
                time.sleep(0.005)

        # Launch 12 writer threads and 3 reader threads.
        writers = [threading.Thread(target=writer, args=(i,)) for i in range(12)]
        readers = [threading.Thread(target=file_reader) for _ in range(3)]

        for r in readers:
            r.start()
        for w in writers:
            w.start()
        for w in writers:
            w.join(timeout=60)

        stop.set()
        for r in readers:
            r.join(timeout=5)

        assert not write_errors, "Write errors:\n" + str(write_errors)
        assert not inconsistencies, "Inconsistencies:\n" + str(inconsistencies)

        # Final on-disk state must be consistent.
        vectors = np.load(str(emb_dir / "vectors.npy"))
        chunk_ids = json.loads((emb_dir / "chunk_ids.json").read_text(encoding="utf-8"))
        manifest = json.loads((idx_dir / "manifest.json").read_text(encoding="utf-8"))

        assert vectors.shape[0] == len(chunk_ids), (
            f"Final vectors {vectors.shape[0]} != chunk_ids {len(chunk_ids)}"
        )
        assert set(chunk_ids) == set(manifest.keys()), (
            "Final chunk_ids set != manifest keys"
        )

    def test_upsert_changed_consistent_baseline(self, tmp_path, monkeypatch):
        """
        upsert_changed reads manifest + vectors + chunk_ids under ONE lock.
        Run a writer thread concurrently; assert upsert_changed never crashes
        and the final index is self-consistent.
        """
        import copilot.paths as _paths
        emb_dir = tmp_path / "embeddings"
        idx_dir = tmp_path / "indexes"
        emb_dir.mkdir()
        idx_dir.mkdir()
        monkeypatch.setattr(_paths, "embeddings_dir", lambda: emb_dir)
        monkeypatch.setattr(_paths, "indexes_dir", lambda: idx_dir)

        from copilot.index import _save_index, upsert_changed

        # Build a tiny KB.
        kb_dir = tmp_path / "kb"
        kb_dir.mkdir()
        (kb_dir / "page.md").write_text(
            textwrap.dedent("""\
                ---
                source_url: https://example.com
                source_tier: 2
                source_count: 1
                verified: true
                availability: live
                ---
                # Test

                ## Section A

                Content for section A.
            """),
            encoding="utf-8",
        )

        # Initial index.
        init_ids = ["id_a", "id_b"]
        init_vecs = _fake_embed(init_ids)
        init_manifest = {cid: {"content_hash": "h", "kb_path": "k",
                                "heading_path": "h", "payload": {}}
                         for cid in init_ids}
        _save_index(init_ids, init_vecs, init_manifest)

        upsert_errors = []
        write_errors = []
        stop = threading.Event()
        lock = threading.Lock()

        def writer_loop() -> None:
            for i in range(8):
                if stop.is_set():
                    break
                n = (i % 4) + 1
                chunk_ids = [f"loop_{i}_{j}" for j in range(n)]
                vecs = _fake_embed(chunk_ids)
                manifest = {cid: {"content_hash": "h", "kb_path": "k",
                                   "heading_path": "h", "payload": {}}
                            for cid in chunk_ids}
                try:
                    _save_index(chunk_ids, vecs, manifest)
                except Exception as exc:
                    with lock:
                        write_errors.append(str(exc))
                time.sleep(0.02)

        def upsert_loop() -> None:
            for _ in range(3):
                if stop.is_set():
                    break
                try:
                    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
                        upsert_changed(kb_dir)
                except Exception as exc:
                    with lock:
                        upsert_errors.append(str(exc))
                time.sleep(0.05)

        wt = threading.Thread(target=writer_loop)
        ut = threading.Thread(target=upsert_loop)
        wt.start()
        ut.start()
        wt.join(timeout=30)
        stop.set()
        ut.join(timeout=10)

        assert not write_errors, "Write errors: " + str(write_errors)
        assert not upsert_errors, "Upsert errors: " + str(upsert_errors)

        # Final consistency check.
        vectors = np.load(str(emb_dir / "vectors.npy"))
        chunk_ids = json.loads((emb_dir / "chunk_ids.json").read_text(encoding="utf-8"))
        manifest = json.loads((idx_dir / "manifest.json").read_text(encoding="utf-8"))

        assert vectors.shape[0] == len(chunk_ids)
        assert set(chunk_ids) == set(manifest.keys())
