"""M2 — injected-client guard precision + post-construction send-time enforcement.

Problem A (precision): the old construction-time check rejected any client whose
follow_redirects was `not False`, which wrongly rejected follow_redirects=None
(httpx treats None as non-following). Tighten to a truthiness check: accept
False AND None, reject only clients that WILL follow.

Problem B (mutability): httpx.Client.follow_redirects is mutable after
construction. A caller can pass False then flip True. Construction-time checks
are best-effort; harden by passing follow_redirects=False on EVERY per-request
send (a per-call value overrides the client attribute).
"""
import httpx
import pytest

from copilot import acquire, ssrf


def _cfg(allowlist=("edsm.net", "spansh.co.uk"), resolver=None):
    guard = ssrf.GuardConfig(
        allowlist=allowlist,
        resolver=resolver or (lambda h: ["93.184.216.34"]),
    )
    return acquire.AcquireConfig(
        guard=guard, user_agent="m2/0.1", timeout=5.0,
        min_interval=0.0, jitter=0.0, max_attempts=2,
        render_enabled=False, max_bytes=100_000,
    )


# ---- AC-M2a: follow_redirects=None is ACCEPTED (precision tighten) --------

def test_injected_client_follow_redirects_none_is_accepted():
    """httpx treats follow_redirects=None as non-following, so it is SAFE and
    must be accepted — the old `is not False` check wrongly rejected it."""
    cfg = _cfg()
    client = httpx.Client(follow_redirects=None)
    f = acquire.Fetcher(cfg, client=client)  # must NOT raise
    f.close()


def test_injected_client_follow_redirects_false_is_accepted():
    cfg = _cfg()
    f = acquire.Fetcher(cfg, client=httpx.Client(follow_redirects=False))
    f.close()


# ---- AC-M2b: follow_redirects=True is rejected as a PLAIN ValueError ------

def test_injected_client_follow_redirects_true_raises_plain_valueerror():
    cfg = _cfg()
    with pytest.raises(ValueError) as ei:
        acquire.Fetcher(cfg, client=httpx.Client(follow_redirects=True))
    # AC1c preserved: a PLAIN ValueError, NOT an SSRFError (which subclasses
    # ValueError and is reserved for URL/scheme rejection).
    assert type(ei.value) is ValueError
    assert not isinstance(ei.value, ssrf.SSRFError)


# ---- AC-M2c: post-construction mutation cannot bypass the per-hop guard ----

def test_post_construction_mutation_does_not_auto_follow():
    """Build with follow_redirects=False, flip it True afterward, then fetch
    across a redirect. The per-send follow_redirects=False OVERRIDES the mutated
    client attribute, so httpx does NOT auto-follow inside one send(); the manual
    per-hop guard still fires and a redirect to an off-list host is refused."""
    seen = []

    def handler(request):
        seen.append(str(request.url))
        if str(request.url) == "https://edsm.net/start":
            # If the client auto-followed, the off-list hop would be fetched
            # inside this send() WITHOUT a guard. It must not.
            return httpx.Response(302, headers={"location": "https://evil.example/x"})
        raise AssertionError(f"auto-follow leaked to {request.url}")

    cfg = _cfg(allowlist=("edsm.net",))
    client = httpx.Client(transport=httpx.MockTransport(handler),
                          follow_redirects=False, timeout=5.0)
    f = acquire.Fetcher(cfg, client=client)
    # ATTACK: flip the mutable attribute True after the construction-time check.
    client.follow_redirects = True
    try:
        with pytest.raises(ssrf.SSRFError) as ei:
            f.fetch("https://edsm.net/start")
    finally:
        f.close()
    # The redirect was NOT auto-followed; our manual loop re-guarded the off-list
    # host and refused it.
    assert ei.value.reason == "not_allowlisted"
    # Only the first hop's socket was touched — no auto-followed second send.
    assert seen == ["https://edsm.net/start"]


def test_post_construction_mutation_to_private_still_refused():
    """Same mutation attack, but the redirect target resolves PRIVATE. Send-time
    enforcement + per-hop guard still refuse it (resolved_ip_blocked)."""
    def resolver(host):
        return ["127.0.0.1"] if host == "spansh.co.uk" else ["93.184.216.34"]

    def handler(request):
        if str(request.url) == "https://edsm.net/start":
            return httpx.Response(302, headers={"location": "https://spansh.co.uk/evil"})
        raise AssertionError("auto-follow leaked to a private host")

    cfg = _cfg(allowlist=("edsm.net", "spansh.co.uk"), resolver=resolver)
    client = httpx.Client(transport=httpx.MockTransport(handler),
                          follow_redirects=False, timeout=5.0)
    f = acquire.Fetcher(cfg, client=client)
    client.follow_redirects = True  # attack
    try:
        with pytest.raises(ssrf.SSRFError) as ei:
            f.fetch("https://edsm.net/start")
    finally:
        f.close()
    assert ei.value.reason == "resolved_ip_blocked"
