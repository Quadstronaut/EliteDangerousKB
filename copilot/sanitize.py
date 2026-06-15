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


def make_nonce() -> str:
    """Random per-call spotlight nonce (16 hex chars; unguessable by injected text)."""
    return secrets.token_hex(8)


def fence(nonce: str) -> tuple[str, str]:
    """Begin/end spotlight markers delimiting the untrusted-data region."""
    return (f"<<<UNTRUSTED-DATA {nonce}>>>", f"<<<END-UNTRUSTED-DATA {nonce}>>>")
