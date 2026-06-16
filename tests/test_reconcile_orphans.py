"""
F2 tests for scripts/reconcile_loop13_orphans.py.

Pins every MC the spec calls out:
  MC-2  orphan keys are the FULL sha256 of the URLs, computed at runtime.
  MC-3  a fixture repo_root keeps the LIVE STATE.toml provably untouched.
  MC-4  queue prepend lands above the first bullet, not appended at the end.
  MC-5  each step is independently guarded; a step-a failure still runs b-d.
  MC-7  derived paths are containment-validated; ../ escapes are rejected.
  MC-10 seen.json / STATE.toml are written via copilot.atomic, never raw open().
Plus exactness + idempotency + dry_run.
"""
import ast
import importlib.util
import json
import sys
import tomllib
from pathlib import Path

import pytest

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent / "scripts" / "reconcile_loop13_orphans.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "reconcile_loop13_orphans", _SCRIPT_PATH
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


recon = _load_module()


# ---------------------------------------------------------------------------
# Fixture: a synthetic repo with orphan keys + non-orphan keys + scratch files.
# ---------------------------------------------------------------------------

def _make_fixture(tmp_path: Path, *, phase: str = "summarize",
                  queue_first_line_bullet: bool = False,
                  consumed_targets: bool = False) -> Path:
    root = tmp_path / "repo"
    (root / "indexes").mkdir(parents=True)
    (root / "sources").mkdir(parents=True)
    (root / "summaries").mkdir(parents=True)
    (root / "queue").mkdir(parents=True)

    # seen.json: 3 orphan keys (derived from the real URLs) + 2 preserved keys.
    orphan_keys = list(recon._orphan_keys().keys())
    assert len(orphan_keys) == 3
    seen = {}
    for k in orphan_keys:
        seen[k] = {"first_seen": "2026-06-13T00:00:00+00:00", "content_sha256": "orphan"}
    # Non-orphan entries that MUST survive byte-for-byte.
    seen["preserved_alpha"] = {"first_seen": "2026-06-01T00:00:00+00:00",
                               "content_sha256": "keepme", "extra": [1, 2, 3]}
    seen["preserved_beta"] = {"first_seen": "2026-06-02T00:00:00+00:00",
                              "content_sha256": "alsokeep"}
    (root / "indexes" / "seen.json").write_text(
        json.dumps(seen, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Orphan scratch files (and one decoy that must NOT be deleted).
    for t in recon.ORPHAN_TARGETS:
        (root / "sources" / f"{t['sha8']}-{t['slug']}.raw").write_text("raw", encoding="utf-8")
        (root / "summaries" / f"{t['sha8']}-{t['slug']}.md").write_text("md", encoding="utf-8")
    (root / "sources" / "deadbeef-keepme.raw").write_text("decoy", encoding="utf-8")

    # STATE.toml
    (root / "STATE.toml").write_text(
        f'loop_number = 13\nlast_completed_phase = "{phase}"\nmode = "search"\n',
        encoding="utf-8",
    )

    # queue/next-targets.md
    if queue_first_line_bullet:
        # First *content* line is a bullet (MC-4 stress case).
        lines = ["- https://example.com/existing-top (tier: 0)"]
        if not consumed_targets:
            for t in recon.ORPHAN_TARGETS:
                lines.append(f"- {t['url']} (already here)")
        text = "\n".join(lines) + "\n"
    else:
        lines = ["# Research Queue — next targets", ""]
        if not consumed_targets:
            for t in recon.ORPHAN_TARGETS:
                lines.append(f"- {t['url']} (already here)")
        else:
            lines.append("- https://example.com/other (tier: 0)")
        text = "\n".join(lines) + "\n"
    (root / "queue" / "next-targets.md").write_text(text, encoding="utf-8")

    return root


# ===========================================================================
# MC-2 + exactness: exactly the 3 orphan keys removed, others preserved.
# ===========================================================================

def test_removes_exactly_three_orphan_keys_and_preserves_rest(tmp_path):
    root = _make_fixture(tmp_path)
    before = json.loads((root / "indexes" / "seen.json").read_text(encoding="utf-8"))

    summary = recon.reconcile(repo_root=root)

    assert set(summary["keys_removed"]) == {"scb", "mrp", "mahr"}
    assert summary["errors"] == []

    after = json.loads((root / "indexes" / "seen.json").read_text(encoding="utf-8"))
    # Orphan keys gone.
    for k in recon._orphan_keys():
        assert k not in after
    # Preserved keys byte-for-byte (value dicts identical).
    assert after["preserved_alpha"] == before["preserved_alpha"]
    assert after["preserved_beta"] == before["preserved_beta"]
    assert set(after.keys()) == {"preserved_alpha", "preserved_beta"}


def test_orphan_keys_are_full_sha256_not_sha8(tmp_path):
    """MC-2: the seen.json keys are the full 64-hex digests, not the sha8 prefix."""
    keys = list(recon._orphan_keys().keys())
    assert all(len(k) == 64 for k in keys), "orphan keys must be full sha256 hexdigests"
    # The sha8 prefixes are filename prefixes, and each key starts with its prefix.
    by_slug = {slug: key for key, slug in recon._orphan_keys().items()}
    for t in recon.ORPHAN_TARGETS:
        assert by_slug[t["slug"]].startswith(t["sha8"])


# ===========================================================================
# Files + state + queue happy path.
# ===========================================================================

def test_deletes_orphan_scratch_files_keeps_decoy(tmp_path):
    root = _make_fixture(tmp_path)
    summary = recon.reconcile(repo_root=root)

    assert len(summary["files_deleted"]) == 6  # 3 raw + 3 md
    for t in recon.ORPHAN_TARGETS:
        assert not (root / "sources" / f"{t['sha8']}-{t['slug']}.raw").exists()
        assert not (root / "summaries" / f"{t['sha8']}-{t['slug']}.md").exists()
    # Decoy untouched.
    assert (root / "sources" / "deadbeef-keepme.raw").exists()


def test_state_reset_summarize_to_commit(tmp_path):
    root = _make_fixture(tmp_path, phase="summarize")
    summary = recon.reconcile(repo_root=root)
    assert summary["state_reset"] is True
    state = tomllib.loads((root / "STATE.toml").read_text(encoding="utf-8"))
    assert state["last_completed_phase"] == "commit"


def test_state_left_alone_when_not_summarize(tmp_path):
    root = _make_fixture(tmp_path, phase="index")
    summary = recon.reconcile(repo_root=root)
    assert summary["state_reset"] is False
    state = tomllib.loads((root / "STATE.toml").read_text(encoding="utf-8"))
    assert state["last_completed_phase"] == "index"


# ===========================================================================
# MC-4: queue prepend lands above the first bullet, not at the end.
# ===========================================================================

def test_queue_prepend_above_first_bullet(tmp_path):
    root = _make_fixture(tmp_path, queue_first_line_bullet=True, consumed_targets=True)
    summary = recon.reconcile(repo_root=root)

    assert set(summary["queue_appended"]) == {"scb", "mrp", "mahr"}
    lines = (root / "queue" / "next-targets.md").read_text(encoding="utf-8").splitlines()
    bullets = [ln for ln in lines if ln.startswith("- ")]

    # The 3 re-seeded targets must appear BEFORE the pre-existing top bullet,
    # not appended after it (the insert==0 misfire the spec warns about).
    existing_idx = next(i for i, ln in enumerate(bullets) if "existing-top" in ln)
    for t in recon.ORPHAN_TARGETS:
        target_idx = next(i for i, ln in enumerate(bullets) if t["url"] in ln)
        assert target_idx < existing_idx, (
            f"{t['slug']} re-seeded AFTER the existing bullet — insert misfired"
        )


def test_queue_noop_when_targets_already_present(tmp_path):
    root = _make_fixture(tmp_path, consumed_targets=False)
    before = (root / "queue" / "next-targets.md").read_text(encoding="utf-8")
    summary = recon.reconcile(repo_root=root)
    assert summary["queue_appended"] == []
    after = (root / "queue" / "next-targets.md").read_text(encoding="utf-8")
    assert before == after  # untouched


# ===========================================================================
# Idempotency: a second run is a clean no-op.
# ===========================================================================

def test_idempotent_second_run(tmp_path):
    root = _make_fixture(tmp_path)
    recon.reconcile(repo_root=root)
    seen_after_first = (root / "indexes" / "seen.json").read_text(encoding="utf-8")
    state_after_first = (root / "STATE.toml").read_text(encoding="utf-8")
    queue_after_first = (root / "queue" / "next-targets.md").read_text(encoding="utf-8")

    second = recon.reconcile(repo_root=root)
    assert second["keys_removed"] == []
    assert second["files_deleted"] == []
    assert second["state_reset"] is False
    assert second["queue_appended"] == []
    assert second["errors"] == []
    # Files unchanged by the second run.
    assert (root / "indexes" / "seen.json").read_text(encoding="utf-8") == seen_after_first
    assert (root / "STATE.toml").read_text(encoding="utf-8") == state_after_first
    assert (root / "queue" / "next-targets.md").read_text(encoding="utf-8") == queue_after_first


# ===========================================================================
# dry_run: same summary, no writes.
# ===========================================================================

def test_dry_run_writes_nothing(tmp_path):
    root = _make_fixture(tmp_path)
    seen_before = (root / "indexes" / "seen.json").read_text(encoding="utf-8")
    state_before = (root / "STATE.toml").read_text(encoding="utf-8")
    queue_before = (root / "queue" / "next-targets.md").read_text(encoding="utf-8")
    files_before = sorted(p.name for p in (root / "sources").iterdir())

    summary = recon.reconcile(repo_root=root, dry_run=True)

    # Summary still reports what WOULD happen.
    assert set(summary["keys_removed"]) == {"scb", "mrp", "mahr"}
    assert len(summary["files_deleted"]) == 6
    assert summary["state_reset"] is True

    # Nothing on disk changed.
    assert (root / "indexes" / "seen.json").read_text(encoding="utf-8") == seen_before
    assert (root / "STATE.toml").read_text(encoding="utf-8") == state_before
    assert (root / "queue" / "next-targets.md").read_text(encoding="utf-8") == queue_before
    assert sorted(p.name for p in (root / "sources").iterdir()) == files_before


# ===========================================================================
# MC-3: a fixture repo_root keeps the LIVE STATE.toml provably untouched.
# ===========================================================================

def test_live_state_untouched_with_fixture_root(tmp_path, monkeypatch):
    from copilot.paths import repo_root as live_repo_root
    live_state = live_repo_root() / "STATE.toml"
    live_before = live_state.read_text(encoding="utf-8") if live_state.exists() else None

    # If copilot.paths.repo_root were ever consulted, point it at a SENTINEL dir
    # that has no STATE.toml — so a stray write would fail loudly, not silently
    # hit the live tree.
    sentinel = tmp_path / "sentinel"
    sentinel.mkdir()
    monkeypatch.setattr("copilot.paths.repo_root", lambda: sentinel)

    root = _make_fixture(tmp_path, phase="summarize")
    summary = recon.reconcile(repo_root=root)
    assert summary["state_reset"] is True
    # Fixture state was written...
    assert tomllib.loads((root / "STATE.toml").read_text(encoding="utf-8"))[
        "last_completed_phase"
    ] == "commit"
    # ...and the live STATE.toml is byte-identical.
    if live_before is not None:
        assert live_state.read_text(encoding="utf-8") == live_before


# ===========================================================================
# MC-5: each step independently guarded — a step-a failure still runs b/c/d.
# ===========================================================================

def test_step_a_failure_does_not_skip_other_steps(tmp_path, monkeypatch):
    root = _make_fixture(tmp_path, phase="summarize")

    # Inject a failure into step (a) only.
    def _boom(*a, **k):
        raise TimeoutError("simulated lock timeout in step a")

    monkeypatch.setattr(recon, "_step_seen", _boom)

    summary = recon.reconcile(repo_root=root)

    # The error is observable...
    assert any("step-a" in e for e in summary["errors"]), summary["errors"]
    assert summary["keys_removed"] == []  # step a never produced a result
    # ...but b/c/d still ran.
    assert len(summary["files_deleted"]) == 6
    assert summary["state_reset"] is True
    state = tomllib.loads((root / "STATE.toml").read_text(encoding="utf-8"))
    assert state["last_completed_phase"] == "commit"


def test_cli_returns_nonzero_on_error(tmp_path, monkeypatch):
    root = _make_fixture(tmp_path, phase="summarize")
    monkeypatch.setattr("copilot.paths.repo_root", lambda: root)

    def _boom(*a, **k):
        raise OSError("simulated")
    monkeypatch.setattr(recon, "_step_files", _boom)

    rc = recon.main([])
    assert rc != 0


# ===========================================================================
# MC-7: derived paths are containment-validated; ../ escapes rejected.
# ===========================================================================

def test_contained_rejects_traversal(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    # A legit join stays inside.
    assert recon._contained(root, "indexes", "seen.json").is_relative_to(root)
    # A ../ escape is rejected.
    with pytest.raises(ValueError):
        recon._contained(root, "..", "evil.txt")
    with pytest.raises(ValueError):
        recon._contained(root, "indexes", "..", "..", "evil.txt")


def test_containment_failure_recorded_not_crashed(tmp_path, monkeypatch):
    """If a step derives an escaping path, the error is recorded in errors[],
    the run does not crash, and no other step is skipped."""
    root = _make_fixture(tmp_path, phase="summarize")

    # Force step-b to derive an escaping path via a poisoned ORPHAN_TARGETS sha8.
    original = recon.ORPHAN_TARGETS

    def restore():
        recon.ORPHAN_TARGETS = original

    # Monkeypatch _step_files to attempt an escaping containment join.
    def _escaping(repo_root, *, dry_run):
        recon._contained(repo_root, "..", "escape")  # raises ValueError
        return []

    monkeypatch.setattr(recon, "_step_files", _escaping)
    summary = recon.reconcile(repo_root=root)
    assert any("step-b" in e for e in summary["errors"])
    # step c still ran.
    assert summary["state_reset"] is True


# ===========================================================================
# MC-10: no raw open()-write of seen.json / STATE.toml in the script.
# ===========================================================================

def test_no_raw_write_of_seen_or_state(tmp_path):
    """Static check: the script never does open(...).write of seen.json/STATE.toml.

    All such writes must go through copilot.atomic. We assert the script imports
    write_json_atomic and write_atomic, and that there is no `open(` call whose
    enclosing source line writes those targets. Conservative: we forbid any
    open(..., 'w') / open(..., 'a') in the script entirely (it has no legitimate
    need for raw writes — reads use Path.read_text / tomllib.load).
    """
    src = _SCRIPT_PATH.read_text(encoding="utf-8")
    tree = ast.parse(src)

    # 1. The atomic helpers ARE imported.
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "copilot.atomic":
            imported |= {a.name for a in node.names}
    assert {"write_atomic", "write_json_atomic"} <= imported

    # 2. No open() call with a write/append mode anywhere in the script.
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
            mode = ""
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                mode = str(node.args[1].value)
            for kw in node.keywords:
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                    mode = str(kw.value.value)
            if "w" in mode or "a" in mode or "+" in mode:
                offenders.append(f"line {node.lineno}: open(..., {mode!r})")
    assert not offenders, "raw write-mode open() in reconcile script:\n" + "\n".join(offenders)
