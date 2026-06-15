"""Portability guard — the repo must run from ANY clone path.

No runtime-relevant tracked file may hardcode an absolute filesystem path, and
the path helpers must resolve dynamically from repo_root(). This is the executable
enforcement of the clone-anywhere rule (item 1).
"""
import re
from pathlib import Path

import pytest

from copilot.paths import repo_root, kb_dir, embeddings_dir, indexes_dir

ROOT = repo_root()

# Files whose contents execute / configure the running system. Dated plan docs
# under docs/ are historical snapshots, not runtime artifacts, so they are excluded.
RUNTIME_GLOBS = [
    "copilot/**/*.py",
    "*.ps1",
    "*.toml",
    "*.json",          # .mcp.json and any config json at root
    "ed-research-prompt.md",
    "requirements.txt",
    "pytest.ini",
]

# A Windows drive-letter absolute path (C:\ , G:\ ...) or a POSIX home path.
# ${CLAUDE_PROJECT_DIR:-.}\.venv is NOT matched (no drive letter precedes the backslash).
_ABS_PATH = re.compile(r"[A-Za-z]:\\|/home/|/Users/")


def _runtime_files():
    seen = set()
    for pat in RUNTIME_GLOBS:
        for p in ROOT.glob(pat):
            if p.is_file() and ".venv" not in p.parts and ".git" not in p.parts:
                seen.add(p)
    return sorted(seen)


def test_no_hardcoded_absolute_paths_in_runtime_files():
    offenders = []
    for p in _runtime_files():
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if _ABS_PATH.search(line):
                offenders.append(f"{p.relative_to(ROOT)}:{i}: {line.strip()}")
    assert not offenders, "Hardcoded absolute paths break clone-anywhere portability:\n" + "\n".join(offenders)


def test_repo_root_resolves_to_config_dir():
    assert (ROOT / "config.toml").is_file()
    # repo_root must be derived, not a constant: it is the parent of copilot/.
    assert (ROOT / "copilot" / "paths.py").is_file()


def test_path_helpers_resolve_under_root():
    for d in (kb_dir(), embeddings_dir(), indexes_dir()):
        assert d.is_absolute()
        assert str(d).startswith(str(ROOT))


def test_mcp_json_uses_portable_project_dir():
    import json
    mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    srv = mcp["mcpServers"]["ed-covas"]
    assert "${CLAUDE_PROJECT_DIR" in srv["command"], "MCP command must use ${CLAUDE_PROJECT_DIR} for portability"
    assert "${CLAUDE_PROJECT_DIR" in srv["cwd"], "MCP cwd must use ${CLAUDE_PROJECT_DIR} for portability"
