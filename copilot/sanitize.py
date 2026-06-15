"""Prompt-injection defense for untrusted retrieved content (item 5).

Retrieved KB/web chunk text is UNTRUSTED. The autonomous loop fetches the open web
into the KB, so an attacker could smuggle instructions into the model's context:
"ignore previous instructions...", fake role turns ("System:"), or chat control
tokens (<|im_start|>). This module:
  * defangs the structural tokens that could break prompt framing or fake a turn, and
  * provides random-nonce SPOTLIGHT fences so the model can tell data from
    instructions and an injection cannot forge the fence (it can't guess the nonce).

100% prevention is not provable against an LLM, so this is one of THREE layers:
  1. this structural sanitization + spotlighting,
  2. the hardened system prompt (instruction hierarchy — see assemble._UNTRUSTED_NOTICE),
  3. the citation + claim-grounding gate (assemble.validate_answer), so even a
     partially successful injection cannot produce an ungrounded/uncited answer.
"""
from __future__ import annotations

import re
import secrets

# Chat-template / control tokens that can break prompt structure across models.
_SPECIAL_TOKENS = (
    "<|im_start|>", "<|im_end|>", "<|endoftext|>", "<|system|>", "<|user|>",
    "<|assistant|>", "<|eot_id|>", "<|start_header_id|>", "<|end_header_id|>",
    "<|begin_of_text|>", "<|end_of_text|>", "[INST]", "[/INST]", "<<SYS>>", "<</SYS>>",
)

_ZWSP = "​"  # zero-width space: breaks token matching, invisible to a reader

# Line-leading fake role markers an injection uses to forge a conversation turn.
_ROLE_LINE_RE = re.compile(r"(?im)^([ \t>*#\-]*)(system|assistant|user|developer|tool)(\s*):")

# Explicit instruction-override phrasing ("ignore the above instructions", ...).
_OVERRIDE_RE = re.compile(
    r"(?i)\b(ignore|disregard|forget|override|bypass)\b[^.\n]{0,40}?"
    r"\b(previous|above|earlier|prior|all|the|your)\b[^.\n]{0,25}?"
    r"\b(instruction|instructions|prompt|prompts|rule|rules|context|message|messages|direction)\b"
)


def sanitize_context_text(text: str) -> str:
    """Defang injection structure in a single untrusted chunk of retrieved text.

    Conservative: it breaks dangerous tokens/markers but preserves human meaning
    (zero-width spaces, bracketed colons) so legitimate ED facts still read normally.
    """
    if not text:
        return text
    out = text
    # 1. Break chat/control special tokens so they can't be tokenized as control.
    for tok in _SPECIAL_TOKENS:
        if tok in out:
            out = out.replace(tok, tok[0] + _ZWSP + tok[1:])
    # 2. Defang our own spotlight keyword so an injection can't fake a fence line.
    out = re.sub(r"(?i)UNTRUSTED-DATA", "UNTRUSTED" + _ZWSP + "-DATA", out)
    # 3. Defang line-leading fake role markers: "System:" -> "System[:]".
    out = _ROLE_LINE_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}[:]", out)
    # 4. Mark explicit override phrases as quoted data, not direction.
    out = _OVERRIDE_RE.sub(lambda m: "(quoted from source) " + m.group(0), out)
    return out


# ---------------------------------------------------------------------------
# Terminal-output sanitizer (security follow-up to 8c0cf9f).
# ---------------------------------------------------------------------------
# DISTINCT threat class from sanitize_context_text above. That one defends the
# LLM PROMPT (chat tokens, fake role lines, override phrasing). THIS one defends
# the local terminal: meta_command() text is printed verbatim to stdout, and two
# interpolated values are untrusted (manifest kb_path, CmdrState.name). An ANSI
# CSI/OSC/ESC, NUL, C0/C1, DEL, or lone-CR payload renders verbatim and can
# hijack the window title (OSC 0), clear the screen (CSI 2J), reposition the
# cursor (CSI H), or overwrite a line (lone CR) to spoof output. We REMOVE the
# control sequences (strip, not escape) so the visible string is a clean
# substring-preserving subset of the input. Pure: deterministic, no I/O.

# CSI: ESC '[' , optional intermediates 0x20-0x2F, final 0x40-0x7E. The whole
# sequence (including a malformed/unterminated tail) is removed. We allow zero
# parameter/intermediate bytes followed by an optional final so a bare "ESC ["
# (truncated) still gets stripped rather than leaving a live introducer.
_CSI_RE = re.compile(r"\x1b\[[0-9:;<=>?]*[ -/]*[@-~]?")

# OSC: ESC ']' ... terminated by BEL (0x07) or ST (ESC '\'). Also matches an
# UNTERMINATED OSC running to end-of-string (a truncated OSC still arms the
# terminal). [\s\S] = any char incl. newline; non-greedy up to the terminator.
_OSC_RE = re.compile(r"\x1b\][\s\S]*?(?:\x07|\x1b\\|$)")

# Any remaining ESC-introduced 2-byte sequence (ESC + a single 0x20-0x7E byte,
# e.g. ESC '\' ST, charset selects ESC '(' B). Strip ESC + its final byte.
_ESC_PAIR_RE = re.compile(r"\x1b[ -~]")

# Control code points to strip outright when encountered bare (after the ESC
# sequence rules above have run): C0 except \n/\t, DEL, C1. NOTE: \r (0x0D) is
# in 0x00-0x1F and is intentionally DROPPED (lone-CR line-overwrite spoof).
# We keep ONLY \n (0x0A) and \t (0x09) from the C0 range.
_BARE_CONTROL_RE = re.compile(
    "[\x00-\x08\x0b-\x1f\x7f\x80-\x9f]"  # C0-minus-(\t,\n), DEL, C1
)


def sanitize_terminal_text(text: str) -> str:
    """Strip terminal-control sequences from text destined for stdout.

    Removes ANSI CSI/OSC sequences, any lone/leftover ESC, the C0 range
    (except '\\n' and '\\t'; '\\r' is dropped), the C1 range (U+0080-U+009F),
    NUL, and DEL. All printable ASCII and ordinary Unicode (>= U+00A0) pass
    through byte-for-byte, so a clean path like 'kb/locations/deciat.md' and a
    clean name like 'Duvrazh' are returned identical.

    PURE: deterministic, no I/O, no global state, no randomness.
    """
    if not text:
        return text
    out = text
    # Order matters: consume multi-byte ESC sequences FIRST (CSI, then OSC),
    # then any stray ESC pair, then any bare ESC, then bare control points.
    # Doing CSI/OSC before the bare-ESC sweep means a complete escape sequence
    # is removed as a unit (introducer + body) rather than leaving its body as
    # visible garbage once the lone ESC is gone.
    out = _CSI_RE.sub("", out)
    out = _OSC_RE.sub("", out)
    out = _ESC_PAIR_RE.sub("", out)
    out = out.replace("\x1b", "")  # any remaining lone ESC (e.g. ESC at EOS)
    out = _BARE_CONTROL_RE.sub("", out)
    return out


def make_nonce() -> str:
    """Random per-call spotlight nonce (16 hex chars; unguessable by injected text)."""
    return secrets.token_hex(8)


def fence(nonce: str) -> tuple[str, str]:
    """Begin/end spotlight markers delimiting the untrusted-data region."""
    return (f"<<<UNTRUSTED-DATA {nonce}>>>", f"<<<END-UNTRUSTED-DATA {nonce}>>>")
