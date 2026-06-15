"""Declarative roster of in-scope ED data sources (Stage-0 item 5).

This is DATA, not fetch logic. The SSRF allowlist and the in-scope source list
are the same list viewed two ways (security boundary == in-scope sources), so we
keep them in one place to prevent drift where a source is "in scope" but not
allowlisted (the SSRF footgun). Tiers match ed-research-prompt SOURCE ROSTER.

Reddit (Tier-3 corroboration) is intentionally OUT of the default fetch
allowlist for v1 — corroboration-only, requires human/verify gating. Its
throttle primitive is adapted into acquire.Fetcher, but its domain is not here.
"""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

from copilot import ssrf

VALID_KINDS = frozenset({"json_api", "html", "js_rendered"})


@dataclass(frozen=True)
class EDSource:
    key: str                  # "edsm" | "spansh" | ...
    domains: tuple[str, ...]  # allowlist entries this source needs
    tier: int                 # 0..3, matches ed-research-prompt SOURCE ROSTER
    kind: str                 # "json_api" | "html" | "js_rendered"
    polite_min_interval: float
    robots_note: str          # robots/ToS + rate-limit note (one line)


# The canonical roster. One data edit + one test to add a source — reviewed here.
ED_SOURCES: tuple[EDSource, ...] = (
    EDSource(
        key="coriolis-data",
        domains=("raw.githubusercontent.com",),
        tier=0,
        kind="json_api",
        polite_min_interval=1.0,
        robots_note="public GitHub raw; be polite ~1 req/s; no auth",
    ),
    EDSource(
        key="edsm",
        domains=("edsm.net",),
        tier=0,
        kind="json_api",
        polite_min_interval=1.0,
        robots_note="public API (api-v1); polite ~1 req/s; UA required (bare UA 403s)",
    ),
    EDSource(
        key="spansh",
        domains=("spansh.co.uk",),
        tier=0,
        kind="json_api",
        polite_min_interval=1.0,
        robots_note="public API; polite ~1 req/s",
    ),
    EDSource(
        key="canonn",
        domains=("api.canonn.tech",),
        tier=0,
        kind="json_api",
        polite_min_interval=1.0,
        robots_note="public API; polite ~1 req/s",
    ),
    EDSource(
        key="inara",
        domains=("inara.cz",),
        tier=1,
        kind="html",
        polite_min_interval=2.0,
        robots_note="25 req / 15 min — gate via check_inara_rate; UA required",
    ),
    EDSource(
        key="frontier-forums",
        domains=("forums.frontier.co.uk",),
        tier=1,
        kind="html",
        polite_min_interval=2.0,
        robots_note="respect robots; polite, low volume",
    ),
    EDSource(
        key="ed-fandom",
        domains=("elite-dangerous.fandom.com",),
        tier=2,
        kind="html",
        polite_min_interval=1.5,
        robots_note="Fandom ToS; polite; attribute; verify vs Tier-0",
    ),
    EDSource(
        key="edsy",
        domains=("edsy.org",),
        tier=2,
        kind="js_rendered",
        polite_min_interval=1.5,
        robots_note="client-rendered; needs Playwright OR import-string fallback; polite",
    ),
    EDSource(
        key="coriolis",
        domains=("coriolis.io",),
        tier=2,
        kind="js_rendered",
        polite_min_interval=1.5,
        robots_note="prefer Tier-0 raw JSON (coriolis-data); render only if necessary",
    ),
)


def default_allowlist() -> tuple[str, ...]:
    """Union of every ED_SOURCES domain (order-stable, de-duplicated).

    This IS the default SSRF allowlist when config omits an explicit list.
    """
    seen: list[str] = []
    for src in ED_SOURCES:
        for dom in src.domains:
            if dom not in seen:
                seen.append(dom)
    return tuple(seen)


def source_for_url(url: str) -> EDSource | None:
    """Return the EDSource whose domain host-suffix-matches the url's host, else None.

    Uses the same exact-or-subdomain suffix rule as the SSRF allowlist so the two
    never disagree about what a host "is".
    """
    host = (urlsplit(url).hostname or "").strip().rstrip(".").lower()
    if not host:
        return None
    for src in ED_SOURCES:
        if ssrf.host_is_allowlisted(host, src.domains):
            return src
    return None
