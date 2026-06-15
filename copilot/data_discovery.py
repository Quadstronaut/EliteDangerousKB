"""
data_discovery.py — scan the machine for Elite Dangerous data files.

READ-ONLY: this module never writes into any game or tool folder.
Only output is indexes/data-sources.json via atomic.write_json_atomic.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from copilot import paths
from copilot.atomic import write_json_atomic

# Subdirectory under Saved Games that contains game-state JSON and journals.
_SAVED_GAMES_SUBPATH = Path("Saved Games") / "Frontier Developments" / "Elite Dangerous"

# 3rd-party tool dir names to scan for under LOCALAPPDATA / APPDATA.
_THIRD_PARTY_DIRS: dict[str, str] = {
    "EDMarketConnector": "edmc",
    "EDDiscovery": "eddiscovery",
    "EDEngineer": "edengineer",
    "Frontier Developments": "frontier-appdata",
}

# Screenshot sub-path under USERPROFILE/Pictures.
_SCREENSHOTS_SUBPATH = Path("Pictures") / "Frontier Developments" / "Elite Dangerous"


def saved_games_dir() -> Path | None:
    """Return the Elite Dangerous Saved Games dir if it exists, else None.

    Path: %USERPROFILE%\\Saved Games\\Frontier Developments\\Elite Dangerous
    """
    userprofile = os.environ.get("USERPROFILE", "")
    if not userprofile:
        return None
    candidate = Path(userprofile) / _SAVED_GAMES_SUBPATH
    return candidate if candidate.is_dir() else None


def _iso_mtime(path: Path) -> str:
    """Return ISO 8601 mtime for a path, or 'unknown' if stat fails."""
    try:
        mtime = path.stat().st_mtime
        return datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
    except OSError:
        return "unknown"


def _entry(path: Path, type_: str) -> dict:
    return {
        "path": str(path),
        "type": type_,
        "last_modified": _iso_mtime(path),
        "ingest_status": "pending",
    }


def _extra_scan_roots() -> list[Path]:
    """Filesystem roots to shallow-scan for ED/Frontier dirs.

    Portable: NO hardcoded drive letter. ED_KB_SCAN_ROOTS (os.pathsep-separated)
    overrides; otherwise enumerate existing local drive roots on Windows, or '/'
    on POSIX, so the scan adapts to whatever machine/clone this runs on.
    """
    env = os.environ.get("ED_KB_SCAN_ROOTS", "").strip()
    if env:
        return [Path(p) for p in env.split(os.pathsep) if p.strip()]
    roots: list[Path] = []
    if os.name == "nt":
        import string
        for letter in string.ascii_uppercase:
            d = Path(f"{letter}:\\")
            if d.exists():
                roots.append(d)
    else:
        roots.append(Path("/"))
    return roots


def discover_data_sources() -> list[dict]:
    """Scan the machine for ED-related data and write indexes/data-sources.json.

    Scans:
    - %USERPROFILE%/Saved Games/Frontier Developments/Elite Dangerous (game-state-json)
    - %LOCALAPPDATA% and %APPDATA% for Frontier/EDMC/EDDiscovery/EDEngineer dirs
    - %USERPROFILE%/Pictures/Frontier Developments/Elite Dangerous (screenshots)
    - extra filesystem roots (ED_KB_SCAN_ROOTS env, else auto-detected drive roots)

    Returns the manifest list (same data written to disk).
    READ-ONLY: never writes into any discovered game or tool folder.
    """
    manifest: list[dict] = []

    # 1. Saved Games game-state JSON dir.
    sg = saved_games_dir()
    if sg is not None:
        manifest.append(_entry(sg, "game-state-json"))

    # 2. LOCALAPPDATA + APPDATA — 3rd-party tools.
    for env_var in ("LOCALAPPDATA", "APPDATA"):
        base = os.environ.get(env_var, "")
        if not base:
            continue
        base_path = Path(base)
        for dir_name, type_label in _THIRD_PARTY_DIRS.items():
            candidate = base_path / dir_name
            if candidate.is_dir():
                manifest.append(_entry(candidate, type_label))

    # 3. Screenshots folder.
    userprofile = os.environ.get("USERPROFILE", "")
    if userprofile:
        screenshots = Path(userprofile) / _SCREENSHOTS_SUBPATH
        if screenshots.is_dir():
            manifest.append(_entry(screenshots, "screenshots"))

    # 4. Extra filesystem roots — Frontier / ED-named dirs. Portable: no hardcoded
    #    drive letter (ED_KB_SCAN_ROOTS env override, else auto-detected roots).
    for root in _extra_scan_roots():
        if not root.is_dir():
            continue
        try:
            for child in root.iterdir():
                if child.is_dir() and any(
                    kw in child.name.lower()
                    for kw in ("frontier", "elite", "dangerous", "edkb", "elitedangerous")
                ):
                    manifest.append(_entry(child, "ed-data-dir"))
        except (PermissionError, OSError):
            continue  # inaccessible root; skip.

    # 5. Deduplicate by resolved path string.
    seen_paths: set[str] = set()
    deduped: list[dict] = []
    for entry in manifest:
        key = str(Path(entry["path"]).resolve())
        if key not in seen_paths:
            seen_paths.add(key)
            deduped.append(entry)

    # 6. Write manifest atomically — only into indexes/, never into game dirs.
    out_path = paths.indexes_dir() / "data-sources.json"
    write_json_atomic(out_path, deduped)

    return deduped
