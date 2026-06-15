"""
Pure retrieval core: embed query → vector search → hydrate Chunks → filter → grade.

No prompt assembly, no profile injection — see assemble.py for those concerns.
"""

from __future__ import annotations

import dataclasses

from copilot import index as _index
from copilot import ollama_client
from copilot.models import Chunk, RetrievalResult
from copilot.paths import load_config
from copilot.query_expand import expand_query, EXPAND_QUERY_DEFAULT


def _config() -> dict:
    """Return the parsed config dict (thin wrapper so tests can patch it).

    Intentionally NOT cached with lru_cache — test monkeypatching replaces this
    function at the module level, so caching would bake in the real config on
    first call and make the mock invisible to subsequent calls.
    """
    return load_config()


def retrieval_filters(cfg: dict) -> dict | None:
    """Translate config[copilot][mode] into retrieve() filters.

    verified_only (the default) restricts retrieval to chunks flagged
    verified=True — the trust boundary the spec promises. include_unverified
    drops the filter so lower-tier capture chunks are eligible.
    """
    mode = cfg.get("copilot", {}).get("mode", "verified_only")
    return {"verified": True} if mode == "verified_only" else None


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

    # 1. Expand the query with ED synonym/abbreviation expansions before
    #    embedding.  The expansion appends known terms so dense embeddings match
    #    both abbreviated and full-form ED terminology.  RetrievalResult.query
    #    is always set to the ORIGINAL query so citations and UX are unchanged.
    embed_text = expand_query(query) if EXPAND_QUERY_DEFAULT else query
    query_vec = ollama_client.embed([embed_text])[0]  # shape (1024,)

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

    # 3b. Drop chunks whose text is empty (stale manifest entry whose source
    # section no longer exists). An empty chunk contributes nothing but its id,
    # which the model could "cite" — a citation to nothing. Never serve them.
    chunks = [c for c in chunks if c.text.strip()]

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
