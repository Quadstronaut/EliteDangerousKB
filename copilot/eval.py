"""
ED-RAG evaluation harness — measurement spine for retrieval quality.

Public API:
    retrieval_metrics(golden, *, top_k) -> dict
        Computes recall@k and MRR over on-topic golden questions.

    refusal_calibration(golden) -> dict
        Computes false_refusal_rate and false_answer_rate.

    load_golden(path=None) -> list[dict]
        Loads the golden question set from eval/golden_questions.json.

CLI:
    python -m copilot.eval [--golden PATH] [--top-k N]
    Builds/loads the index if needed, runs both metric functions, prints a report.
    Exits non-zero if Ollama is unavailable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from copilot.models import RetrievalResult
from copilot.paths import repo_root


# ---------------------------------------------------------------------------
# Golden question loader
# ---------------------------------------------------------------------------

def load_golden(path: str | Path | None = None) -> list[dict]:
    """Load golden questions JSON. Defaults to eval/golden_questions.json."""
    if path is None:
        path = repo_root() / "eval" / "golden_questions.json"
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Core metric helpers
# ---------------------------------------------------------------------------

def _rank_of_hit(result: RetrievalResult, record: dict) -> int | None:
    """Return the 1-based rank of the first hit, or None if no hit found."""
    expected_paths = set(record.get("expect_kb_paths", []))
    expected_subs = record.get("expect_chunk_substrings", [])

    for rank, chunk in enumerate(result.chunks, start=1):
        if chunk.kb_path in expected_paths:
            return rank
        if any(sub.lower() in chunk.text.lower() for sub in expected_subs):
            return rank
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def retrieval_metrics(
    golden: list[dict],
    *,
    top_k: int = 5,
) -> dict[str, Any]:
    """
    Compute recall@k and MRR over on-topic golden questions.

    Calls retriever.retrieve for each on-topic record (off_topic=False).
    Returns:
        {
            "recall_at_k": float,   # fraction of questions with a hit in top_k
            "mrr": float,           # mean reciprocal rank
            "top_k": int,
            "n_questions": int,
            "n_hits": int,
        }

    Raises copilot.ollama_client.OllamaUnavailable if Ollama is not reachable.
    """
    from copilot import retriever  # local import to allow test mocking

    on_topic = [r for r in golden if not r.get("off_topic", False)]
    n = len(on_topic)
    if n == 0:
        return {
            "recall_at_k": 0.0,
            "mrr": 0.0,
            "top_k": top_k,
            "n_questions": 0,
            "n_hits": 0,
        }

    hits = 0
    rr_sum = 0.0

    for record in on_topic:
        result = retriever.retrieve(record["question"], top_k=top_k)
        rank = _rank_of_hit(result, record)
        if rank is not None:
            hits += 1
            rr_sum += 1.0 / rank

    return {
        "recall_at_k": hits / n,
        "mrr": rr_sum / n,
        "top_k": top_k,
        "n_questions": n,
        "n_hits": hits,
    }


def refusal_calibration(golden: list[dict]) -> dict[str, Any]:
    """
    Compute false_refusal_rate and false_answer_rate.

    - false_refusal_rate: fraction of ON-TOPIC queries where grounded=False
      (the retriever refused to ground a legitimate question).
    - false_answer_rate: fraction of OFF-TOPIC queries where grounded=True
      (the retriever claims to answer a question it should refuse).

    Returns:
        {
            "false_refusal_rate": float,
            "false_answer_rate": float,
            "n_on_topic": int,
            "n_off_topic": int,
            "n_false_refusals": int,
            "n_false_answers": int,
        }

    Raises copilot.ollama_client.OllamaUnavailable if Ollama is not reachable.
    """
    from copilot import retriever  # local import to allow test mocking

    on_topic = [r for r in golden if not r.get("off_topic", False)]
    off_topic = [r for r in golden if r.get("off_topic", False)]

    false_refusals = 0
    for record in on_topic:
        result = retriever.retrieve(record["question"])
        if not result.grounded:
            false_refusals += 1

    false_answers = 0
    for record in off_topic:
        result = retriever.retrieve(record["question"])
        if result.grounded:
            false_answers += 1

    n_on = len(on_topic)
    n_off = len(off_topic)

    return {
        "false_refusal_rate": false_refusals / n_on if n_on else 0.0,
        "false_answer_rate": false_answers / n_off if n_off else 0.0,
        "n_on_topic": n_on,
        "n_off_topic": n_off,
        "n_false_refusals": false_refusals,
        "n_false_answers": false_answers,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Entry point for `python -m copilot.eval`.

    Degrades gracefully if Ollama is unavailable: prints a clear message,
    returns exit code 1. Never crashes with a raw traceback.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="ED-RAG evaluation harness — measures retrieval recall@k, MRR, and refusal calibration."
    )
    parser.add_argument(
        "--golden",
        default=None,
        help="Path to golden_questions.json (default: eval/golden_questions.json)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        dest="top_k",
        help="Top-k to use for recall and MRR (default: 5)",
    )
    args = parser.parse_args(argv)

    try:
        golden = load_golden(args.golden)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[eval] ERROR: could not load golden questions: {exc}", file=sys.stderr)
        return 1

    # Optionally build/load the index if it does not exist yet.
    try:
        from copilot import index as _index
        from copilot.paths import embeddings_dir

        emb_npy = embeddings_dir() / "vectors.npy"
        if not emb_npy.exists():
            print("[eval] No index found — building index from KB...", file=sys.stderr)
            from copilot.paths import kb_dir
            n = _index.build_index(kb_dir())
            print(f"[eval] Index built: {n} chunks.", file=sys.stderr)
    except Exception as exc:
        print(f"[eval] WARNING: index check/build failed: {exc}", file=sys.stderr)

    # Run metrics, catching Ollama unavailability gracefully.
    try:
        from copilot.ollama_client import OllamaUnavailable

        print(f"\n=== ED-RAG Evaluation — top_k={args.top_k} ===\n")

        ret = retrieval_metrics(golden, top_k=args.top_k)
        print("-- Retrieval Metrics --")
        print(f"  Questions (on-topic): {ret['n_questions']}")
        print(f"  Hits in top-{ret['top_k']}:      {ret['n_hits']}")
        print(f"  Recall@{ret['top_k']}:            {ret['recall_at_k']:.3f}")
        print(f"  MRR:                 {ret['mrr']:.3f}")

        print()

        cal = refusal_calibration(golden)
        print("-- Refusal Calibration --")
        print(f"  On-topic questions:  {cal['n_on_topic']}")
        print(f"  Off-topic questions: {cal['n_off_topic']}")
        print(f"  False refusals:      {cal['n_false_refusals']}  (rate: {cal['false_refusal_rate']:.3f})")
        print(f"  False answers:       {cal['n_false_answers']}  (rate: {cal['false_answer_rate']:.3f})")
        print()

    except Exception as exc:
        # Catch OllamaUnavailable and any other runtime failure cleanly.
        print(f"\n[eval] Ollama unavailable or retrieval error: {exc}", file=sys.stderr)
        print("[eval] Ensure `ollama serve` is running and bge-m3 is pulled.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
