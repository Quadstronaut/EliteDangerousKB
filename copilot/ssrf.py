"""SSRF guard — the single chokepoint for every outbound URL in acquire.py.

The web-acquisition layer fetches the open web into the KB. Without a guard, a
crafted (or redirected, or DNS-rebound) URL can make our process talk to a
loopback/private/link-local/cloud-metadata address — classic SSRF. This module
is a PURE, synchronous validator: it parses one URL, refuses bad schemes/ports,
refuses IP literals in blocked ranges, enforces the domain allowlist for
hostnames, then RESOLVES the host and refuses if ANY resolved IP is blocked
(DNS-rebind defense). The only I/O is the injectable resolver() — tests swap it
to simulate a public hostname that resolves to 127.0.0.1.

Adapted (hardened) from the upstream scraper http/render helpers, which used
follow_redirects=True with no host/IP guard. We invert that: the client follows
NO redirects; acquire.py re-runs assert_url_safe on every hop. (Code was copied
and rewritten here; nothing under copilot/ imports the upstream package.)
"""
from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass, field
from typing import Callable, Iterable
from urllib.parse import urlsplit


# Exact .reason strings asserted by tests/test_ssrf.py — DO NOT rename.
REASONS = frozenset(
    {
        "scheme",
        "no_host",
        "literal_ip_blocked",
        "resolved_ip_blocked",
        "not_allowlisted",
        "resolve_failed",
        "port_blocked",
    }
)


class SSRFError(ValueError):
    """Raised when a URL/host/IP fails the SSRF guard. Carries .reason (str enum)."""

    def __init__(self, reason: str, message: str = "") -> None:
        self.reason = reason
        super().__init__(message or reason)


def _default_resolver(host: str) -> list[str]:
    """Resolve host -> list of IP strings (v4 and v6). Stdlib getaddrinfo wrapper.

    Returns every distinct address the host maps to so the caller can block if
    ANY of them is private. Raises socket.gaierror on failure (caught upstream).
    """
    infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    out: list[str] = []
    for info in infos:
        ip = info[4][0]
        # getaddrinfo IPv6 sockaddr can carry a %scope suffix — strip it.
        ip = ip.split("%", 1)[0]
        if ip not in out:
            out.append(ip)
    return out


@dataclass(frozen=True)
class GuardConfig:
    allowlist: tuple[str, ...]                       # suffix-matched ED domains
    allow_any: bool = False                          # default: allowlist enforced
    allowed_ports: frozenset[int] = frozenset({80, 443})
    allow_private: bool = False                      # NEVER True in prod config
    resolver: Callable[[str], list[str]] = field(default=_default_resolver)


def is_ip_blocked(ip: str) -> bool:
    """True if ip (v4 or v6) is loopback/private/link-local/reserved/etc.

    Blocks 0.0.0.0, 127/8, 10/8, 172.16/12, 192.168/16, 169.254/16 (incl. the
    cloud-metadata 169.254.169.254), ::1, fc00::/7, fe80::/10, and unwraps
    IPv4-mapped IPv6 (::ffff:0:0/96) to re-check the embedded v4 address. Any
    unparseable address is treated as blocked (fail-closed).
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True  # fail closed: can't parse -> don't trust

    # IPv4-mapped IPv6 (::ffff:127.0.0.1): unwrap and re-check the v4 inside.
    if isinstance(addr, ipaddress.IPv6Address) and addr.ipv4_mapped is not None:
        return is_ip_blocked(str(addr.ipv4_mapped))

    return bool(
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
        or addr.is_unspecified
    )


def host_is_allowlisted(host: str, allowlist: Iterable[str]) -> bool:
    """Case-insensitive exact-or-subdomain suffix match.

    'inara.cz' matches 'inara.cz' and 'www.inara.cz' but NOT 'evilinara.cz' and
    NOT 'inara.cz.evil.com'. An IP literal is NEVER allowlisted by a domain
    entry (returns False) — a domain allowlist must not authorize a bare IP.
    """
    host = host.strip().rstrip(".").lower()
    if not host:
        return False
    # IP literals are never authorized by a domain allowlist.
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass
    for entry in allowlist:
        entry = entry.strip().rstrip(".").lower()
        if not entry:
            continue
        if host == entry or host.endswith("." + entry):
            return True
    return False


def _is_ip_literal(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def assert_url_safe(url: str, cfg: GuardConfig) -> str:
    """The ONE guard. Validates a SINGLE url (one hop). Returns url unchanged on success.

    Steps, in order (each failure raises SSRFError with the exact .reason):
      1. parse; refuse non-http(s) scheme            -> 'scheme'
      2. refuse missing host                          -> 'no_host'
      3. refuse port not in allowed_ports             -> 'port_blocked'
      4. host is an IP literal: if is_ip_blocked      -> 'literal_ip_blocked'
         (a domain allowlist NEVER authorizes a bare IP; an IP literal that is
          NOT in a blocked range is allowed only when allow_any is True)
      5. else (hostname): enforce allowlist unless allow_any -> 'not_allowlisted'
      6. resolve host -> list[ip]; empty/raises       -> 'resolve_failed'
      7. for EVERY resolved ip: if is_ip_blocked (unless allow_private)
                                                       -> 'resolved_ip_blocked'
    Pure/synchronous; the only I/O is cfg.resolver().
    """
    parts = urlsplit(url)

    # 1. scheme
    if parts.scheme.lower() not in ("http", "https"):
        raise SSRFError("scheme", f"non-http(s) scheme: {parts.scheme!r} in {url!r}")

    # 2. host
    host = parts.hostname  # already lowercased + brackets stripped by urlsplit
    if not host:
        raise SSRFError("no_host", f"URL has no host: {url!r}")

    # 3. port (explicit only; default ports for the scheme are implicitly allowed)
    try:
        port = parts.port  # raises ValueError on a malformed port
    except ValueError:
        raise SSRFError("port_blocked", f"malformed port in {url!r}")
    if port is not None and port not in cfg.allowed_ports:
        raise SSRFError("port_blocked", f"port {port} not in {sorted(cfg.allowed_ports)}")

    # 4 / 5. literal IP vs hostname
    if _is_ip_literal(host):
        if is_ip_blocked(host):
            raise SSRFError("literal_ip_blocked", f"blocked IP literal: {host}")
        # A non-blocked IP literal is only allowed when the allowlist is disabled.
        if not cfg.allow_any:
            raise SSRFError("not_allowlisted", f"IP literal not allowed: {host}")
        # allow_any + non-blocked literal: nothing left to resolve; accept.
        return url
    else:
        if not cfg.allow_any and not host_is_allowlisted(host, cfg.allowlist):
            raise SSRFError("not_allowlisted", f"host not allowlisted: {host}")

    # 6. resolve
    try:
        ips = cfg.resolver(host)
    except Exception as exc:  # gaierror, timeout, anything from the resolver
        raise SSRFError("resolve_failed", f"DNS resolve failed for {host}: {exc}") from exc
    if not ips:
        raise SSRFError("resolve_failed", f"DNS returned no address for {host}")

    # 7. every resolved IP must be public (DNS-rebind defense)
    if not cfg.allow_private:
        for ip in ips:
            if is_ip_blocked(ip):
                raise SSRFError(
                    "resolved_ip_blocked",
                    f"{host} resolved to blocked IP {ip}",
                )

    return url


def assert_redirect_chain_safe(initial_url: str, cfg: GuardConfig) -> None:
    """Documented helper. Per-hop redirect enforcement lives in acquire.Fetcher,
    which follows redirects MANUALLY and calls assert_url_safe on every Location
    before issuing the next request (follow_redirects=False on the httpx client).
    This function exists so the invariant has a named anchor; it validates only
    the initial hop. Real chain safety = the manual loop in Fetcher.fetch.
    """
    assert_url_safe(initial_url, cfg)
