"""
KB vector index: full rebuild, incremental upsert, cosine search.

Artifacts (all written atomically via write_json_atomic / numpy save):
  embeddings/vectors.npy      — (N, 1024) float32, L2-normalised, row-order = chunk_ids.json
  embeddings/chunk_ids.json   — [chunk_id, ...]  (row index → id)
  indexes/manifest.json       — {chunk_id: {content_hash, kb_path, heading_path, payload}}

content_hash = sha256 of the raw markdown section text for the chunk.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from pathlib import Path

import numpy as np

from copilot import ollama_client
from copilot import paths
from copilot.atomic import write_json_atomic
from copilot.chunker import chunk_page
from copilot.models import Chunk


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _chunk_payload(chunk: Chunk) -> dict:
    """Chunk fields serialisable to manifest payload — minus text and score."""
    d = dataclasses.asdict(chunk)
    d.pop("text", None)
    d.pop("score", None)
    return d


def _save_index(
    chunk_ids: list[str],
    vectors: np.ndarray,
    manifest: dict,
) -> None:
    # Reference via the paths module so test monkeypatching takes effect.
    emb = paths.embeddings_dir()
    emb.mkdir(parents=True, exist_ok=True)
    idx = paths.indexes_dir()
    idx.mkdir(parents=True, exist_ok=True)

    # vectors.npy — write to tmp then replace for atomicity.
    # np.save auto-appends ".npy" unless the name already ends in it, so use a
    # temp name that already ends in .npy to keep the written path predictable.
    tmp_npy = emb / "vectors.tmp.npy"
    np.save(str(tmp_npy), vectors)
    tmp_npy.replace(emb / "vectors.npy")

    write_json_atomic(emb / "chunk_ids.json", chunk_ids)
    write_json_atomic(idx / "manifest.json", manifest)


def _embed_chunks(chunks: list[Chunk]) -> np.ndarray:
    """Embed all chunk texts; return (N, 1024) float32 L2-normalised matrix."""
    texts = [c.text for c in chunks]
    return ollama_client.embed(texts)  # already L2-normalised per contract


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_index(kb_dir: Path) -> int:
    """Full rebuild from all .md files under kb_dir. Returns chunk count."""
    all_chunks: list[Chunk] = []
    for md_path in sorted(kb_dir.rglob("*.md")):
        all_chunks.extend(chunk_page(md_path))

    if not all_chunks:
        _save_index([], np.empty((0, 1024), dtype=np.float32), {})
        return 0

    vectors = _embed_chunks(all_chunks)

    chunk_ids = [c.chunk_id for c in all_chunks]
    manifest: dict[str, dict] = {}
    for chunk in all_chunks:
        manifest[chunk.chunk_id] = {
            "content_hash": _content_hash(chunk.text),
            "kb_path": chunk.kb_path,
            "heading_path": chunk.heading_path,
            "payload": _chunk_payload(chunk),
        }

    _save_index(chunk_ids, vectors, manifest)
    return len(all_chunks)


def upsert_changed(kb_dir: Path) -> dict:
    """
    Incremental update: diff current chunk content_hashes against stored manifest.
    Re-embeds only added/changed chunks; tombstones removed ones.
    Returns {"added": int, "removed": int, "unchanged": int}.
    """
    old_manifest = load_manifest()
    emb_path = paths.embeddings_dir() / "vectors.npy"
    ids_path = paths.embeddings_dir() / "chunk_ids.json"

    if emb_path.exists() and ids_path.exists():
        old_vectors = np.load(str(emb_path))
        old_ids: list[str] = json.loads(ids_path.read_text(encoding="utf-8"))
    else:
        old_vectors = np.empty((0, 1024), dtype=np.float32)
        old_ids = []

    # Gather current chunks
    current_chunks: list[Chunk] = []
    for md_path in sorted(kb_dir.rglob("*.md")):
        current_chunks.extend(chunk_page(md_path))

    current_by_id: dict[str, Chunk] = {c.chunk_id: c for c in current_chunks}
    current_hashes: dict[str, str] = {
        cid: _content_hash(chunk.text) for cid, chunk in current_by_id.items()
    }

    # Classify
    old_ids_set = set(old_ids)
    added_ids: list[str] = []
    unchanged_ids: list[str] = []
    removed_ids: list[str] = []

    for cid, chunk in current_by_id.items():
        h = current_hashes[cid]
        if cid not in old_manifest or old_manifest[cid]["content_hash"] != h:
            added_ids.append(cid)
        else:
            unchanged_ids.append(cid)

    for cid in old_ids_set:
        if cid not in current_by_id:
            removed_ids.append(cid)

    # Build new index:
    # 1. Keep unchanged rows from old matrix.
    old_row: dict[str, int] = {cid: i for i, cid in enumerate(old_ids)}
    new_ids: list[str] = unchanged_ids + added_ids
    kept_vectors = (
        np.stack([old_vectors[old_row[cid]] for cid in unchanged_ids])
        if unchanged_ids
        else np.empty((0, 1024), dtype=np.float32)
    )

    # 2. Embed added chunks.
    if added_ids:
        new_vecs = _embed_chunks([current_by_id[cid] for cid in added_ids])
        all_vectors = np.concatenate([kept_vectors, new_vecs], axis=0).astype(np.float32)
    else:
        all_vectors = kept_vectors.astype(np.float32)

    # 3. Build new manifest.
    new_manifest: dict[str, dict] = {}
    for cid in unchanged_ids:
        new_manifest[cid] = old_manifest[cid]
    for cid in added_ids:
        chunk = current_by_id[cid]
        new_manifest[cid] = {
            "content_hash": current_hashes[cid],
            "kb_path": chunk.kb_path,
            "heading_path": chunk.heading_path,
            "payload": _chunk_payload(chunk),
        }
    # removed_ids are simply omitted (tombstoned).

    _save_index(new_ids, all_vectors, new_manifest)
    return {
        "added": len(added_ids),
        "removed": len(removed_ids),
        "unchanged": len(unchanged_ids),
    }


def search(query_vec: np.ndarray, top_k: int) -> list[tuple[str, float]]:
    """
    Cosine similarity search.
    query_vec must be L2-normalised (same convention as stored vectors).
    Returns list of (chunk_id, score) sorted descending, length = min(top_k, N).
    """
    emb_path = paths.embeddings_dir() / "vectors.npy"
    ids_path = paths.embeddings_dir() / "chunk_ids.json"

    if not emb_path.exists() or not ids_path.exists():
        return []

    vectors: np.ndarray = np.load(str(emb_path))  # (N, 1024)
    chunk_ids: list[str] = json.loads(ids_path.read_text(encoding="utf-8"))

    if vectors.shape[0] == 0:
        return []

    scores: np.ndarray = vectors @ query_vec  # cosine; both sides normalised
    top_k = min(top_k, len(scores))
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(chunk_ids[i], float(scores[i])) for i in top_indices]


def load_manifest() -> dict:
    """Load indexes/manifest.json; returns {} if the file does not exist."""
    path = paths.indexes_dir() / "manifest.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def chunk_by_id(chunk_id: str) -> Chunk | None:
    """
    Reconstruct a Chunk from manifest payload.
    Re-reads the source .md file to restore the text field.
    Returns None if chunk_id is not in the manifest.
    """
    manifest = load_manifest()
    if chunk_id not in manifest:
        return None

    entry = manifest[chunk_id]
    kb_rel = entry["kb_path"]

    kb_abs = paths.repo_root() / kb_rel
    if not kb_abs.exists():
        # File was deleted; return Chunk with empty text.
        payload = entry["payload"]
        return Chunk(
            chunk_id=chunk_id,
            text="",
            kb_path=payload["kb_path"],
            heading_path=payload["heading_path"],
            source_url=payload.get("source_url"),
            source_tier=payload["source_tier"],
            source_count=payload["source_count"],
            verified=payload["verified"],
            availability=payload["availability"],
            changed_note=payload.get("changed_note"),
            score=0.0,
        )

    # Re-chunk the page to find this specific chunk's text.
    chunks = chunk_page(kb_abs)
    for c in chunks:
        if c.chunk_id == chunk_id:
            return c

    # Chunk no longer exists in current page content; return with empty text.
    payload = entry["payload"]
    return Chunk(
        chunk_id=chunk_id,
        text="",
        kb_path=payload["kb_path"],
        heading_path=payload["heading_path"],
        source_url=payload.get("source_url"),
        source_tier=payload["source_tier"],
        source_count=payload["source_count"],
        verified=payload["verified"],
        availability=payload["availability"],
        changed_note=payload.get("changed_note"),
        score=0.0,
    )
