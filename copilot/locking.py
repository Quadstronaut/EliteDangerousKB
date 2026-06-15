"""copilot/locking.py — Cross-process exclusive lock via OS byte-range locking.

Uses the OS-native advisory byte-range lock (``msvcrt.locking`` on Windows,
``fcntl.flock`` on POSIX) on a persistent lock file. This is structurally immune
to the failure class that broke the earlier O_EXCL-token + stale-reclaim approach
on Windows:

  * NO double-grant — the OS arbitrates a 1-byte exclusive lock; at most one open
    handle holds it at a time, even across processes. (The token approach could
    reclaim a still-live token under load and let two processes into the critical
    section, silently losing a seen.json write.)
  * NO stale-reclaim race — when a holder process dies, the OS releases its locks
    automatically. There is no PID-liveness probe to get wrong and no token file
    to delete, so there is no NTFS delete-pending window (which previously killed
    legitimate waiters with a spurious EACCES and caused lost updates).

The lock file is created once (``O_CREAT``, never ``O_EXCL``) and NEVER deleted,
so every contender locks byte 0 of the SAME inode. It is empty/inert and is
gitignored (``*.lock``).

Within one process, a ``threading.Lock`` per path serialises threads, and a
``threading.local`` depth counter makes the lock reentrant — Windows refuses a
second byte-range lock on the same region even from the same process, so we must
not take the OS lock twice in one thread.

``file_lock(lock_path, *, timeout=10.0, poll_interval=0.05, stale_after=60.0)``
  ``stale_after`` is accepted for API/back-compat but is unused: OS auto-release
  on process death supersedes manual staleness reclaim.
"""
from __future__ import annotations

import contextlib
import os
import threading
import time
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# Public exceptions
# ---------------------------------------------------------------------------

class LockError(Exception):
    """Base class for all locking errors."""


class LockTimeout(LockError):
    """Raised when file_lock cannot acquire the lock before the deadline."""


# ---------------------------------------------------------------------------
# OS byte-range lock primitives (the cross-process arbiter)
# ---------------------------------------------------------------------------

if os.name == "nt":
    import msvcrt

    def _os_try_lock(fd: int) -> None:
        """Acquire a 1-byte exclusive lock at offset 0, non-blocking.

        Raises OSError if the region is already locked by another handle.
        """
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)

    def _os_unlock(fd: int) -> None:
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
else:
    import fcntl

    def _os_try_lock(fd: int) -> None:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _os_unlock(fd: int) -> None:
        fcntl.flock(fd, fcntl.LOCK_UN)


# ---------------------------------------------------------------------------
# Per-process, per-path in-process mutex + reentrancy
# ---------------------------------------------------------------------------

_registry_guard = threading.Lock()
_path_mutexes: dict[str, threading.Lock] = {}
_thread_local = threading.local()


def _norm(lock_path: str | Path) -> str:
    """Canonical per-process registry key for a lock path.

    abspath + normcase (never realpath — realpath on a non-existent Windows path
    can return internal NTFS paths and split one logical lock into several keys,
    defeating the in-process mutex). Strips the \\\\?\\ extended-length prefix.
    """
    s = os.path.abspath(str(lock_path))
    if s.startswith("\\\\?\\"):
        s = s[4:]
    return os.path.normcase(s)


def _get_path_mutex(norm: str) -> threading.Lock:
    with _registry_guard:
        m = _path_mutexes.get(norm)
        if m is None:
            m = threading.Lock()
            _path_mutexes[norm] = m
        return m


def _depth(norm: str) -> int:
    return getattr(_thread_local, "depths", {}).get(norm, 0)


def _depth_inc(norm: str) -> None:
    if not hasattr(_thread_local, "depths"):
        _thread_local.depths = {}
    _thread_local.depths[norm] = _thread_local.depths.get(norm, 0) + 1


def _depth_dec(norm: str) -> None:
    depths = getattr(_thread_local, "depths", {})
    if depths.get(norm, 0) <= 1:
        depths.pop(norm, None)
    else:
        depths[norm] = depths[norm] - 1


# ---------------------------------------------------------------------------
# Public context manager
# ---------------------------------------------------------------------------

@contextlib.contextmanager
def file_lock(
    lock_path: str | Path,
    *,
    timeout: float = 10.0,
    poll_interval: float = 0.05,
    stale_after: float = 60.0,
) -> Iterator[None]:
    """Cross-process, crash-safe exclusive lock (OS byte-range lock).

    Usage::

        with file_lock(path / "foo.lock", timeout=10.0):
            # critical section — at most one process+thread is here

    timeout <= 0 raises LockTimeout immediately. A holder that dies releases the
    lock automatically (OS-enforced). ``stale_after`` is ignored (kept for
    back-compat with the previous token-based API).
    """
    if timeout <= 0:
        raise LockTimeout(f"file_lock({lock_path!r}): timeout={timeout!r} <= 0, refusing to wait")

    norm = _norm(lock_path)

    # Reentrant within a thread: already held -> just nest, don't re-lock the OS.
    if _depth(norm) > 0:
        _depth_inc(norm)
        try:
            yield
        finally:
            _depth_dec(norm)
        return

    deadline = time.monotonic() + timeout
    mutex = _get_path_mutex(norm)
    remaining = deadline - time.monotonic()
    if remaining <= 0 or not mutex.acquire(timeout=remaining):
        raise LockTimeout(f"file_lock({lock_path!r}): timed out after {timeout}s on the in-process mutex")

    try:
        lock_path_str = str(lock_path)
        Path(lock_path_str).parent.mkdir(parents=True, exist_ok=True)
        # O_CREAT (never O_EXCL): all contenders share the SAME persistent inode.
        fd = os.open(lock_path_str, os.O_CREAT | os.O_RDWR)
        try:
            # Ensure the file has >=1 byte so the byte-range lock has a region on
            # every Windows build (locking beyond EOF is allowed but we don't rely
            # on it). The write is idempotent under concurrent creators.
            try:
                if os.fstat(fd).st_size == 0:
                    os.write(fd, b"\0")
            except OSError:
                pass

            while True:
                try:
                    _os_try_lock(fd)
                    break
                except OSError:
                    # Region held by another handle (or transient) — poll to deadline.
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise LockTimeout(
                            f"file_lock({lock_path!r}): timed out after {timeout}s "
                            "waiting for the cross-process lock"
                        )
                    time.sleep(min(poll_interval, remaining))

            _depth_inc(norm)
            try:
                yield
            finally:
                _depth_dec(norm)
                try:
                    _os_unlock(fd)
                except OSError:
                    pass  # closing fd below also releases the OS lock
        finally:
            os.close(fd)  # releasing the handle releases the lock unconditionally
    finally:
        mutex.release()
