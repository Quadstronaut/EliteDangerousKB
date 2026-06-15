"""
Pure retrieval core: embed query → vector search → [hybrid fusion] → hydrate Chunks → filter → grade.

No prompt assembly, no profile injection — see assemble.py for those concerns.

Hybrid retrieval path (config[retrieval].fusion = "rrf"):
    1. Embed the expanded query → dense cosine search (wide candidate set = candidate_k).
    2. BM25 sparse search over the same wide candidate set.
    3. RRF fuse the two ranked lists → reranked candidate pool.
    4. Hydrate chunk ids in fused order → drop empty-text chunks.
    5. Apply filters (e.g. verified=True).
    6. Compute grounding from POST-FILTER dense cosine scores (NOT RRF scores).
       max_score ∈ [0,1] is always a cosine similarity.
       grounded = max_score >= tau.

    This keeps the refusal gate anchored to semantic similarity, preventing a
    high BM25/RRF score from laundering a false-positive past the trust threshold.

Kill switch: config[retrieval].fusion = "dense" restores the exact legacy path
without calling sparse.search at all — byte-for-byte identical to pre-hybrid behaviour.

VALUE-NOW VERDICT: At ~27 chunks, recall@5 is already 1.0 and MRR is near-ceiling.
Hybrid fusion does NOT move those needles yet. This is scaffolding for growth;
proven net-neutral on the current golden set (see eval/golden_questions.json).
"""

from __future__ import annotations

import dataclasses
import sys

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
    Embed query, search index (dense + optional sparse fusion), hydrate Chunks,
    apply filters, and compute grounding.

    Signature UNCHANGED from the pre-hybrid API.

    grounded = max_DENSE_cosine_of_surviving_chunks >= config.retrieval.tau
    max_score is always a cosine in [0,1], never an RRF score.
    If the index is empty or all chunks are filtered away, grounded=False.

    RetrievalResult.query == original query (not the expanded form used for embedding).
    """
    cfg = _config()
    tau: float = cfg["retrieval"]["tau"]
    k: int = top_k if top_k is not None else cfg["retrieval"]["top_k"]

    # Retrieve fusion config with safe defaults (additive — old configs without
    # these keys fall back to the legacy dense-only path automatically).
    retrieval_cfg = cfg.get("retrieval", {})
    fusion_mode: str = retrieval_cfg.get("fusion", "dense")   # "rrf" | "dense"
    rrf_k: int = int(retrieval_cfg.get("rrf_k", 60))
    candidate_k: int = int(retrieval_cfg.get("candidate_k", max(32, k * 4)))

    # 1. Expand the query with ED synonym/abbreviation expansions before
    #    embedding.  The expansion appends known terms so dense embeddings match
    #    both abbreviated and full-form ED terminology.  RetrievalResult.query
    #    is always set to the ORIGINAL query so citations and UX are unchanged.
    embed_text = expand_query(query) if EXPAND_QUERY_DEFAULT else query
    query_vec = ollama_client.embed([embed_text])[0]  # shape (1024,)

    # 2. Dense cosine search.
    #    Under hybrid (fusion="rrf") we use a WIDE candidate set (candidate_k)
    #    for recall-first retrieval before fusion narrows to top_k.
    #    Under dense-only (fusion="dense") we use exactly k — identical to legacy.
    dense_top_k = candidate_k if fusion_mode == "rrf" else k
    dense_hits = _index.search(query_vec, dense_top_k)

    if not dense_hits and fusion_mode != "rrf":
        # Legacy fast-path: empty dense → done.
        return RetrievalResult(query=query, chunks=[], max_score=0.0, grounded=False)

    # 3. Hybrid path: sparse search + RRF fusion.
    if fusion_mode == "rrf":
        sparse_hits = _sparse_search_safe(query, candidate_k)

        if sparse_hits or dense_hits:
            from copilot.fusion import rrf_fuse
            fused = rrf_fuse(dense_hits, sparse_hits, k=rrf_k, top_k=k)
        else:
            # Both backends empty → no results.
            return RetrievalResult(query=query, chunks=[], max_score=0.0, grounded=False)

        # Hydrate in FUSED order.
        ordered_ids = [cid for cid, _ in fused]
    else:
        # Dense-only path (fusion="dense") — exact legacy behaviour.
        ordered_ids = [cid for cid, _ in dense_hits]

    # Build a lookup of dense cosine scores by chunk_id.
    # Grounding uses POST-FILTER dense cosine, NOT RRF score (spec §grounding).
    dense_score_map: dict[str, float] = {cid: score for cid, score in dense_hits}

    # 4. Hydrate Chunks; attach dense cosine score via dataclasses.replace.
    #    Chunks whose chunk_id had no dense hit get score 0.0 (only possible
    #    under hybrid when a sparse-only hit surfaces a chunk that didn't land
    #    in the dense candidate_k window — rare but handled defensively).
    chunks: list[Chunk] = []
    for chunk_id in ordered_ids:
        chunk = _index.chunk_by_id(chunk_id)
        if chunk is None:
            continue
        dense_cos = dense_score_map.get(chunk_id, 0.0)
        chunks.append(dataclasses.replace(chunk, score=dense_cos))

    # 4b. Drop chunks whose text is empty (stale manifest entry whose source
    # section no longer exists). An empty chunk contributes nothing but its id,
    # which the model could "cite" — a citation to nothing. Never serve them.
    chunks = [c for c in chunks if c.text.strip()]

    # 5. Apply filters (e.g. {"verified": True}).
    #    Grounding is computed from POST-FILTER scores only — a high-cosine
    #    UNVERIFIED chunk that is filtered out does NOT keep grounding alive.
    if filters:
        for key, value in filters.items():
            chunks = [c for c in chunks if getattr(c, key, None) == value]

    # 6. Grounding uses POST-FILTER dense cosine scores — NEVER RRF scores.
    #    This ensures the refusal gate cannot be laundered by a high BM25 score.
    max_score = max((c.score for c in chunks), default=0.0)
    grounded = max_score >= tau

    return RetrievalResult(
        query=query,
        chunks=chunks,
        max_score=max_score,
        grounded=grounded,
    )


def _sparse_search_safe(query: str, top_k: int) -> list[tuple[str, float]]:
    """Call sparse.search() with graceful degradation on any failure.

    Returns [] on any exception (missing artifact, corrupt file, import error).
    The caller (retrieve()) treats [] as "no sparse signal" and continues with
    whatever dense results it already has — grounding is not weakened.

    This is the degrade-to-dense path mandated by the spec's acceptance test
    test_sparse_backend_missing_degrades_to_dense.
    """
    try:
        from copilot import sparse
        return sparse.search(query, top_k)
    except Exception as exc:
        print(
            f"[retriever] WARNING: sparse search failed ({exc}) — degrading to dense only",
            file=sys.stderr,
        )
        return []
