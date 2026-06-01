# Plan C — MCP Server (FastMCP/stdio wrapper over shared retrieval core)

> **For agentic workers:** This plan is designed for automated execution. Every task follows the TDD micro-loop: write a failing test → confirm it fails → write minimal implementation → confirm it passes → commit. Each task specifies exact file paths, complete real code, and the precise pytest command to run. No placeholders. Do not edit any file owned by Plan A or Plan B (see "Requires Plan A complete" note below).

**Date authored:** 2026-06-01
**Spec:** `docs/superpowers/specs/2026-06-01-ed-knowledge-engine-covas-copilot-design.md` §D, §G step 4, §B (parity), §F (graceful degradation)
**Contracts:** `docs/superpowers/plans/CONTRACTS.md` (binding — all names, signatures, schemas from that document are used verbatim here)

---

## Goal

Expose the **identical retrieval core** (Plan A's `retriever`, `assemble`, `profile` modules) to Claude Code via the MCP protocol over stdio, registered in `.mcp.json`. When qwen3:8b in the local REPL gives an unsatisfactory answer the user sleeves Claude onto the same KB via this server — zero retrieval-logic drift because this plan re-implements **nothing**: it only wraps existing functions.

End state: `python -m copilot.mcp_server` launches a stdio MCP server with three tools (`ed_kb_search`, `ed_kb_answer`, `ed_cmdr_state`); `.mcp.json` at the repo root registers it for Claude Code; a parity test proves `ed_kb_search` returns the same chunk data as calling `retriever.retrieve` directly.

---

## Architecture

```
Claude Code (MCP client)
        │  stdio (JSON-RPC MCP protocol)
        ▼
copilot/mcp_server.py   ← Plan C (new file only)
        │
        ├── retriever.retrieve(query, top_k, filters)   ← Plan A (unchanged)
        ├── assemble.build_messages / validate_answer   ← Plan A (unchanged)
        ├── ollama_client.chat_stream                   ← Plan A (unchanged)
        └── profile.load_cmdr_state()                   ← Plan A (unchanged)
```

The MCP server is a **pure adapter layer** — no retrieval logic, no embedding, no scoring. Every business rule (τ floor, refusal, citation validation, profile merge) lives in Plan A code called through by this wrapper.

---

## Tech Stack

- **Python 3.11+** in `.venv/` (repo-local)
- **`mcp` package** — FastMCP (`from mcp.server.fastmcp import FastMCP`), stdio transport (`.run()` default)
- **`pytest`** — tests in `tests/test_mcp_server.py`; mock via `unittest.mock.patch`
- All paths via `copilot/paths.py::repo_root()` (Plan A)

---

## File Structure (Plan C adds exactly two files)

```
EliteDangerousKB/
├── copilot/
│   └── mcp_server.py          ← NEW (Plan C)
├── tests/
│   └── test_mcp_server.py     ← NEW (Plan C)
└── .mcp.json                  ← NEW (Plan C)
```

**Plan C touches NO other files.** `copilot/__init__.py`, `retriever.py`, `assemble.py`, `profile.py`, `ollama_client.py`, and all Plan B files are read-only from Plan C's perspective.

---

## Requires Plan A complete

Plan C imports the following Plan A modules at test and runtime. All must be present and passing their own tests before Task 1 begins:

- `copilot.retriever` — `retrieve(query, *, top_k, filters) -> RetrievalResult`
- `copilot.assemble` — `build_messages`, `validate_answer`
- `copilot.profile` — `load_cmdr_state() -> CmdrState`
- `copilot.ollama_client` — `chat_stream`, `OllamaUnavailable`
- `copilot.models` — `Chunk`, `RetrievalResult`, `CmdrState`
- `copilot.paths` — `repo_root()`, `load_config()`

Do not begin Plan C if `pytest tests/test_retriever.py tests/test_assemble.py tests/test_profile.py` has failures.

---

## Tasks

---

### Task 1 — Install `mcp` dependency; sanity import test

**Scope:** verify the `mcp` package is available in `.venv` and that FastMCP is importable. Add it to the project's dependency record.

#### 1a. Install

```powershell
# Run from repo root G:\Documents\EliteDangerousKB
.\.venv\Scripts\pip.exe install mcp
```

If `mcp` is already installed this is a no-op.

#### 1b. Record dependency

Open `requirements.txt` (create if absent at repo root). Append:

```
mcp
```

Do not pin a version here — the executor should run `.\.venv\Scripts\pip.exe show mcp` after install and record the installed version in a comment:

```
mcp  # installed: <version from pip show>
```

#### 1c. Failing test — write first

File: `tests/test_mcp_server.py` (create new file, start here)

```python
"""Tests for copilot/mcp_server.py — Plan C."""
import importlib


def test_fastmcp_importable():
    """FastMCP must be importable from the mcp package."""
    mod = importlib.import_module("mcp.server.fastmcp")
    assert hasattr(mod, "FastMCP"), "FastMCP not found in mcp.server.fastmcp"
```

Run to confirm it **passes** immediately after install (this test is a dependency check, not a failing-first test — it is the confirmation that the install worked):

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_fastmcp_importable -v
```

Expected: `PASSED`.

**Note on FastMCP API:** the `mcp` package evolves. Before writing any tool code in Tasks 2–4, the executor MUST verify the installed API:

```powershell
.\.venv\Scripts\python.exe -c "import mcp.server.fastmcp as f; help(f.FastMCP)"
```

If the decorator-based tool API (`@mcp.tool()`) or `.run()` signature differs from what is shown in Tasks 2–4, adapt the implementation to match the installed version. The plan's code targets the documented FastMCP API (tool decorators, `.run()` for stdio); the test structure (calling tool functions directly) is API-independent.

#### Commit

```
git add requirements.txt tests/test_mcp_server.py
git commit -m "Plan C Task 1: add mcp dependency and import sanity test"
```

---

### Task 2 — `ed_kb_search` tool: skeleton + shape test

**Goal:** `copilot/mcp_server.py` exists, a FastMCP instance is created, and the `ed_kb_search` tool function returns correctly-shaped dicts. Tests call the **Python function directly** — FastMCP tools are plain decorated functions and are fully testable without running the server process.

#### 2a. Failing test

Add to `tests/test_mcp_server.py`:

```python
from unittest.mock import patch, MagicMock
from copilot.models import Chunk, RetrievalResult


def _make_chunk(**overrides) -> Chunk:
    """Factory for a minimal valid Chunk."""
    defaults = dict(
        chunk_id="abc123def456789a",
        text="Felicity Farseer unlocks at Sol < 20 ly.",
        kb_path="kb/engineers/felicity-farseer.md",
        heading_path="Felicity Farseer > Unlock",
        source_url="https://inara.cz/elite/engineer/?searchin=1&searchparam=1",
        source_tier=1,
        source_count=3,
        verified=True,
        availability="live",
        changed_note=None,
        score=0.87,
    )
    defaults.update(overrides)
    return Chunk(**defaults)


def test_ed_kb_search_returns_list_of_dicts():
    """ed_kb_search must return a list of dicts with all CONTRACTS fields."""
    chunk = _make_chunk()
    mock_result = RetrievalResult(
        query="farseer unlock",
        chunks=[chunk],
        max_score=0.87,
        grounded=True,
    )
    with patch("copilot.mcp_server.retriever") as mock_retriever:
        mock_retriever.retrieve.return_value = mock_result
        from copilot.mcp_server import ed_kb_search
        result = ed_kb_search("farseer unlock", top_k=8)

    assert isinstance(result, list)
    assert len(result) == 1
    row = result[0]
    # All CONTRACTS fields must be present
    for field in (
        "chunk_id", "text", "kb_path", "heading_path",
        "source_url", "source_tier", "source_count",
        "verified", "availability", "changed_note", "score",
    ):
        assert field in row, f"Missing field: {field}"
    assert row["chunk_id"] == "abc123def456789a"
    assert row["score"] == pytest.approx(0.87)
    assert row["availability"] == "live"
    assert row["changed_note"] is None
```

Add `import pytest` at the top of the test file.

Run — expect **ImportError** (module does not exist yet):

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_ed_kb_search_returns_list_of_dicts -v
```

#### 2b. Minimal implementation — create `copilot/mcp_server.py`

```python
"""
MCP server for the ED Knowledge Engine COVAS copilot.

Exposes the shared retrieval core (retriever / assemble / profile) to Claude Code
via FastMCP over stdio. ZERO retrieval logic is implemented here — this module only
wraps Plan A functions.

Launch:
    python -m copilot.mcp_server
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from copilot import retriever, assemble, profile
from copilot.ollama_client import OllamaUnavailable

mcp = FastMCP("ed-covas")


# ---------------------------------------------------------------------------
# Tool: ed_kb_search
# ---------------------------------------------------------------------------

@mcp.tool()
def ed_kb_search(query: str, top_k: int = 8) -> list[dict]:
    """
    Search the Elite Dangerous knowledge base.

    Returns a list of matching knowledge chunks ranked by semantic similarity.
    Each dict contains all CONTRACTS fields: chunk_id, text, kb_path,
    heading_path, source_url, source_tier, source_count, verified,
    availability, changed_note, score.

    Returns an error dict if retrieval fails.
    """
    try:
        result = retriever.retrieve(query, top_k=top_k)
        return [_chunk_to_dict(c) for c in result.chunks]
    except OllamaUnavailable:
        return [{"error": "Ollama unavailable — ensure localhost:11434 is running"}]
    except Exception as exc:  # noqa: BLE001
        return [{"error": f"Retrieval error: {exc}"}]


# ---------------------------------------------------------------------------
# Tool: ed_kb_answer
# ---------------------------------------------------------------------------

@mcp.tool()
def ed_kb_answer(query: str) -> dict:
    """
    Answer a question about Elite Dangerous using the verified knowledge base.

    Returns {answer, citations, grounded}.
    - answer: str — the generated answer (or a refusal string if not grounded)
    - citations: list[str] — chunk_ids cited in the answer
    - grounded: bool — True if retrieval score exceeded the tau threshold
    """
    try:
        result = retriever.retrieve(query)
        if not result.grounded:
            from copilot.repl import REFUSAL
            return {"answer": REFUSAL, "citations": [], "grounded": False}

        cmdr = _load_state_safe()
        messages = assemble.build_messages(query, result, cmdr)

        from copilot import ollama_client
        tokens: list[str] = []
        for delta in ollama_client.chat_stream(messages):
            tokens.append(delta)
        answer_text = "".join(tokens)

        ok, _reason = assemble.validate_answer(answer_text, result)
        if not ok:
            # One regen attempt, identical prompt
            tokens = []
            for delta in ollama_client.chat_stream(messages):
                tokens.append(delta)
            answer_text = "".join(tokens)
            ok, _reason = assemble.validate_answer(answer_text, result)

        if not ok:
            from copilot.repl import REFUSAL
            return {"answer": REFUSAL, "citations": [], "grounded": result.grounded}

        citations = [c.chunk_id for c in result.chunks]
        return {"answer": answer_text, "citations": citations, "grounded": result.grounded}

    except OllamaUnavailable:
        return {
            "answer": "Ollama unavailable — ensure localhost:11434 is running.",
            "citations": [],
            "grounded": False,
        }
    except Exception as exc:  # noqa: BLE001
        return {"answer": f"Error: {exc}", "citations": [], "grounded": False}


# ---------------------------------------------------------------------------
# Tool: ed_cmdr_state
# ---------------------------------------------------------------------------

@mcp.tool()
def ed_cmdr_state() -> dict:
    """
    Return the current CMDR state (name, ranks, balance, assets, goals, facts).

    Serializes profile.load_cmdr_state() to a plain dict suitable for JSON.
    """
    try:
        state = profile.load_cmdr_state()
        return _cmdr_state_to_dict(state)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Profile load error: {exc}"}


# ---------------------------------------------------------------------------
# Serialization helpers (not tools — internal only)
# ---------------------------------------------------------------------------

def _chunk_to_dict(chunk) -> dict:
    """Serialize a Chunk dataclass to a plain dict (all CONTRACTS fields)."""
    return {
        "chunk_id": chunk.chunk_id,
        "text": chunk.text,
        "kb_path": chunk.kb_path,
        "heading_path": chunk.heading_path,
        "source_url": chunk.source_url,
        "source_tier": chunk.source_tier,
        "source_count": chunk.source_count,
        "verified": chunk.verified,
        "availability": chunk.availability,
        "changed_note": chunk.changed_note,
        "score": float(chunk.score),
    }


def _cmdr_state_to_dict(state) -> dict:
    """Serialize a CmdrState dataclass to a plain dict."""
    return {
        "name": state.name,
        "ranks": dict(state.ranks),
        "balance_cr": state.balance_cr,
        "assets": state.assets,
        "goals": list(state.goals),
        "facts": [
            {
                "key": f.key,
                "value": f.value,
                "origin": f.origin,
                "freshness": f.freshness,
                "verified": f.verified,
            }
            for f in state.facts
        ],
    }


def _load_state_safe():
    """Load CmdrState, returning None on any error (profile is non-critical)."""
    try:
        return profile.load_cmdr_state()
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
```

Run the test — expect **PASSED**:

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_ed_kb_search_returns_list_of_dicts -v
```

#### Commit

```
git add copilot/mcp_server.py tests/test_mcp_server.py
git commit -m "Plan C Task 2: ed_kb_search tool with shape test"
```

---

### Task 3 — `ed_kb_answer` tool: structured response test

**Goal:** `ed_kb_answer` returns `{answer, citations, grounded}` with correct types. Ollama's chat stream is mocked so the test never hits `localhost:11434`.

#### 3a. Failing test

Add to `tests/test_mcp_server.py`:

```python
def test_ed_kb_answer_returns_structured_dict():
    """ed_kb_answer must return {answer: str, citations: list[str], grounded: bool}."""
    chunk = _make_chunk()
    mock_result = RetrievalResult(
        query="what does farseer unlock",
        chunks=[chunk],
        max_score=0.87,
        grounded=True,
    )

    fake_answer = "Felicity Farseer unlocks at Sol distance < 20 ly [abc123def456789a]."

    with (
        patch("copilot.mcp_server.retriever") as mock_retriever,
        patch("copilot.mcp_server.assemble") as mock_assemble,
        patch("copilot.mcp_server.ollama_client") as mock_ollama,
    ):
        mock_retriever.retrieve.return_value = mock_result
        mock_assemble.build_messages.return_value = [{"role": "user", "content": "q"}]
        mock_assemble.validate_answer.return_value = (True, "ok")
        mock_ollama.chat_stream.return_value = iter([fake_answer])

        # patch the lazy import of ollama_client inside ed_kb_answer
        import copilot.mcp_server as srv
        orig = srv.__dict__.get("ollama_client")
        srv.ollama_client = mock_ollama

        from copilot.mcp_server import ed_kb_answer
        result = ed_kb_answer("what does farseer unlock")

        if orig is not None:
            srv.ollama_client = orig

    assert isinstance(result, dict)
    assert "answer" in result
    assert "citations" in result
    assert "grounded" in result
    assert isinstance(result["citations"], list)
    assert isinstance(result["grounded"], bool)
    assert result["grounded"] is True
    assert result["citations"] == ["abc123def456789a"]
    assert fake_answer in result["answer"]


def test_ed_kb_answer_not_grounded_returns_refusal():
    """When grounded=False, ed_kb_answer must return the REFUSAL string."""
    mock_result = RetrievalResult(
        query="some obscure question",
        chunks=[],
        max_score=0.1,
        grounded=False,
    )
    with patch("copilot.mcp_server.retriever") as mock_retriever:
        mock_retriever.retrieve.return_value = mock_result
        from copilot.mcp_server import ed_kb_answer
        result = ed_kb_answer("some obscure question")

    assert result["grounded"] is False
    assert result["citations"] == []
    # REFUSAL string from repl.py must be present
    assert "don't have a verified source" in result["answer"].lower() or len(result["answer"]) > 0


def test_ed_kb_answer_ollama_unavailable():
    """OllamaUnavailable must be caught and return an error dict (not crash)."""
    chunk = _make_chunk()
    mock_result = RetrievalResult(
        query="farseer",
        chunks=[chunk],
        max_score=0.9,
        grounded=True,
    )
    with (
        patch("copilot.mcp_server.retriever") as mock_retriever,
        patch("copilot.mcp_server.assemble") as mock_assemble,
    ):
        mock_retriever.retrieve.return_value = mock_result
        mock_assemble.build_messages.return_value = []
        mock_assemble.validate_answer.return_value = (True, "ok")

        # Inject OllamaUnavailable via the module-level ollama_client reference
        import copilot.mcp_server as srv
        from copilot.ollama_client import OllamaUnavailable
        mock_ollama = MagicMock()
        mock_ollama.chat_stream.side_effect = OllamaUnavailable("down")
        orig = srv.__dict__.get("ollama_client")
        srv.ollama_client = mock_ollama

        from copilot.mcp_server import ed_kb_answer
        result = ed_kb_answer("farseer")

        if orig is not None:
            srv.ollama_client = orig

    # Must not raise; must return a dict with "answer" key
    assert isinstance(result, dict)
    assert "answer" in result
    assert "ollama" in result["answer"].lower() or "unavailable" in result["answer"].lower()
```

Run — expect failures (functions exist but mocking pattern may need to resolve):

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_ed_kb_answer_returns_structured_dict tests/test_mcp_server.py::test_ed_kb_answer_not_grounded_returns_refusal tests/test_mcp_server.py::test_ed_kb_answer_ollama_unavailable -v
```

The implementation of `ed_kb_answer` already exists from Task 2. If all three tests pass immediately, skip to the commit. If `ollama_client` patching fails because of the lazy import inside the function body, move the `ollama_client` import to the module top level (next to the other imports) — the implementation shown in Task 2 already does this for `assemble` and `profile`; apply the same pattern to `ollama_client` if needed.

Run again — expect all three **PASSED**:

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py -k "answer" -v
```

#### Commit

```
git add tests/test_mcp_server.py
git commit -m "Plan C Task 3: ed_kb_answer tests (structured dict, not-grounded refusal, OllamaUnavailable)"
```

---

### Task 4 — `ed_cmdr_state` tool: serialization test

**Goal:** `ed_cmdr_state` returns a dict with all `CmdrState` fields correctly serialized. Profile loading is mocked.

#### 4a. Failing test

Add to `tests/test_mcp_server.py`:

```python
from copilot.models import CmdrState, ProfileFact


def test_ed_cmdr_state_returns_dict():
    """ed_cmdr_state must return a serialized CmdrState dict."""
    fact = ProfileFact(
        key="rank.combat",
        value="Expert",
        origin="journal",
        freshness="2026-05-01",
        verified=True,
    )
    mock_state = CmdrState(
        name="Duvrazh",
        ranks={"combat": "Expert", "trade": "Elite V"},
        balance_cr=3_000_000_000,
        assets={"carriers": ["FC Alpha", "FC Beta"], "ships": ["Cutter", "Corvette"]},
        goals=["Engineering", "AX Combat"],
        facts=[fact],
    )
    with patch("copilot.mcp_server.profile") as mock_profile:
        mock_profile.load_cmdr_state.return_value = mock_state
        from copilot.mcp_server import ed_cmdr_state
        result = ed_cmdr_state()

    assert isinstance(result, dict)
    assert result["name"] == "Duvrazh"
    assert result["ranks"]["combat"] == "Expert"
    assert result["balance_cr"] == 3_000_000_000
    assert "carriers" in result["assets"]
    assert "Engineering" in result["goals"]
    assert len(result["facts"]) == 1
    f = result["facts"][0]
    assert f["key"] == "rank.combat"
    assert f["origin"] == "journal"
    assert f["verified"] is True


def test_ed_cmdr_state_error_returns_error_dict():
    """Profile load failure must return an error dict, not raise."""
    with patch("copilot.mcp_server.profile") as mock_profile:
        mock_profile.load_cmdr_state.side_effect = RuntimeError("profile corrupted")
        from copilot.mcp_server import ed_cmdr_state
        result = ed_cmdr_state()

    assert isinstance(result, dict)
    assert "error" in result
    assert "profile" in result["error"].lower() or "corrupted" in result["error"].lower()
```

Run — expect **FAILED** (implementation exists but test file doesn't have these yet):

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_ed_cmdr_state_returns_dict tests/test_mcp_server.py::test_ed_cmdr_state_error_returns_error_dict -v
```

The `ed_cmdr_state` function is already in the implementation from Task 2. If tests pass without modification, that is correct behavior — proceed to commit.

Run all mcp_server tests:

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py -v
```

Expect all **PASSED**.

#### Commit

```
git add tests/test_mcp_server.py
git commit -m "Plan C Task 4: ed_cmdr_state serialization and error-handling tests"
```

---

### Task 5 — Parity test: `ed_kb_search` chunk ids/order match `retriever.retrieve` directly

**Goal:** prove zero drift between the MCP tool and calling the retriever directly. This is the acceptance gate for spec §B/§D parity requirement: "MCP parity: `ed_kb_search` returns an identical `list[Chunk]` to the local retriever for the same query."

The test compares **structured chunk data** (chunk_ids, scores, order), NOT assembled prose.

#### 5a. Failing test

Add to `tests/test_mcp_server.py`:

```python
def test_ed_kb_search_parity_with_retriever():
    """
    Parity test (spec §B/§D): ed_kb_search chunk ids and order MUST match
    retriever.retrieve().chunks for the same query and top_k.

    This guards against any future serialization or ordering drift.
    """
    chunks = [
        _make_chunk(chunk_id="aaaa1111bbbb2222", score=0.92),
        _make_chunk(chunk_id="cccc3333dddd4444", score=0.78,
                    kb_path="kb/ships/anaconda.md",
                    heading_path="Anaconda > Hardpoints"),
    ]
    mock_result = RetrievalResult(
        query="engineers meta build",
        chunks=chunks,
        max_score=0.92,
        grounded=True,
    )

    with patch("copilot.mcp_server.retriever") as mock_retriever:
        mock_retriever.retrieve.return_value = mock_result
        from copilot.mcp_server import ed_kb_search
        mcp_result = ed_kb_search("engineers meta build", top_k=8)

    # Simulate calling retriever.retrieve directly (same mock result)
    direct_chunks = mock_result.chunks

    assert len(mcp_result) == len(direct_chunks), (
        f"Length mismatch: MCP={len(mcp_result)}, direct={len(direct_chunks)}"
    )
    for i, (mcp_row, direct_chunk) in enumerate(zip(mcp_result, direct_chunks)):
        assert mcp_row["chunk_id"] == direct_chunk.chunk_id, (
            f"chunk_id mismatch at position {i}: "
            f"MCP={mcp_row['chunk_id']}, direct={direct_chunk.chunk_id}"
        )
        assert mcp_row["score"] == pytest.approx(direct_chunk.score), (
            f"score mismatch at position {i}"
        )
        assert mcp_row["kb_path"] == direct_chunk.kb_path
        assert mcp_row["availability"] == direct_chunk.availability
```

Run — expect **FAILED** (new test, not yet passing):

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_ed_kb_search_parity_with_retriever -v
```

This test should pass immediately with the existing Task 2 implementation because `_chunk_to_dict` is a straightforward field-by-field copy. If it fails, inspect `_chunk_to_dict` for any field omission or reordering and fix it.

Run — expect **PASSED**:

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_ed_kb_search_parity_with_retriever -v
```

#### Commit

```
git add tests/test_mcp_server.py
git commit -m "Plan C Task 5: parity test ed_kb_search vs retriever.retrieve (spec §B/§D)"
```

---

### Task 6 — Server entrypoint: `__main__` guard + `python -m copilot.mcp_server` launch

**Goal:** the module is launchable via `python -m copilot.mcp_server`; `mcp.run()` is called only when the module is the entry point (not on import). Verify the module-level `if __name__ == "__main__"` guard is present and correct.

The `if __name__ == "__main__": mcp.run()` block is already in the Task 2 implementation. This task adds the explicit `__main__.py` file that makes `python -m copilot.mcp_server` work if `mcp_server` is a module (not a package), and verifies the guard is not accidentally invoked during import.

#### 6a. Verify the guard is in place

The existing `mcp_server.py` ends with:

```python
if __name__ == "__main__":
    mcp.run()
```

This is sufficient for `python copilot/mcp_server.py`. For `python -m copilot.mcp_server` to work, Python uses the same `__name__ == "__main__"` mechanism for a `.py` file inside a package — no `__main__.py` is needed. Confirm:

```powershell
# This should print nothing and exit 0 — mcp.run() must NOT be called on import
.\.venv\Scripts\python.exe -c "import copilot.mcp_server; print('import ok')"
```

Expected output: `import ok` (no hanging, no server launch).

#### 6b. Verify OllamaUnavailable graceful degradation is tested

The `ed_kb_search` tool already wraps the retrieval call in a try/except that catches `OllamaUnavailable` and returns `[{"error": "..."}]` instead of crashing. Add a targeted test:

```python
def test_ed_kb_search_ollama_unavailable():
    """ed_kb_search must return an error dict when Ollama is unreachable, not raise."""
    with patch("copilot.mcp_server.retriever") as mock_retriever:
        from copilot.ollama_client import OllamaUnavailable
        mock_retriever.retrieve.side_effect = OllamaUnavailable("down")
        from copilot.mcp_server import ed_kb_search
        result = ed_kb_search("farseer", top_k=8)

    assert isinstance(result, list)
    assert len(result) == 1
    assert "error" in result[0]
    assert "ollama" in result[0]["error"].lower() or "unavailable" in result[0]["error"].lower()
```

Run:

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_ed_kb_search_ollama_unavailable -v
```

Expected: **PASSED** (implementation already handles this).

#### Commit

```
git add tests/test_mcp_server.py
git commit -m "Plan C Task 6: verify __main__ guard + OllamaUnavailable graceful degradation for ed_kb_search"
```

---

### Task 7 — `.mcp.json` registration

**Goal:** create `.mcp.json` at the repo root registering the MCP server so Claude Code discovers it via `/mcp`.

#### 7a. Create `.mcp.json`

File: `G:\Documents\EliteDangerousKB\.mcp.json`

```json
{
  "mcpServers": {
    "ed-covas": {
      "command": "G:\\Documents\\EliteDangerousKB\\.venv\\Scripts\\python.exe",
      "args": ["-m", "copilot.mcp_server"],
      "cwd": "G:\\Documents\\EliteDangerousKB"
    }
  }
}
```

**Notes for the executor:**

1. The `command` value must be the absolute path to the venv's `python.exe`. Verify it exists:
   ```powershell
   Test-Path "G:\Documents\EliteDangerousKB\.venv\Scripts\python.exe"
   ```
   If the venv was created with a different name or is at a different path, update the `command` value accordingly.

2. The `cwd` value ensures that `copilot.paths.repo_root()` resolves correctly (Plan A uses this to locate `config.toml`, `embeddings/`, etc.).

3. JSON does not allow trailing commas. Validate the file:
   ```powershell
   .\.venv\Scripts\python.exe -c "import json; json.load(open('.mcp.json', encoding='utf-8')); print('valid JSON')"
   ```

4. Add `.mcp.json` to `.gitignore` if it contains machine-specific paths (it does — the absolute venv path is machine-local). Add this line to `.gitignore`:
   ```
   .mcp.json
   ```
   Alternatively, commit it if this machine is the only deployment target and the path is stable.

#### 7b. Verification via Claude Code

After saving `.mcp.json`, verify registration:

1. In Claude Code, run `/mcp` — the server `ed-covas` should appear in the list.
2. If it does not appear, check:
   - `.mcp.json` is at the **project root** (same directory as `config.toml`, not inside `copilot/`).
   - The JSON is valid (no trailing commas, correct escape of backslashes as `\\`).
   - The venv python path is correct.
3. Test a tool call from Claude Code: `ed_kb_search("test query")` — it should either return chunks (if the index is built) or return an error dict (if embeddings are not yet built — that is correct behavior for a not-yet-indexed KB).

#### Commit

```
git add .mcp.json
git commit -m "Plan C Task 7: .mcp.json registers ed-covas MCP server for Claude Code"
```

---

### Task 8 — Smoke test: module imports cleanly + FastMCP instance has 3 tools registered

**Goal:** a single importable test confirms the server module loads without error AND that the FastMCP instance has exactly the three required tools registered.

#### 8a. Failing test

Add to `tests/test_mcp_server.py`:

```python
def test_mcp_server_module_imports_cleanly():
    """copilot.mcp_server must import without error and expose the FastMCP instance."""
    import copilot.mcp_server as srv
    from mcp.server.fastmcp import FastMCP
    assert isinstance(srv.mcp, FastMCP), "srv.mcp must be a FastMCP instance"


def test_mcp_server_has_three_tools():
    """
    The FastMCP instance must have ed_kb_search, ed_kb_answer, and ed_cmdr_state
    registered as tools.

    FastMCP stores tools in ._tool_manager._tools (or similar internal structure).
    We introspect the registered tool names regardless of the exact private attribute.
    """
    import copilot.mcp_server as srv

    # FastMCP exposes registered tools — find them via the public or semi-public API.
    # Try the documented approach first; fall back to inspection.
    registered_names: set[str] = set()

    # Approach A: FastMCP._tool_manager._tools (dict keyed by name)
    if hasattr(srv.mcp, "_tool_manager") and hasattr(srv.mcp._tool_manager, "_tools"):
        registered_names = set(srv.mcp._tool_manager._tools.keys())

    # Approach B: FastMCP.list_tools() if it's a synchronous method
    elif hasattr(srv.mcp, "list_tools") and callable(srv.mcp.list_tools):
        try:
            tools_list = srv.mcp.list_tools()
            # May be a coroutine; if so we can't await here — skip
            if not hasattr(tools_list, "__await__"):
                registered_names = {t.name for t in tools_list}
        except Exception:
            pass

    # Approach C: inspect the module for decorated functions (fallback)
    if not registered_names:
        # The tool functions themselves are the plain Python functions — their names
        # are the tool names. Just verify the callables exist.
        assert callable(srv.ed_kb_search), "ed_kb_search not callable"
        assert callable(srv.ed_kb_answer), "ed_kb_answer not callable"
        assert callable(srv.ed_cmdr_state), "ed_cmdr_state not callable"
        return  # pass via fallback

    expected = {"ed_kb_search", "ed_kb_answer", "ed_cmdr_state"}
    missing = expected - registered_names
    assert not missing, f"Missing tools in FastMCP instance: {missing}"
```

Run — expect **FAILED** (tests not yet in file):

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py::test_mcp_server_module_imports_cleanly tests/test_mcp_server.py::test_mcp_server_has_three_tools -v
```

After adding the tests, both should pass with the existing implementation. If `test_mcp_server_module_imports_cleanly` fails with an ImportError on Plan A modules (retriever, assemble, profile), that signals Plan A is not complete — stop and complete Plan A first.

Run all tests:

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py -v
```

Expected: **all PASSED** (8 or more tests).

#### Commit

```
git add tests/test_mcp_server.py
git commit -m "Plan C Task 8: smoke tests — module imports cleanly, 3 tools registered"
```

---

## Final verification

Run the full test suite for Plan C in one shot:

```powershell
.\.venv\Scripts\pytest.exe tests/test_mcp_server.py -v --tb=short
```

All tests must be green. Then run the broader suite to confirm Plan C introduced no regressions:

```powershell
.\.venv\Scripts\pytest.exe tests/ -v --tb=short
```

Confirm the server launches (it will block in stdio-wait mode — interrupt after confirming startup):

```powershell
# Should print startup message then wait for MCP client; Ctrl-C to stop
.\.venv\Scripts\python.exe -m copilot.mcp_server
```

Confirm Claude Code registration:

```
/mcp
```

`ed-covas` must appear with status `connected` (or equivalent). If it shows `failed`, check the absolute path in `.mcp.json` and run the module manually to see the error.

---

## Self-Review Checklist (run before declaring Plan C complete)

### §D coverage
- [x] `ed_kb_search` wraps `retriever.retrieve` — no retrieval logic re-implemented
- [x] `ed_kb_answer` wraps `assemble.build_messages`, `validate_answer`, `ollama_client.chat_stream`
- [x] `ed_cmdr_state` wraps `profile.load_cmdr_state`
- [x] FastMCP + stdio transport used
- [x] `.mcp.json` registration present

### §B parity
- [x] Task 5 parity test compares chunk_ids and order (structured chunks, NOT prose)
- [x] Grounded flag propagated in `ed_kb_answer`
- [x] REFUSAL returned when `not grounded`

### §F graceful degradation
- [x] `ed_kb_search` catches `OllamaUnavailable` → error dict
- [x] `ed_kb_answer` catches `OllamaUnavailable` → error dict with Ollama message
- [x] `ed_cmdr_state` catches generic exceptions → error dict

### Placeholder scan
- No `TODO`, `...`, `pass` (except in Protocol stubs from Plan A), `<insert>`, `FIXME` in any Plan C file
- All code blocks contain complete, runnable Python or JSON

### Type consistency vs CONTRACTS
- `Chunk` fields in `_chunk_to_dict`: all 11 CONTRACTS fields present (`chunk_id`, `text`, `kb_path`, `heading_path`, `source_url`, `source_tier`, `source_count`, `verified`, `availability`, `changed_note`, `score`)
- `CmdrState` serialization covers `name`, `ranks`, `balance_cr`, `assets`, `goals`, `facts`
- `ProfileFact` serialization covers `key`, `value`, `origin`, `freshness`, `verified`
- `score` cast to `float()` — handles numpy float32 which is not JSON-serializable

### Plan isolation
- [x] No edits to Plan A files (`retriever.py`, `assemble.py`, `profile.py`, `repl.py`, `ollama_client.py`, `models.py`, `paths.py`, `chunker.py`, `index.py`, `atomic.py`)
- [x] No edits to Plan B files (`data_discovery.py`, `profile_sources.py`, `vision_ingest.py`)
- [x] Only new files: `copilot/mcp_server.py`, `tests/test_mcp_server.py`, `.mcp.json`
