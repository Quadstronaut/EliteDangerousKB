"""
tests/test_locking.py — Concurrency and correctness tests for copilot/locking.py.

Coverage:
  T1  record_source no-loss (threads + cross-process)
  T2  same-url interleave preserves first_seen
  T3  _save_index concurrent writers, on-disk set always consistent
  T4  reader-during-write: search never sees mismatched vectors/chunk_ids
  T5  stale-lock reclaim after dead holder (cross-process kill)
  T6  timeout honoured under live contention
  T7  mutual exclusion proven via non-atomic counter
  T8  no litter / no real-repo leakage
  T10 portability + stdlib-only static checks

All tests use tmp_path and monkeypatch of copilot.paths.* / seen_path.
None are marked integration — they run in the default gate.
Windows multiprocessing NOTE: spawn mode requires module-level worker functions
(importable by name); closures/lambdas are never used as worker targets.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import textwrap
import threading
import time
from pathlib import Path
import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _fake_embed(texts: list[str]) -> np.ndarray:
    """Deterministic fake embeddings — mirrors test_index.py."""
    vecs = []
    for t in texts:
        seed = int(hashlib.sha256(t.encode()).hexdigest()[:8], 16) % (2**31)
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(1024).astype(np.float32)
        v /= np.linalg.norm(v)
        vecs.append(v)
    return np.array(vecs, dtype=np.float32)


def _make_md(title: str, heading: str, body: str) -> str:
    import textwrap as _tw
    return _tw.dedent(f"""\
        ---
        source_url: https://example.com
        source_tier: 2
        source_count: 1
        verified: true
        availability: live
        ---
        # {title}

        ## {heading}

        {body}
    """)


# ---------------------------------------------------------------------------
# Module-level worker functions for Windows spawn picklability
# ---------------------------------------------------------------------------

def _worker_record_source(args):
    """Worker: call record_source for one URL; return error string or None."""
    url, content_hash, seen_path_str = args
    try:
        from copilot.loop_state import record_source
        record_source(url, content_hash, seen_path_str)
        return None
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


def _worker_save_index(args):
    """Worker: call _save_index with a fake (N, 1024) vector set."""
    emb_dir_str, idx_dir_str, chunk_ids = args
    try:
        import copilot.paths as _paths
        from copilot.index import _save_index

        # Monkeypatch is in-process only; for subprocess-style workers we
        # patch via module attributes directly (safe because each worker is
        # a fresh spawn with its own memory space).
        _paths.embeddings_dir = lambda: Path(emb_dir_str)
        _paths.indexes_dir = lambda: Path(idx_dir_str)

        vecs = _fake_embed(chunk_ids)
        manifest = {cid: {"content_hash": "h", "kb_path": "k", "heading_path": "h",
                           "payload": {}} for cid in chunk_ids}
        _save_index(chunk_ids, vecs, manifest)
        return None
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


# ---------------------------------------------------------------------------
# T1: record_source no-loss (threads)
# ---------------------------------------------------------------------------

class TestT1ThreadedNoLoss:
    """T1 (threads): 60 threads, each distinct URL -> exactly 60 entries."""

    def test_no_loss_threads(self, tmp_path, monkeypatch):
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        seen_str = str(seen)

        import copilot.loop_state as _ls
        # No monkeypatch needed for seen_path — it is caller-supplied.

        N = 60
        errors = []
        lock = threading.Lock()

        def worker(i: int) -> None:
            url = f"https://example.com/page/{i}"
            try:
                from copilot.loop_state import record_source
                record_source(url, f"hash{i}", seen_str)
            except Exception as exc:
                with lock:
                    errors.append(f"Thread {i}: {exc}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)

        assert not errors, f"Worker errors:\n" + "\n".join(errors)
        data = json.loads(seen.read_text(encoding="utf-8"))
        assert len(data) == N, f"Expected {N} entries, got {len(data)}"


# ---------------------------------------------------------------------------
# T1 cross-process: real subprocess workers
# ---------------------------------------------------------------------------

class TestT1CrossProcess:
    """T1 (cross-process): 12 subprocesses each record a distinct URL."""

    def test_no_loss_cross_process(self, tmp_path):
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        seen_str = str(seen)

        N = 12
        # Build a small worker script that imports and calls record_source.
        # We write it to tmp_path so there are no absolute-path literals in
        # tracked files.
        repo_root = Path(__file__).resolve().parent.parent
        # Worker script injects repo_root into sys.path so 'copilot' is importable
        # regardless of where the script file lives (tmp_path != repo_root).
        worker_script = tmp_path / "_worker_rs.py"
        worker_script.write_text(
            textwrap.dedent(f"""\
                import sys
                sys.path.insert(0, {str(repo_root)!r})
                from copilot.loop_state import record_source
                idx = int(sys.argv[1])
                seen_path = sys.argv[2]
                record_source(f"https://example.com/xp/{{idx}}", f"hash{{idx}}", seen_path)
            """),
            encoding="utf-8",
        )

        procs = []
        for i in range(N):
            p = subprocess.Popen(
                [sys.executable, str(worker_script), str(i), seen_str],
            )
            procs.append(p)

        failed = []
        for i, p in enumerate(procs):
            rc = p.wait(timeout=60)
            if rc != 0:
                failed.append(f"proc {i} exited with rc={rc}")

        assert not failed, "Subprocess failures:\n" + "\n".join(failed)
        data = json.loads(seen.read_text(encoding="utf-8"))
        assert len(data) == N, f"Expected {N} entries, got {len(data)}"


# ---------------------------------------------------------------------------
# T2: same-url interleave preserves first_seen
# ---------------------------------------------------------------------------

class TestT2SameUrl:
    def test_same_url_one_entry_first_seen_stable(self, tmp_path):
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        seen_str = str(seen)

        url = "https://example.com/same"
        N = 30

        errors = []
        lock = threading.Lock()

        def worker(i: int) -> None:
            try:
                from copilot.loop_state import record_source
                record_source(url, f"hash{i}", seen_str)
            except Exception as exc:
                with lock:
                    errors.append(str(exc))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)

        assert not errors

        data = json.loads(seen.read_text(encoding="utf-8"))
        assert len(data) == 1, f"Same URL must collapse to 1 key, got {len(data)}"

        key = hashlib.sha256(url.encode()).hexdigest()
        entry = data[key]
        assert "first_seen" in entry
        assert "content_sha256" in entry
        # content_sha256 must be one of the written values
        assert any(entry["content_sha256"] == f"hash{i}" for i in range(N))


# ---------------------------------------------------------------------------
# T3: _save_index concurrent writers — on-disk set always consistent
# ---------------------------------------------------------------------------

class TestT3SaveIndexConcurrency:
    def test_save_index_concurrent_writers(self, tmp_path, monkeypatch):
        import copilot.paths as _paths
        emb_dir = tmp_path / "embeddings"
        idx_dir = tmp_path / "indexes"
        emb_dir.mkdir()
        idx_dir.mkdir()
        monkeypatch.setattr(_paths, "embeddings_dir", lambda: emb_dir)
        monkeypatch.setattr(_paths, "indexes_dir", lambda: idx_dir)

        from copilot.index import _save_index

        N = 20
        errors = []
        lock = threading.Lock()

        def writer(i: int) -> None:
            chunk_ids = [f"chunk_{i}_{j}" for j in range(5)]
            vecs = _fake_embed(chunk_ids)
            manifest = {cid: {"content_hash": "h", "kb_path": "k",
                               "heading_path": "h", "payload": {}}
                        for cid in chunk_ids}
            try:
                # _save_index does NOT call ollama_client.embed — it just
                # writes pre-computed vectors.  No patch needed here.
                _save_index(chunk_ids, vecs, manifest)
            except Exception as exc:
                with lock:
                    errors.append(f"writer {i}: {exc}")

        threads = [threading.Thread(target=writer, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)

        assert not errors, "Writer errors:\n" + "\n".join(errors)

        # Read final state and verify consistency.
        vecs_path = emb_dir / "vectors.npy"
        ids_path = emb_dir / "chunk_ids.json"
        mfst_path = idx_dir / "manifest.json"

        assert vecs_path.exists()
        assert ids_path.exists()
        assert mfst_path.exists()

        vectors = np.load(str(vecs_path))
        chunk_ids = json.loads(ids_path.read_text(encoding="utf-8"))
        manifest = json.loads(mfst_path.read_text(encoding="utf-8"))

        assert vectors.shape[0] == len(chunk_ids), (
            f"vectors {vectors.shape[0]} != chunk_ids {len(chunk_ids)}"
        )
        assert set(chunk_ids) == set(manifest.keys()), (
            f"chunk_ids set != manifest keys"
        )


# ---------------------------------------------------------------------------
# T4: reader-during-write — search never trips the length-mismatch guard
# ---------------------------------------------------------------------------

class TestT4ReaderDuringWrite:
    def test_reader_never_sees_skew(self, tmp_path, monkeypatch, capsys):
        import copilot.paths as _paths
        emb_dir = tmp_path / "embeddings"
        idx_dir = tmp_path / "indexes"
        emb_dir.mkdir()
        idx_dir.mkdir()
        monkeypatch.setattr(_paths, "embeddings_dir", lambda: emb_dir)
        monkeypatch.setattr(_paths, "indexes_dir", lambda: idx_dir)

        from copilot.index import _save_index, search

        # Write a valid initial index.
        init_ids = [f"init_{j}" for j in range(8)]
        init_vecs = _fake_embed(init_ids)
        init_manifest = {cid: {"content_hash": "h", "kb_path": "k",
                                "heading_path": "h", "payload": {}}
                         for cid in init_ids}
        _save_index(init_ids, init_vecs, init_manifest)

        stop = threading.Event()
        guard_trips = []
        search_errors = []
        write_errors = []

        def long_writer() -> None:
            for i in range(15):
                if stop.is_set():
                    break
                n = (i % 8) + 2
                chunk_ids = [f"w_{i}_{j}" for j in range(n)]
                vecs = _fake_embed(chunk_ids)
                manifest = {cid: {"content_hash": "h", "kb_path": "k",
                                   "heading_path": "h", "payload": {}}
                            for cid in chunk_ids}
                try:
                    _save_index(chunk_ids, vecs, manifest)
                except Exception as exc:
                    write_errors.append(str(exc))
                time.sleep(0.02)

        def reader() -> None:
            query = _fake_embed(["query"])[0]
            while not stop.is_set():
                try:
                    search(query, top_k=3)
                except Exception as exc:
                    search_errors.append(str(exc))
                time.sleep(0.005)

        writer_t = threading.Thread(target=long_writer)
        readers = [threading.Thread(target=reader) for _ in range(3)]

        writer_t.start()
        for r in readers:
            r.start()

        writer_t.join(timeout=30)
        stop.set()
        for r in readers:
            r.join(timeout=5)

        assert not write_errors, "Write errors: " + str(write_errors)
        assert not search_errors, "Search errors: " + str(search_errors)

        # The length-mismatch guard emits a specific WARNING — check it never fired.
        stderr = capsys.readouterr().err
        assert "length mismatch" not in stderr, (
            "Length-mismatch guard was tripped by a concurrent write — "
            "the locking is not protecting readers correctly."
        )


# ---------------------------------------------------------------------------
# T5: stale-lock reclaim after dead holder (cross-process kill)
# ---------------------------------------------------------------------------

class TestT5StaleReclaim:
    def test_reclaim_dead_pid_lockfile(self, tmp_path):
        """Write a lockfile stamped with a guaranteed-dead PID, verify reclaim."""
        from copilot.locking import file_lock, LockTimeout

        lock_path = tmp_path / "test_stale.lock"
        dead_pid = 9999999  # Almost certainly not a live PID.
        # Stamp the lockfile as if a process with dead_pid created it.
        lock_path.write_text(f"{dead_pid}:{time.time() - 120}\n", encoding="ascii")

        # A fresh file_lock should reclaim the dead-PID token and acquire.
        acquired = False
        with file_lock(str(lock_path), timeout=5.0, stale_after=60.0):
            acquired = True
        assert acquired, "Should have reclaimed dead-PID lock"

    def test_reclaim_killed_subprocess(self, tmp_path):
        """
        Real cross-process kill: a child acquires the lock, parent kills it,
        then a fresh file_lock must acquire within a bounded time.
        """
        from copilot.locking import file_lock, LockTimeout

        lock_path = tmp_path / "kill_test.lock"
        ready_flag = tmp_path / "ready.flag"

        # Child script: acquire file_lock, write ready flag, sleep a long time.
        child_script = tmp_path / "_child_lock.py"
        child_script.write_text(
            textwrap.dedent(f"""\
                import sys, time
                sys.path.insert(0, {str(Path(__file__).resolve().parent.parent)!r})
                from copilot.locking import file_lock
                with file_lock({str(lock_path)!r}, timeout=10.0):
                    open({str(ready_flag)!r}, 'w').close()
                    time.sleep(120)  # hold the lock until killed
            """),
            encoding="utf-8",
        )

        proc = subprocess.Popen([sys.executable, str(child_script)])

        # Wait for child to signal it holds the lock.
        deadline = time.monotonic() + 10
        while not ready_flag.exists():
            if time.monotonic() > deadline:
                proc.kill()
                pytest.fail("Child never signalled lock acquisition")
            time.sleep(0.05)

        # Kill the child while it holds the lock.
        proc.kill()
        proc.wait()

        # The lock token is now owned by a dead PID.
        # A fresh file_lock must reclaim it within stale_after (we use a short
        # stale_after so the test is fast even if PID-probe has jitter).
        t0 = time.monotonic()
        acquired = False
        with file_lock(str(lock_path), timeout=15.0, stale_after=5.0):
            acquired = True
        elapsed = time.monotonic() - t0

        assert acquired, "Should have reclaimed killed-subprocess lock"
        assert elapsed < 15.0, f"Reclaim took too long: {elapsed:.2f}s"

    def test_live_pid_not_stolen(self, tmp_path):
        """A lock held by a LIVE process must not be stolen."""
        from copilot.locking import file_lock, LockTimeout

        lock_path = tmp_path / "live_test.lock"
        acquired = threading.Event()
        released = threading.Event()

        def holder():
            with file_lock(str(lock_path), timeout=10.0):
                acquired.set()
                released.wait(timeout=5)

        t = threading.Thread(target=holder)
        t.start()
        acquired.wait(timeout=5)

        # Another thread with a short timeout must raise LockTimeout.
        with pytest.raises(LockTimeout):
            with file_lock(str(lock_path), timeout=0.3, stale_after=60.0):
                pass

        released.set()
        t.join(timeout=5)


# ---------------------------------------------------------------------------
# T6: timeout honoured under live contention
# ---------------------------------------------------------------------------

class TestT6Timeout:
    def test_timeout_raises_lock_timeout(self, tmp_path):
        from copilot.locking import file_lock, LockTimeout

        lock_path = tmp_path / "timeout_test.lock"
        holder_ready = threading.Event()
        release_holder = threading.Event()

        def holder():
            with file_lock(str(lock_path), timeout=10.0):
                holder_ready.set()
                release_holder.wait(timeout=10)

        t = threading.Thread(target=holder)
        t.start()
        holder_ready.wait(timeout=5)

        t0 = time.monotonic()
        with pytest.raises(LockTimeout):
            with file_lock(str(lock_path), timeout=0.5, stale_after=60.0):
                pass
        elapsed = time.monotonic() - t0

        release_holder.set()
        t.join(timeout=5)

        # Must raise within ~timeout + generous slack (not hang).
        assert elapsed < 3.0, f"LockTimeout raised too late: {elapsed:.2f}s"
        assert elapsed >= 0.4, f"LockTimeout raised too early: {elapsed:.2f}s"

    def test_zero_timeout_raises_immediately(self, tmp_path):
        from copilot.locking import file_lock, LockTimeout

        lock_path = tmp_path / "zero_timeout.lock"
        t0 = time.monotonic()
        with pytest.raises(LockTimeout):
            with file_lock(str(lock_path), timeout=0.0):
                pass
        elapsed = time.monotonic() - t0
        assert elapsed < 0.5, f"Zero-timeout should raise immediately, took {elapsed:.2f}s"

    def test_negative_timeout_raises_immediately(self, tmp_path):
        from copilot.locking import file_lock, LockTimeout

        lock_path = tmp_path / "neg_timeout.lock"
        t0 = time.monotonic()
        with pytest.raises(LockTimeout):
            with file_lock(str(lock_path), timeout=-1.0):
                pass
        elapsed = time.monotonic() - t0
        assert elapsed < 0.5, f"Negative timeout should raise immediately, took {elapsed:.2f}s"


# ---------------------------------------------------------------------------
# T7: mutual exclusion proven via non-atomic counter
# ---------------------------------------------------------------------------

class TestT7MutualExclusion:
    def test_non_atomic_counter_under_file_lock(self, tmp_path):
        """
        N threads each do read-sleep-write on a plain (non-atomic) counter file
        under file_lock.  Without the lock, concurrent reads would produce lost
        updates (final < N).  With the lock, final == N.
        """
        from copilot.locking import file_lock

        lock_path = tmp_path / "counter.lock"
        counter_path = tmp_path / "counter.txt"
        counter_path.write_text("0", encoding="utf-8")

        N = 40
        errors = []
        err_lock = threading.Lock()

        def increment() -> None:
            try:
                with file_lock(str(lock_path), timeout=30.0):
                    val = int(counter_path.read_text(encoding="utf-8"))
                    time.sleep(0.002)  # force interleaving without the lock
                    counter_path.write_text(str(val + 1), encoding="utf-8")
            except Exception as exc:
                with err_lock:
                    errors.append(str(exc))

        threads = [threading.Thread(target=increment) for _ in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)

        assert not errors, "Errors: " + str(errors)
        final = int(counter_path.read_text(encoding="utf-8"))
        assert final == N, (
            f"Counter is {final}, expected {N} — mutual exclusion failed "
            "(lost updates imply two threads held the lock simultaneously)"
        )


# ---------------------------------------------------------------------------
# T8: no litter / no real-repo leakage
# ---------------------------------------------------------------------------

class TestT8NoLitter:
    def test_no_lock_litter_after_clean_run(self, tmp_path, monkeypatch):
        import copilot.paths as _paths
        emb_dir = tmp_path / "embeddings"
        idx_dir = tmp_path / "indexes"
        emb_dir.mkdir()
        idx_dir.mkdir()
        monkeypatch.setattr(_paths, "embeddings_dir", lambda: emb_dir)
        monkeypatch.setattr(_paths, "indexes_dir", lambda: idx_dir)

        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")

        from copilot.loop_state import record_source
        from copilot.index import _save_index

        # Run some operations.
        for i in range(5):
            record_source(f"https://example.com/{i}", f"h{i}", str(seen))

        chunk_ids = ["a", "b", "c"]
        vecs = _fake_embed(chunk_ids)
        manifest = {cid: {"content_hash": "h", "kb_path": "k",
                           "heading_path": "h", "payload": {}}
                    for cid in chunk_ids}
        _save_index(chunk_ids, vecs, manifest)

        # Lock files PERSIST by design: the OS byte-range lock (msvcrt/fcntl) lives
        # on the open handle of a stable lock-file inode that all contenders must
        # share, so we never delete it. They are empty/inert and gitignored. We DO
        # require that no .tmp write-staging litter remains.
        tmp_files = list(tmp_path.rglob("*.tmp")) + list(tmp_path.rglob("*.tmp.npy"))
        assert not tmp_files, f"Tmp litter found: {tmp_files}"

    def test_real_repo_untouched(self, tmp_path, monkeypatch):
        """The test's monkeypatched operations must not write into the real repo.

        NOTE: the byte-range index.lock is persistent-by-design — created on first
        lock acquisition by any real eval/build CLI run, never deleted, gitignored.
        It may already exist in the real repo. We snapshot its presence and assert
        only that THIS test did not CREATE it, rather than asserting the ambient
        repo lacks one (which would make the test fail after any legitimate CLI run
        such as `python -m copilot.eval`).
        """
        import copilot.paths as _paths
        from copilot.paths import repo_root

        real_indexes = repo_root() / "indexes"
        real_emb = repo_root() / "embeddings"
        # Snapshot a pre-existing CLI-created lock so it is not blamed on this test.
        lock_existed_before = (real_indexes / "index.lock").exists()

        emb_dir = tmp_path / "embeddings"
        idx_dir = tmp_path / "indexes"
        emb_dir.mkdir()
        idx_dir.mkdir()
        monkeypatch.setattr(_paths, "embeddings_dir", lambda: emb_dir)
        monkeypatch.setattr(_paths, "indexes_dir", lambda: idx_dir)

        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")

        from copilot.loop_state import record_source
        record_source("https://example.com/test", "hash", str(seen))

        # THIS test must not have CREATED index.lock in the real repo (a lock that
        # pre-existed from a real CLI run is exempt — not this test's doing).
        if real_indexes.exists() and not lock_existed_before:
            assert not (real_indexes / "index.lock").exists(), (
                "index.lock was written to the real repo indexes/ dir by this test"
            )
        if real_emb.exists():
            assert not (real_emb / "vectors.lock").exists()

        # seen.json in the real repo must not exist (we wrote to tmp_path).
        assert not (real_indexes / "seen.json").exists() or \
               not (real_indexes / "seen.json.lock").exists(), \
               "seen.json.lock appeared in real repo indexes/"


# ---------------------------------------------------------------------------
# T10: portability + stdlib-only static checks
# ---------------------------------------------------------------------------

class TestT10Portability:
    def test_no_absolute_path_in_locking_py(self):
        """copilot/locking.py must contain no absolute-path literals."""
        from copilot.paths import repo_root
        locking_path = repo_root() / "copilot" / "locking.py"
        text = locking_path.read_text(encoding="utf-8")
        abs_pat = re.compile(r"[A-Za-z]:\\|/home/|/Users/")
        offenders = [
            f"line {i+1}: {line.rstrip()}"
            for i, line in enumerate(text.splitlines())
            if abs_pat.search(line)
        ]
        assert not offenders, (
            "Absolute-path literals in copilot/locking.py:\n" + "\n".join(offenders)
        )

    def test_locking_imports_stdlib_only(self):
        """copilot/locking.py must import only stdlib modules (no pip deps)."""
        import sys as _sys
        from copilot.paths import repo_root
        locking_path = repo_root() / "copilot" / "locking.py"
        tree = ast.parse(locking_path.read_text(encoding="utf-8"))

        stdlib_allowlist = {
            # standard lib modules used/potentially used in locking.py
            "contextlib", "errno", "os", "pathlib", "threading", "time",
            "typing", "ctypes", "__future__", "abc", "collections",
            "functools", "weakref", "warnings",
            "msvcrt", "fcntl",  # platform-specific stdlib byte-range lock primitives
        }

        third_party = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top not in stdlib_allowlist:
                        third_party.append(top)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    if top not in stdlib_allowlist:
                        third_party.append(top)

        assert not third_party, (
            f"Non-stdlib imports in copilot/locking.py: {third_party}"
        )

    def test_lock_timeout_is_lock_error_subclass(self):
        """LockTimeout must be a subclass of LockError and Exception."""
        from copilot.locking import LockError, LockTimeout
        assert issubclass(LockTimeout, LockError)
        assert issubclass(LockError, Exception)

    def test_same_thread_reentry_no_deadlock(self, tmp_path):
        """Same thread can re-enter file_lock without deadlocking."""
        from copilot.locking import file_lock
        lock_path = tmp_path / "reentry.lock"
        # The outer context manager acquires; the inner one should re-enter
        # (refcount bump) without trying to re-acquire the disk token.
        result = []
        with file_lock(str(lock_path), timeout=5.0):
            with file_lock(str(lock_path), timeout=5.0):
                result.append("inner")
        assert result == ["inner"], "Reentrant file_lock failed"
