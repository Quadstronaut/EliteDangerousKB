"""Adversarial SSRF suite (Stage-0 A4). Each case asserts SSRFError AND the exact
.reason. The resolver is injected so the default suite makes ZERO network calls
(A3): a resolver that raises if hit unexpectedly proves no real DNS happened.
"""
import pytest

from copilot import ssrf
from copilot.acquire_sources import default_allowlist


# A resolver that maps test hostnames to chosen IPs, and raises if asked about
# anything unexpected — so an unintended real lookup is a loud test failure (A3).
def make_resolver(mapping):
    def _resolve(host):
        if host not in mapping:
            raise AssertionError(f"unexpected DNS resolution attempted for {host!r}")
        return list(mapping[host])
    return _resolve


def guard(*, allow_any=False, allow_private=False, allowlist=None, resolver=None,
          allowed_ports=frozenset({80, 443})):
    return ssrf.GuardConfig(
        allowlist=tuple(allowlist if allowlist is not None else default_allowlist()),
        allow_any=allow_any,
        allow_private=allow_private,
        allowed_ports=allowed_ports,
        resolver=resolver or make_resolver({}),
    )


# --- is_ip_blocked unit ---

@pytest.mark.parametrize("ip", [
    "0.0.0.0", "127.0.0.1", "10.0.0.1", "172.16.5.5", "192.168.1.1",
    "169.254.169.254", "::1", "fc00::1", "fe80::1", "224.0.0.1",
    "::ffff:127.0.0.1", "::",
])
def test_is_ip_blocked_blocks_private(ip):
    assert ssrf.is_ip_blocked(ip) is True


@pytest.mark.parametrize("ip", ["8.8.8.8", "1.1.1.1", "93.184.216.34", "2606:2800:220:1::"])
def test_is_ip_blocked_allows_public(ip):
    assert ssrf.is_ip_blocked(ip) is False


def test_is_ip_blocked_unparseable_fails_closed():
    assert ssrf.is_ip_blocked("not-an-ip") is True


# --- host_is_allowlisted unit (A4g, I4) ---

def test_allowlist_exact_and_subdomain():
    al = ("inara.cz",)
    assert ssrf.host_is_allowlisted("inara.cz", al)
    assert ssrf.host_is_allowlisted("www.inara.cz", al)
    assert ssrf.host_is_allowlisted("INARA.CZ", al)  # case-insensitive


def test_allowlist_rejects_lookalikes():
    al = ("inara.cz",)
    assert not ssrf.host_is_allowlisted("evilinara.cz", al)
    assert not ssrf.host_is_allowlisted("inara.cz.evil.com", al)


def test_allowlist_never_matches_ip_literal():
    assert not ssrf.host_is_allowlisted("127.0.0.1", ("127.0.0.1",))
    assert not ssrf.host_is_allowlisted("8.8.8.8", ("edsm.net",))


# --- assert_url_safe adversarial cases (A4 a-j) ---

def test_a_private_ip_literal_refused():
    cfg = guard(allow_any=True)  # allow_any so we get to the IP-literal check
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("http://10.0.0.5/x", cfg)
    assert ei.value.reason == "literal_ip_blocked"


def test_b_loopback_and_ipv6_loopback_refused():
    cfg = guard(allow_any=True)
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("http://127.0.0.1/x", cfg)
    assert ei.value.reason == "literal_ip_blocked"
    with pytest.raises(ssrf.SSRFError) as ei2:
        ssrf.assert_url_safe("http://[::1]/x", cfg)
    assert ei2.value.reason == "literal_ip_blocked"


def test_c_cloud_metadata_refused():
    cfg = guard(allow_any=True)
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("http://169.254.169.254/latest/meta-data/", cfg)
    assert ei.value.reason == "literal_ip_blocked"


def test_f_non_http_scheme_refused():
    cfg = guard()
    for url in ("file:///etc/passwd", "ftp://edsm.net/x", "data:text/html,hi",
                "gopher://edsm.net/", "edsm.net/no-scheme"):
        with pytest.raises(ssrf.SSRFError) as ei:
            ssrf.assert_url_safe(url, cfg)
        assert ei.value.reason == "scheme", url


def test_no_host_refused():
    cfg = guard()
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("http:///nohost", cfg)
    assert ei.value.reason == "no_host"


def test_g_allowlist_off_list_refused_on_list_allowed():
    rez = make_resolver({"edsm.net": ["93.184.216.34"]})
    cfg = guard(resolver=rez)
    # off-list public host -> not_allowlisted (and DNS is never even attempted)
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("https://evil.example.com/x", cfg)
    assert ei.value.reason == "not_allowlisted"
    # on-list host with a public resolved IP -> OK, returns url unchanged
    assert ssrf.assert_url_safe("https://edsm.net/api-v1/system", cfg) == \
        "https://edsm.net/api-v1/system"


def test_h_dns_rebind_resolved_ip_refused():
    # public-looking allowlisted host whose injected resolver returns a private IP
    rez = make_resolver({"edsm.net": ["127.0.0.1"]})
    cfg = guard(resolver=rez)
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("https://edsm.net/api-v1/system", cfg)
    assert ei.value.reason == "resolved_ip_blocked"


def test_h2_dns_rebind_metadata_resolved_ip_refused():
    rez = make_resolver({"edsm.net": ["169.254.169.254"]})
    cfg = guard(resolver=rez)
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("https://edsm.net/x", cfg)
    assert ei.value.reason == "resolved_ip_blocked"


def test_i_ipv4_mapped_ipv6_refused():
    cfg = guard(allow_any=True)
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("http://[::ffff:127.0.0.1]/x", cfg)
    assert ei.value.reason == "literal_ip_blocked"


def test_j_port_not_allowed_refused():
    cfg = guard()
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("https://edsm.net:8080/x", cfg)
    assert ei.value.reason == "port_blocked"


def test_explicit_allowed_port_passes():
    rez = make_resolver({"edsm.net": ["93.184.216.34"]})
    cfg = guard(resolver=rez)
    assert ssrf.assert_url_safe("https://edsm.net:443/x", cfg) == "https://edsm.net:443/x"


def test_resolve_failed_reason():
    def boom(host):
        raise OSError("no such host")
    cfg = guard(resolver=boom)
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("https://edsm.net/x", cfg)
    assert ei.value.reason == "resolve_failed"


def test_resolve_empty_reason():
    cfg = guard(resolver=make_resolver({"edsm.net": []}))
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("https://edsm.net/x", cfg)
    assert ei.value.reason == "resolve_failed"


def test_allow_private_lets_resolved_private_through():
    rez = make_resolver({"edsm.net": ["127.0.0.1"]})
    cfg = guard(resolver=rez, allow_private=True)
    assert ssrf.assert_url_safe("https://edsm.net/x", cfg) == "https://edsm.net/x"


def test_ip_literal_refused_without_allow_any():
    # A non-blocked public IP literal is still refused unless allow_any is set:
    # a domain allowlist never authorizes a bare IP (documented invariant).
    cfg = guard()  # allow_any=False
    with pytest.raises(ssrf.SSRFError) as ei:
        ssrf.assert_url_safe("http://8.8.8.8/x", cfg)
    assert ei.value.reason == "not_allowlisted"


def test_redirect_chain_helper_validates_initial():
    rez = make_resolver({"edsm.net": ["93.184.216.34"]})
    cfg = guard(resolver=rez)
    # ok
    ssrf.assert_redirect_chain_safe("https://edsm.net/x", cfg)
    # bad scheme bubbles up
    with pytest.raises(ssrf.SSRFError):
        ssrf.assert_redirect_chain_safe("file:///x", cfg)
