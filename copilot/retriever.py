"""
Pure retrieval core: embed query → vector search → hydrate Chunks → filter → grade.

No prompt assembly, no profile injection — see assemble.py for those concerns.
"""

from __future__ import annotations

import dataclasses
from functools import lru_cache

from copilot import index as _index
from copilot import ollama_client
from copilot.models import Chunk, RetrievalResult
from copilot.paths import load_config


def _config() -> dict:
    """Return the parsed config dict (thin wrapper so tests can patch it)."""
    return load_config()


def retrieve(
    query: str,
    *,
    top_k: int | None = None,
    filters: dict | None = None,
) -> RetrievalResult:
    """
    Embed query, search index, hydrate Chunks with cosine score, apply filters.

    grounded = max_score >= config.retrieval.tau
    If the index is empty or all chunks are filtered away, grounded=False.
    """
    cfg = _config()
    tau: float = cfg["retrieval"]["tau"]
    k: int = top_k if top_k is not None else cfg["retrieval"]["top_k"]

    # 1. Embed the query into a single (1024,) normalised vector.
    query_vec = ollama_client.embed([query])[0]  # shape (1024,)

    # 2. Search index.
    hits = _index.search(query_vec, k)
    if not hits:
        return RetrievalResult(
            query=query, chunks=[], max_score=0.0, grounded=False
        )

    # 3. Hydrate Chunks; attach cosine score via dataclasses.replace.
    chunks: list[Chunk] = []
    for chunk_id, score in hits:
        chunk = _index.chunk_by_id(chunk_id)
        if chunk is None:
            continue
        chunks.append(dataclasses.replace(chunk, score=score))

    # 4. Apply filters (e.g. {"verified": True}).
    if filters:
        for key, value in filters.items():
            chunks = [c for c in chunks if getattr(c, key, None) == value]

    max_score = max((c.score for c in chunks), default=0.0)
    grounded = max_score >= tau

    return RetrievalResult(
        query=query,
        chunks=chunks,
        max_score=max_score,
        grounded=grounded,
    )
