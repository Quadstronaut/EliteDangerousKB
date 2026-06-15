"""
tests/test_repl_meta_security.py — terminal-control sanitizer (security
follow-up to 8c0cf9f).

meta_command() text is printed verbatim to the local terminal. Two interpolated
values are UNTRUSTED: manifest kb_path (web-sourced via the research loop) and
CmdrState.name (file-supplied frontmatter). An ANSI CSI/OSC/ESC, NUL, C0/C1,
DEL, or lone-CR payload renders verbatim and can hijack the window title, clear
the screen, reposition the cursor, or spoof a line. sanitize_terminal_text()
strips those sequences; this module pins the function contract (AC-SAN-*) and
the repl wiring (AC-WIRE-*). All offline — no Ollama, no network.
"""

from __future__ import annotations

import json

import pytest

from copilot import paths
from copilot.models import CmdrState
from copilot.repl import meta_command
from copilot.sanitize import sanitize_terminal_text

ESC = "\x1b"
BEL = "\x07"
NUL = "\x00"
CR = "\x0d"
DEL = "\x7f"


# ---------------------------------------------------------------------------
# Manifest fixture plumbing (mirrors test_repl_meta.py)
# ---------------------------------------------------------------------------

def _write_manifest(tmp_path, manifest: dict) -> None:
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


@pytest.fixture
def indexes_tmp(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "indexes_dir", lambda: tmp_path)
    return tmp_path


def _manifest_two_pages() -> dict:
    """Clean kb_paths — identical shape to test_repl_meta._manifest_two_pages."""
    return {
        "aabbccdd11223344": {
            "content_hash": "h1",
            "kb_path": "kb/engineers/felicity-farseer.md",
            "heading_path": "Felicity Farseer > Unlock",
            "payload": {},
        },
        "eeff00112233aabb": {
            "content_hash": "h2",
            "kb_path": "kb/engineers/felicity-farseer.md",
            "heading_path": "Felicity Farseer > Location",
            "payload": {},
        },
        "1122334455667788": {
            "content_hash": "h3",
            "kb_path": "kb/systems/deciat.md",
            "heading_path": "Deciat > Overview",
            "payload": {},
        },
    }


# ===========================================================================
# AC-SAN-1: exists, importable, callable, str->str, deterministic.
# ===========================================================================

def test_ac_san_1_exists_pure():
    assert callable(sanitize_terminal_text)
    payloads = [
        "",
        "Duvrazh",
        "kb/locations/deciat.md",
        f"x{ESC}[2Jy{NUL}z{ESC}]0;t{BEL}w",
        f"line1\nline2\twith{CR}tab\x9bmore",
    ]
    for p in payloads:
        first = sanitize_terminal_text(p)
        assert isinstance(first, str)
        # determinism: same input -> equal output, and idempotent on its result
        assert sanitize_terminal_text(p) == first
        assert sanitize_terminal_text(first) == first


# ===========================================================================
# AC-SAN-2: clean identity — clean strings pass byte-for-byte.
# ===========================================================================

def test_ac_san_2_clean_identity():
    assert sanitize_terminal_text("kb/locations/deciat.md") == "kb/locations/deciat.md"
    assert sanitize_terminal_text("Duvrazh") == "Duvrazh"
    assert sanitize_terminal_text("") == ""
    multiline = "alpha\n\tbeta\n  - gamma\tdelta\n"
    assert sanitize_terminal_text(multiline) == multiline
    # ordinary Unicode >= U+00A0 survives (e.g. accented name, NBSP, em-dash)
    uni = "Sol — Achenar Björk"
    assert sanitize_terminal_text(uni) == uni


# ===========================================================================
# AC-SAN-3: OSC window-title (ESC ']0;pwned' BEL).
# ===========================================================================

def test_ac_san_3_osc_window_title():
    payload = f"before{ESC}]0;pwned{BEL}after"
    out = sanitize_terminal_text(payload)
    assert ESC not in out
    assert BEL not in out
    # the OSC body (incl. its 'pwned' arming string) is removed as a unit
    assert "pwned" not in out
    assert "before" in out and "after" in out


def test_ac_san_3_osc_st_terminated_and_unterminated():
    # ST-terminated OSC
    st = f"a{ESC}]2;title{ESC}\\b"
    out = sanitize_terminal_text(st)
    assert ESC not in out and "title" not in out
    assert "a" in out and "b" in out
    # unterminated OSC running to end-of-string is still removed
    unterminated = f"keep{ESC}]0;runaway-to-eos"
    out2 = sanitize_terminal_text(unterminated)
    assert ESC not in out2
    assert "runaway" not in out2
    assert out2 == "keep"


# ===========================================================================
# AC-SAN-4: CSI clear-screen (ESC '[2J').
# ===========================================================================

def test_ac_san_4_csi_clear_screen():
    payload = f"vis{ESC}[2Jible"
    out = sanitize_terminal_text(payload)
    assert ESC not in out
    assert "[2J" not in out
    assert "vis" in out and "ible" in out
    assert out == "visible"


# ===========================================================================
# AC-SAN-5: cursor reposition (ESC '[H', ESC '[12;40H').
# ===========================================================================

@pytest.mark.parametrize("seq", ["[H", "[12;40H", "[1;1H", "[2A", "[K"])
def test_ac_san_5_cursor_reposition(seq):
    payload = f"keep{ESC}{seq}text"
    out = sanitize_terminal_text(payload)
    assert ESC not in out
    assert seq not in out  # no leftover CSI body
    assert out == "keeptext"


# ===========================================================================
# AC-SAN-6: NUL / CR / C1 / DEL removed; \n and \t preserved.
# ===========================================================================

@pytest.mark.parametrize("ctrl", [NUL, CR, DEL, "\x9b", "\x80", "\x9f", "\x01", "\x08"])
def test_ac_san_6_control_points_removed(ctrl):
    payload = f"a{ctrl}b\n\tc"
    out = sanitize_terminal_text(payload)
    assert ctrl not in out
    # \n and \t in the same input are preserved
    assert "\n" in out and "\t" in out
    assert out == "ab\n\tc"


def test_ac_san_6_cr_dropped_no_overwrite_spoof():
    # lone CR enables line-overwrite spoofing: it must be dropped, not kept.
    payload = f"real output{CR}FAKE"
    out = sanitize_terminal_text(payload)
    assert CR not in out
    assert out == "real outputFAKE"


# ===========================================================================
# AC-WIRE-1: kb_path payload neutralised in topics output.
# ===========================================================================

def test_ac_wire_1_kb_path_payload_neutralised(indexes_tmp):
    # readable stem wrapped in OSC/CSI/NUL/CR payloads
    evil = f"kb/systems/{ESC}]0;X{BEL}dec{NUL}iat{CR}{ESC}[2J.md"
    manifest = {
        "deadbeef00000001": {
            "content_hash": "h",
            "kb_path": evil,
            "heading_path": "x",
            "payload": {},
        },
    }
    _write_manifest(indexes_tmp, manifest)
    out = meta_command("topics", CmdrState(name="Duvrazh"))
    assert out is not None
    for bad in (ESC, NUL, BEL, CR):
        assert bad not in out, f"residual control char {bad!r} in topics output"
    # the readable stem survives (the path segments between the payloads)
    assert "kb/systems/" in out
    assert "dec" in out and "iat" in out


# ===========================================================================
# AC-WIRE-2: name payload neutralised in help output.
# ===========================================================================

def test_ac_wire_2_name_payload_neutralised(indexes_tmp):
    name = f"Duv{ESC}]0;X{BEL}razh{ESC}[2J{NUL}{CR}"
    out = meta_command("help", CmdrState(name=name))
    assert out is not None
    for bad in (ESC, NUL, BEL, CR):
        assert bad not in out, f"residual control char {bad!r} in help output"
    # the readable portion of the name survives
    assert "Duv" in out and "razh" in out


# ===========================================================================
# AC-WIRE-3: content contract preserved with clean fixture.
# ===========================================================================

def test_ac_wire_3_content_contract_preserved(indexes_tmp):
    _write_manifest(indexes_tmp, _manifest_two_pages())
    out = meta_command("topics", CmdrState(name="Duvrazh"))
    assert out is not None
    assert "kb/systems/deciat.md" in out
    assert "kb/engineers/felicity-farseer.md" in out
    # true page count (2) and chunk count (3) substrings unchanged
    assert "2 page(s)" in out
    assert "3 indexed" in out


# ===========================================================================
# AC-WIRE-5: defense-in-depth no-op on clean static content.
# ===========================================================================

def test_ac_wire_5_outer_wrap_no_op_on_clean(indexes_tmp):
    _write_manifest(indexes_tmp, _manifest_two_pages())
    state = CmdrState(name="Duvrazh")

    # sources output is byte-identical after a second sanitize pass (idempotent,
    # no truncation/character loss on the static roster).
    sources = meta_command("sources", state)
    assert sources is not None
    assert sanitize_terminal_text(sources) == sources

    # help output for a clean state is likewise byte-identical under re-pass.
    help_out = meta_command("help", state)
    assert help_out is not None
    assert sanitize_terminal_text(help_out) == help_out
    # and the clean name is present verbatim (no character loss)
    assert "Duvrazh" in help_out
