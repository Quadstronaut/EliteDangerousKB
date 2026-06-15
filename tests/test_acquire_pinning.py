"""M1 — DNS-rebind TOCTOU defense: the GET path PINS the connection to the IP
the guard vetted, so a rebinding/racing resolver cannot return public to the
guard then private to the socket microseconds later.

These tests exercise the OWNED/real-transport pinning branch. We construct a
normal (owned) Fetcher, then swap its real transport for an httpx.MockTransport
that CAPTURES the request — while keeping _owns_client=True so the pinning code
path under test actually runs. MockTransport opens no socket and re-resolves
nothing, so we observe exactly what the real transport would have been told to
connect to. (The default acquire suite deliberately injects clients and so
never exercises pinning — see tests/test_acquire.py; pinning is invisible there
by design, which is why those tests stay green unchanged.)
"""
import httpx
import pytest

from copilot import acquire, ssrf


def _make_cfg(resolver, *, allowlist=("edsm.net", "spansh.co.uk"),
              allow_any=False, allow_private=False):
    guard = ssrf.GuardConfig(
        allowlist=allowlist,
        allow_any=allow_any,
        allow_private=allow_private,
        resolver=resolver,
    )
    return acquire.AcquireConfig(
        guard=guard, user_agent="pin-test/0.1", timeout=5.0,
        min_interval=0.0, jitter=0.0, max_attempts=2,
        render_enabled=False, max_bytes=100_000,
    )


def _owned_fetcher_with_capture(cfg, handler):
    """Build an OWNED Fetcher, then swap in a capturing MockTransport while
    keeping _owns_client=True so the PINNING branch runs."""
    f = acquire.Fetcher(cfg)
    f._client.close()
    f._client = httpx.Client(transport=httpx.MockTransport(handler),
                             follow_redirects=False)
    f._owns_client = True
    return f


# ---- AC-M1a: rebinding resolver cannot be exploited (single resolve) ------

def test_pin_defeats_dns_rebind_single_resolve():
    """Resolver returns PUBLIC first, PRIVATE on any later call. If the design
    pins correctly there is NO second resolve to exploit: the socket target is
    the vetted public IP and the resolver was called exactly once for the hop."""
    calls = {"n": 0}

    def rebinding(host):
        calls["n"] += 1
        # first answer public; every subsequent answer is loopback (the attack)
        return ["93.184.216.34"] if calls["n"] == 1 else ["127.0.0.1"]

    captured = {}

    def handler(request):
        captured["url"] = str(request.url)
        captured["host"] = request.headers.get("host")
        captured["sni"] = request.extensions.get("sni_hostname")
        return httpx.Response(200, text="ok", headers={"content-type": "text/plain"})

    cfg = _make_cfg(rebinding)
    f = _owned_fetcher_with_capture(cfg, handler)
    try:
        r = f.fetch("https://edsm.net/page")
    finally:
        f.close()

    # Exactly ONE resolve happened for the hop — nothing left to rebind.
    assert calls["n"] == 1
    # The socket was told to connect to the VETTED public IP, never the rebind.
    assert captured["url"] == "https://93.184.216.34/page"
    assert "127.0.0.1" not in captured["url"]
    # Virtual-hosting + TLS cert verification preserved (Host + SNI = hostname).
    assert captured["host"] == "edsm.net"
    assert captured["sni"] == "edsm.net"
    # The FetchResult still reports the hostname URL, not the literal IP.
    assert r.url == "https://edsm.net/page"
    assert r.redirect_chain == ("https://edsm.net/page",)


# ---- AC-M1b: vetted-private host fails closed (no unpinned fallback) ------

def test_vetted_private_host_raises_resolved_ip_blocked():
    """A host the guard vets and finds PRIVATE raises resolved_ip_blocked before
    any connect (today's behavior, preserved). No unpinned fallback connect."""
    captured = {"hit": False}

    def handler(request):
        captured["hit"] = True
        return httpx.Response(200, text="should-never-reach")

    cfg = _make_cfg(lambda h: ["127.0.0.1"])  # always private
    f = _owned_fetcher_with_capture(cfg, handler)
    try:
        with pytest.raises(ssrf.SSRFError) as ei:
            f.fetch("https://edsm.net/page")
    finally:
        f.close()
    assert ei.value.reason == "resolved_ip_blocked"
    assert captured["hit"] is False  # connection never opened


def test_pin_failure_degrades_closed_never_unpinned():
    """If pinning cannot be constructed (empty vetted-IP set), the request is
    REFUSED — never fall back to an unpinned (re-resolving) connect (AC-M1b)."""
    cfg = _make_cfg(lambda h: ["93.184.216.34"])
    f = acquire.Fetcher(cfg)
    try:
        with pytest.raises(ssrf.SSRFError) as ei:
            # Directly exercise the builder's degrade-closed contract.
            f._build_pinned_request("https://edsm.net/page", [])
    finally:
        f.close()
    assert ei.value.reason == "resolved_ip_blocked"


# ---- AC-M1c: per-hop re-pin (each hop binds to its OWN vetted IP) ---------

def test_per_hop_repin_hop2_private_refused_at_hop2():
    """A 2-hop redirect where hop-2's host re-resolves PRIVATE at connect time is
    refused at hop-2 with resolved_ip_blocked. Hop-1 connected to hop-1's vetted
    IP; hop-2 is independently parsed -> guarded -> would pin its OWN vetted IP,
    but is private so it fails closed before any hop-2 connect."""
    targets = []

    def resolver(host):
        # hop-1 host public; hop-2 host private (the rebind/off-list-at-connect).
        return ["93.184.216.34"] if host == "edsm.net" else ["127.0.0.1"]

    def handler(request):
        targets.append(str(request.url))
        # hop-1 served from the pinned public IP, redirects to spansh.co.uk
        if request.headers.get("host") == "edsm.net":
            return httpx.Response(302, headers={"location": "https://spansh.co.uk/evil"})
        raise AssertionError(f"hop-2 connection must never open: {request.url}")

    cfg = _make_cfg(resolver, allowlist=("edsm.net", "spansh.co.uk"))
    f = _owned_fetcher_with_capture(cfg, handler)
    try:
        with pytest.raises(ssrf.SSRFError) as ei:
            f.fetch("https://edsm.net/start")
    finally:
        f.close()
    assert ei.value.reason == "resolved_ip_blocked"
    # Exactly one connection opened — hop-1, pinned to ITS OWN vetted IP.
    assert targets == ["https://93.184.216.34/start"]


def test_per_hop_repin_each_hop_binds_its_own_ip():
    """A benign 2-hop redirect across two allowlisted hosts that resolve to
    DIFFERENT public IPs: each hop's socket target is that hop's OWN vetted IP,
    never the prior hop's."""
    def resolver(host):
        return {"edsm.net": ["93.184.216.34"],
                "spansh.co.uk": ["151.101.0.81"]}[host]

    targets = []

    def handler(request):
        targets.append(str(request.url))
        host = request.headers.get("host")
        if host == "edsm.net":
            return httpx.Response(302, headers={"location": "https://spansh.co.uk/final"})
        if host == "spansh.co.uk":
            return httpx.Response(200, text="DONE", headers={"content-type": "text/plain"})
        raise AssertionError(f"unexpected host {host}")

    cfg = _make_cfg(resolver, allowlist=("edsm.net", "spansh.co.uk"))
    f = _owned_fetcher_with_capture(cfg, handler)
    try:
        r = f.fetch("https://edsm.net/start")
    finally:
        f.close()
    assert r.text == "DONE"
    assert r.url == "https://spansh.co.uk/final"
    # Hop-1 pinned to edsm's IP; hop-2 pinned to spansh's OWN IP (re-pin).
    assert targets == [
        "https://93.184.216.34/start",
        "https://151.101.0.81/final",
    ]
    # The redirect_chain still reports HOSTNAME URLs (pinning is connection-only).
    assert r.redirect_chain == (
        "https://edsm.net/start",
        "https://spansh.co.uk/final",
    )


def test_ip_literal_pins_to_itself_under_allow_any():
    """An allow_any IP-literal host pins to the literal itself (M1: literal IS
    its own vetted target)."""
    cfg = _make_cfg(lambda h: (_ for _ in ()).throw(AssertionError("no DNS")),
                    allow_any=True, allowlist=())
    f = acquire.Fetcher(cfg)
    try:
        req = f._build_pinned_request("https://93.184.216.34/x", ["93.184.216.34"])
    finally:
        f.close()
    assert str(req.url) == "https://93.184.216.34/x"
    assert req.headers.get("host") == "93.184.216.34"
