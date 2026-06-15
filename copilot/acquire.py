"""Hardened web-acquisition primitive (Stage-0 item: copilot/acquire.py).

Every outbound request passes through ssrf.assert_url_safe BEFORE the socket
opens — the initial URL AND every redirect Location (we follow redirects
MANUALLY, follow_redirects=False, so a 302 to a private/non-allowlisted host is
refused). All returned text is run through sanitize.sanitize_context_text so no
raw fetched text ever leaves this module. Acquisition NEVER marks content
verified; it stages content for the existing verify phase only.

Adapted (hardened) from the upstream scraper http/render/reddit helpers:
  - the upstream make_client used follow_redirects=True with no guard -> SSRF. Fixed.
  - the upstream renderer rendered arbitrary URLs with no guard -> SSRF. Now guarded +
    allowlist-only (Playwright can't be per-hop guarded; residual-risk reduced).
  - the upstream reddit polite-throttle primitive is reused here, source-agnostic.

Code was copied/adapted, NOT referenced: nothing under copilot/ imports the
upstream package or hard-codes its source path (I12).
"""
from __future__ import annotations

import hashlib
import random
import time
from dataclasses import dataclass
from typing import Optional

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from copilot import sanitize, ssrf
from copilot.acquire_sources import default_allowlist

DEFAULT_UA: str = "EliteDangerousKB-research/0.1 (+local; polite)"
DEFAULT_TIMEOUT: float = 30.0
MAX_REDIRECTS: int = 5
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class PlaywrightUnavailable(RuntimeError):
    """Raised by render() when the optional playwright dependency is absent.
    Catchable + documented so the loop degrades gracefully (I7)."""


@dataclass(frozen=True)
class AcquireConfig:
    guard: ssrf.GuardConfig
    user_agent: str = DEFAULT_UA
    timeout: float = DEFAULT_TIMEOUT
    min_interval: float = 1.0
    jitter: float = 0.5
    max_attempts: int = 3
    render_enabled: bool = False
    max_bytes: int = 5_000_000


@dataclass(frozen=True)
class FetchResult:
    url: str                       # FINAL url after redirects (every hop guarded)
    status: int
    content_type: Optional[str]
    text: str                      # ALREADY sanitized via sanitize_context_text
    raw_sha256: str                # sha256 of RAW pre-sanitize bytes (seen.json parity)
    rendered: bool                 # True if the Playwright path produced it
    redirect_chain: tuple[str, ...]


def load_acquire_config(cfg: dict | None = None) -> AcquireConfig:
    """Build AcquireConfig from config.toml [acquire] (via paths.load_config()
    if cfg is None). Safe defaults for any missing key. allow_private and
    allow_any default False regardless of config UNLESS explicitly set true.

    Offline-safe: this function performs NO network I/O (I8/I13).
    """
    if cfg is None:
        # Local import keeps import-time deps minimal and offline-clean.
        from copilot.paths import load_config

        cfg = load_config()

    acq = dict((cfg or {}).get("acquire", {}) or {})

    # --- allowlist: explicit non-empty list overrides; else roster union ---
    raw_allow = acq.get("allowlist")
    if isinstance(raw_allow, (list, tuple)) and len(raw_allow) > 0:
        allowlist = tuple(str(d).strip().lower() for d in raw_allow)
    else:
        allowlist = default_allowlist()

    # --- ports ---
    raw_ports = acq.get("allowed_ports")
    if isinstance(raw_ports, (list, tuple)) and len(raw_ports) > 0:
        allowed_ports = frozenset(int(p) for p in raw_ports)
    else:
        allowed_ports = frozenset({80, 443})

    # --- security flags: default False unless EXPLICITLY True (A10) ---
    allow_any = acq.get("allow_any") is True
    allow_private = acq.get("allow_private") is True

    guard = ssrf.GuardConfig(
        allowlist=allowlist,
        allow_any=allow_any,
        allowed_ports=allowed_ports,
        allow_private=allow_private,
    )

    return AcquireConfig(
        guard=guard,
        user_agent=str(acq.get("user_agent", DEFAULT_UA)),
        timeout=float(acq.get("timeout", DEFAULT_TIMEOUT)),
        min_interval=float(acq.get("min_interval", 1.0)),
        jitter=float(acq.get("jitter", 0.5)),
        max_attempts=int(acq.get("max_attempts", 3)),
        render_enabled=acq.get("render") is True,
        max_bytes=int(acq.get("max_bytes", 5_000_000)),
    )


def _is_retryable(exc: BaseException) -> bool:
    # SSRFError must NEVER be retried (I10) — it is terminal.
    if isinstance(exc, ssrf.SSRFError):
        return False
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRYABLE_STATUS
    return isinstance(exc, httpx.TransportError)


class Fetcher:
    """Hardened GET + optional render, all behind ssrf.assert_url_safe."""

    def __init__(self, cfg: AcquireConfig, *, client: httpx.Client | None = None) -> None:
        self._cfg = cfg
        self._owns_client = client is None
        # follow_redirects=False is the load-bearing flip vs the upstream helper:
        # we guard each hop ourselves before issuing the next request (I3).
        self._client = client or httpx.Client(
            http2=True,
            timeout=cfg.timeout,
            follow_redirects=False,
            headers={"User-Agent": cfg.user_agent, "Accept": "*/*"},
        )
        self._last_request_at: float = 0.0

    # --- polite throttle (adapted from reddit.py) ---
    def _throttle(self) -> None:
        if self._cfg.min_interval <= 0.0 and self._cfg.jitter <= 0.0:
            return
        elapsed = time.monotonic() - self._last_request_at
        wait = self._cfg.min_interval + random.uniform(0, self._cfg.jitter) - elapsed
        if wait > 0:
            time.sleep(wait)

    def _read_capped(self, resp: httpx.Response) -> bytes:
        """Stream the body, refusing once it exceeds max_bytes (I11, DoS guard)."""
        cap = self._cfg.max_bytes
        # Cheap pre-check: trust an honest Content-Length to fail fast.
        cl = resp.headers.get("content-length")
        if cl is not None:
            try:
                if int(cl) > cap:
                    raise ValueError(f"response too large: Content-Length {cl} > {cap}")
            except ValueError as exc:
                if "too large" in str(exc):
                    raise
        chunks: list[bytes] = []
        total = 0
        for chunk in resp.iter_bytes():
            total += len(chunk)
            if total > cap:
                raise ValueError(f"response body exceeded max_bytes ({cap})")
            chunks.append(chunk)
        return b"".join(chunks)

    def _guarded_get(self, url: str) -> httpx.Response:
        """One guarded, throttled, retried GET (no redirect following)."""
        # SSRF guard BEFORE any socket opens (I1). Raised SSRFError is terminal.
        ssrf.assert_url_safe(url, self._cfg.guard)

        @retry(
            retry=retry_if_exception(_is_retryable),
            stop=stop_after_attempt(self._cfg.max_attempts),
            wait=wait_exponential(multiplier=1, min=1, max=30),
            reraise=True,
        )
        def _do() -> httpx.Response:
            self._throttle()
            # stream=True so we can cap the body before buffering it whole.
            resp = self._client.send(
                self._client.build_request("GET", url),
                stream=True,
            )
            self._last_request_at = time.monotonic()
            # Only raise (and thus retry) on retryable statuses; redirects and
            # other statuses pass through for the caller to interpret.
            if resp.status_code in RETRYABLE_STATUS:
                try:
                    resp.read()
                finally:
                    resp.close()
                raise httpx.HTTPStatusError(
                    f"retryable status {resp.status_code}",
                    request=resp.request,
                    response=resp,
                )
            return resp

        return _do()

    def fetch(self, url: str) -> FetchResult:
        """Hardened GET with manual, per-hop-guarded redirect following.

        Guards the initial URL and EVERY redirect Location before the next
        request. Enforces MAX_REDIRECTS and max_bytes. Routes the final body
        through sanitize.sanitize_context_text. SSRFError on any hop propagates
        immediately and is NEVER retried (I10).
        """
        chain: list[str] = []
        current = url
        for _hop in range(MAX_REDIRECTS + 1):
            resp = self._guarded_get(current)
            chain.append(current)
            try:
                if resp.is_redirect:
                    loc = resp.headers.get("location")
                    if not loc:
                        # Redirect status with no Location — treat as terminal.
                        return self._finalize(resp, current, chain)
                    # Resolve relative redirects against the current URL.
                    nxt = str(httpx.URL(resp.url).join(loc))
                    resp.close()
                    current = nxt
                    continue
                return self._finalize(resp, current, chain)
            finally:
                # _finalize closes on the success path; ensure redirect responses
                # are not leaked if we looped without an explicit close above.
                if not resp.is_closed:
                    resp.close()
        raise httpx.TooManyRedirects(
            f"exceeded MAX_REDIRECTS={MAX_REDIRECTS} for {url!r}"
        )

    def _finalize(self, resp: httpx.Response, final_url: str, chain: list[str]) -> FetchResult:
        try:
            raw = self._read_capped(resp)
        finally:
            resp.close()
        raw_sha = hashlib.sha256(raw).hexdigest()
        # Decode using httpx's charset detection, replacing undecodable bytes.
        try:
            text = raw.decode(resp.encoding or "utf-8", errors="replace")
        except (LookupError, TypeError):
            text = raw.decode("utf-8", errors="replace")
        clean = sanitize.sanitize_context_text(text)
        return FetchResult(
            url=final_url,
            status=resp.status_code,
            content_type=resp.headers.get("content-type"),
            text=clean,
            raw_sha256=raw_sha,
            rendered=False,
            redirect_chain=tuple(chain),
        )

    def render(self, url: str, **opts) -> FetchResult:
        """Optional Playwright render. assert_url_safe(url) runs FIRST.

        Playwright follows redirects/subresources internally and CANNOT be
        per-hop guarded the way httpx is, so render is gated to allowlisted
        hosts ONLY (refuses when allow_any=True, since an arbitrary host can't
        get the residual-risk reduction). Lazy-imports playwright; raises
        PlaywrightUnavailable if absent (I7). Output text is sanitized.
        """
        # Residual-risk reduction: render only allowlisted, non-allow_any hosts.
        if self._cfg.guard.allow_any:
            raise ssrf.SSRFError(
                "not_allowlisted",
                "render() refuses allow_any mode: arbitrary-host render is unguardable",
            )
        # Guard the initial URL (the only hop we control). Subresource/redirect
        # hops inside the browser are NOT individually guarded — documented risk.
        ssrf.assert_url_safe(url, self._cfg.guard)

        sync_playwright = _import_playwright()
        wait_state = opts.get("wait_state", "networkidle")
        timeout_ms = int(opts.get("timeout_ms", int(self._cfg.timeout * 1000)))
        wait_for = opts.get("wait_for")
        extra_wait_ms = int(opts.get("extra_wait_ms", 0))

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context = browser.new_context(user_agent=self._cfg.user_agent)
                page = context.new_page()
                page.goto(url, timeout=timeout_ms, wait_until=wait_state)
                if wait_for:
                    page.wait_for_selector(wait_for, timeout=timeout_ms)
                if extra_wait_ms > 0:
                    page.wait_for_timeout(extra_wait_ms)
                html = page.content()
            finally:
                browser.close()

        raw = html.encode("utf-8", errors="replace")
        clean = sanitize.sanitize_context_text(html)
        return FetchResult(
            url=url,
            status=200,
            content_type="text/html",
            text=clean,
            raw_sha256=hashlib.sha256(raw).hexdigest(),
            rendered=True,
            redirect_chain=(url,),
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "Fetcher":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def _import_playwright():
    """Lazy import so the module loads offline / without the optional dep (I7/I8)."""
    try:
        from playwright.sync_api import sync_playwright  # type: ignore[import-not-found]
    except ImportError as exc:
        raise PlaywrightUnavailable(
            "Playwright is required for JS-rendered sources. "
            "Install with: pip install playwright && playwright install chromium"
        ) from exc
    return sync_playwright
