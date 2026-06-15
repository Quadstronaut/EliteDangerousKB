"""
copilot/sparse.py — BM25 sparse retrieval for the ED Knowledge Engine.

VALUE-NOW VERDICT (spec §5):
    At ~5 pages / 27 chunks, dense recall@5 is already 1.0 and MRR is near-ceiling.
    BM25 adds no measurable headroom on today's corpus. This module is SCAFFOLDING
    FOR GROWTH — it becomes valuable when the autonomous research loop grows the KB
    to hundreds of chunks, where two failure modes emerge:

    (a) Rare exact lexical tokens (commodity names like "Tritium", system names,
        version strings like "Update 19.04") that bge-m3 under-matches because the
        embedding model distributes meaning across a semantic cone — a rare proper
        noun can land far from its nearest dense neighbour.

    (b) Recall dilution: as N grows and the dense cone widens, lexically-obvious
        hits fall outside the top-k cosine window.

    Kill switch: set config[retrieval].fusion = "dense" to restore exact legacy
    behaviour without calling this module at all.

Public API:
    tokenize(text)                     → list[str]
    build_from_corpus(corpus)          → SparseIndex  (in-memory, no I/O)
    search_index(idx, query, top_k)    → list[tuple[str, float]]
    persist(corpus)                    → None          (writes sparse artifact)
    load_ids()                         → list[str]     (from persisted artifact)
    search(query, top_k)               → list[tuple[str, float]]  (from disk)

Design: self-rolled BM25+ (Robertson–Spärck Jones) with zero new dependencies.
The index is serialised as JSON (not pickle) for portability and debuggability.
Path helpers flow through paths.* so test monkeypatching redirects to tmp_path.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import TypedDict


# ---------------------------------------------------------------------------
# Public type alias — the in-memory sparse index structure.
# ---------------------------------------------------------------------------

class SparseIndex(TypedDict):
    """In-memory BM25 index.

    Fields:
        idf:        {term: idf_score}              — per-term inverse document frequency
        tf:         {chunk_id: {term: tf_score}}   — BM25-normalised term frequency
        chunk_ids:  [chunk_id, ...]                 — all indexed chunk ids (deterministic order)
        avgdl:      float                           — average document length in tokens
        N:          int                             — total document count
    """
    idf: dict[str, float]
    tf: dict[str, dict[str, float]]
    chunk_ids: list[str]
    avgdl: float
    N: int


# BM25+ parameters. k1 and b are standard corpus-invariant defaults.
# delta raises the floor above 0 so non-matching terms don't drown rare hits.
_BM25_K1: float = 1.5
_BM25_B: float = 0.75
_BM25_DELTA: float = 1.0   # BM25+ variant (Lv & Zhai, 2011)

# Regex: split on whitespace and any common punctuation, lowercase.
_SPLIT_RE = re.compile(r"[^\w]+")


# ---------------------------------------------------------------------------
# Tokeniser (identical at build time and query time — no train/query skew)
# ---------------------------------------------------------------------------

def tokenize(text: str) -> list[str]:
    """Deterministic, lowercase, punctuation-splitting tokeniser.

    Same function used at index build time and query time, so there is NO
    tokenisation skew between what was indexed and what is searched.
    Pure Python — no I/O, no external dependencies.

    Punctuation is treated as a token boundary (not a token), so
    "Tritium, Hydrogen" → ["tritium", "hydrogen"].
    Empty tokens from leading/trailing punctuation are dropped.
    """
    lower = text.lower()
    tokens = _SPLIT_RE.split(lower)
    return [t for t in tokens if t]  # drop empty strings from split artefacts


# ---------------------------------------------------------------------------
# In-memory BM25 build
# ---------------------------------------------------------------------------

def build_from_corpus(corpus: dict[str, str]) -> SparseIndex:
    """Build an in-memory BM25 index from a {chunk_id: text} corpus.

    No disk I/O. Safe to call from tests or from persist().

    BM25+ formula per term t, document d:
        TF(t,d)  = ((k1+1) * tf_raw) / (k1*(1-b + b*dl/avgdl) + tf_raw) + delta
        IDF(t)   = log((N - df + 0.5) / (df + 0.5) + 1)
        score(q,d) = Σ_{t∈q} IDF(t) * TF(t,d)

    Args:
        corpus: {chunk_id: text} dict.  May be empty.

    Returns:
        SparseIndex typed dict.
    """
    if not corpus:
        return SparseIndex(idf={}, tf={}, chunk_ids=[], avgdl=0.0, N=0)

    chunk_ids = list(corpus.keys())
    N = len(chunk_ids)

    # 1. Tokenise all documents; compute per-doc term frequencies (raw counts).
    raw_tf: dict[str, dict[str, int]] = {}   # chunk_id → {term: count}
    dl: dict[str, int] = {}                   # chunk_id → doc length in tokens

    for cid, text in corpus.items():
        tokens = tokenize(text)
        dl[cid] = len(tokens)
        counts: dict[str, int] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        raw_tf[cid] = counts

    avgdl = sum(dl.values()) / N

    # 2. Document frequencies: how many docs contain each term.
    df: dict[str, int] = {}
    for counts in raw_tf.values():
        for term in counts:
            df[term] = df.get(term, 0) + 1

    # 3. IDF scores (BM25+ variant).
    idf: dict[str, float] = {
        term: math.log((N - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
        for term, doc_freq in df.items()
    }

    # 4. Normalised TF scores per document (BM25+ with delta floor).
    tf_store: dict[str, dict[str, float]] = {}
    for cid in chunk_ids:
        doc_len = dl[cid]
        counts = raw_tf[cid]
        # Guard avgdl==0 (every doc tokenises to zero length): defer the
        # length-norm ratio to 0.0 instead of dividing by zero. Without this,
        # build_from_corpus raises ZeroDivisionError out of persist() INSIDE
        # _save_index's lock AFTER the dense triple is written, breaking the
        # dense+sparse atomic-group invariant (council route-back, MAJOR).
        length_ratio = (doc_len / avgdl) if avgdl > 0 else 0.0
        norm_factor = _BM25_K1 * (1.0 - _BM25_B + _BM25_B * length_ratio)
        tf_doc: dict[str, float] = {}
        for term, raw_count in counts.items():
            tf_doc[term] = (_BM25_K1 + 1) * raw_count / (norm_factor + raw_count) + _BM25_DELTA
        tf_store[cid] = tf_doc

    return SparseIndex(
        idf=idf,
        tf=tf_store,
        chunk_ids=chunk_ids,
        avgdl=avgdl,
        N=N,
    )


# ---------------------------------------------------------------------------
# In-memory search
# ---------------------------------------------------------------------------

def search_index(
    idx: SparseIndex,
    query: str,
    top_k: int,
) -> list[tuple[str, float]]:
    """Query an in-memory SparseIndex.

    Returns:
        list of (chunk_id, bm25_score) sorted descending by score.
        BM25 scores are NOT cosine — they are NOT in [0,1].

    Args:
        idx:   In-memory SparseIndex from build_from_corpus().
        query: Raw query string; tokenised with the same tokenize() function.
        top_k: Maximum number of results to return.
    """
    if idx["N"] == 0 or not query or top_k <= 0:
        return []

    query_terms = tokenize(query)
    if not query_terms:
        return []

    idf = idx["idf"]
    tf_store = idx["tf"]
    chunk_ids = idx["chunk_ids"]

    # Score every document.  Only terms present in both query and index contribute.
    scores: dict[str, float] = {}
    for term in query_terms:
        term_idf = idf.get(term, 0.0)
        if term_idf == 0.0:
            continue
        for cid in chunk_ids:
            tf_val = tf_store[cid].get(term, 0.0)
            if tf_val > 0.0:
                scores[cid] = scores.get(cid, 0.0) + term_idf * tf_val

    # Sort descending; return top_k.
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


# ---------------------------------------------------------------------------
# Persistence — sparse artifact alongside the dense index
# ---------------------------------------------------------------------------

_SPARSE_ARTIFACT_NAME = "sparse_index.json"


def _artifact_path() -> Path:
    """Return the path to the sparse artifact.

    Flows through paths.embeddings_dir() so test monkeypatching of that
    function redirects writes/reads to tmp_path — no cross-test pollution and
    no artifact written to the real repo during tests.
    """
    from copilot import paths
    return paths.embeddings_dir() / _SPARSE_ARTIFACT_NAME


def persist(corpus: dict[str, str]) -> None:
    """Build a BM25 index from corpus and write the sparse artifact to disk.

    MUST be called while the index file_lock is already held — the caller
    (index._save_index) owns the lock contract.  This function does NOT
    acquire the lock itself; it is a grouped write under the caller's lock.

    Artifact: embeddings/sparse_index.json (JSON for portability).

    Args:
        corpus: {chunk_id: text} dict — the same deduped corpus that was
                used to build the dense index.
    """
    from copilot.atomic import write_json_atomic

    idx = build_from_corpus(corpus)

    # Serialise to a format that round-trips cleanly via JSON.
    payload = {
        "idf": idx["idf"],
        "tf": idx["tf"],
        "chunk_ids": idx["chunk_ids"],
        "avgdl": idx["avgdl"],
        "N": idx["N"],
    }
    write_json_atomic(_artifact_path(), payload)


def _load_artifact() -> SparseIndex | None:
    """Load and deserialise the sparse artifact from disk.

    Returns None if the artifact does not exist or is unreadable.
    Callers treat None as "sparse backend unavailable → degrade to dense".
    """
    path = _artifact_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return SparseIndex(
            idf=data["idf"],
            tf=data["tf"],
            chunk_ids=data["chunk_ids"],
            avgdl=float(data["avgdl"]),
            N=int(data["N"]),
        )
    except (KeyError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(
            f"[sparse] WARNING: sparse_index.json unreadable ({exc}) — degrading to dense only",
            file=sys.stderr,
        )
        return None


def load_ids() -> list[str]:
    """Return chunk_ids the persisted sparse index can return.

    Used by the consistency invariant test to assert that
    set(sparse.load_ids()) == set(chunk_ids from dense index).

    Returns [] if no artifact exists.  Never raises.
    """
    idx = _load_artifact()
    if idx is None:
        return []
    return list(idx["chunk_ids"])


def search(query: str, top_k: int) -> list[tuple[str, float]]:
    """Load the persisted sparse index and search it.

    Returns [] (never raises) if no artifact exists.
    The caller (retriever.py) treats a raised exception as degrade-to-dense,
    but this function also swallows its own errors defensively.

    Args:
        query:  Raw query string.
        top_k:  Maximum results to return.

    Returns:
        list of (chunk_id, bm25_score) sorted descending, or [].
    """
    try:
        idx = _load_artifact()
        if idx is None:
            return []
        return search_index(idx, query, top_k)
    except Exception as exc:
        print(
            f"[sparse] WARNING: sparse search failed ({exc}) — degrading to dense only",
            file=sys.stderr,
        )
        return []
