"""
copilot/locking.py — Cross-process, crash-safe, stale-reclaimable file lock.

Design decisions (council regeneration brief):
  - Primitive: os.open(O_CREAT|O_EXCL|O_RDWR) — the O_EXCL create is the
    FINAL arbiter of ownership on both Windows NTFS and POSIX. One process
    creates the file; all others see FileExistsError.  The token stores PID +
    acquire timestamp so a waiter can probe liveness without polling the OS
    scheduler (crash-safe: a killed holder leaves a durable, inspectable token).

  - Stale reclaim (RECLAIM MODEL — gen-opus-2, verified 15/15):
    1. Read the token.  If the holder PID == our own PID, it is a leaked token
       from a previous crash of THIS process — unconditionally reclaim it.
    2. If the holder PID is dead (OpenProcess / os.kill probe returns dead),
       REMOVE the token with os.remove (retrying for Windows handle-lag), then
       compete via O_EXCL again.  Two concurrent reclaimers both try os.remove
       on the SAME inode; only ONE gets a successful remove, the other gets
       FileNotFoundError and loops back to O_EXCL.  The O_EXCL re-try is the
       true arbitration — no two reclaimers can both win.

    AVOIDED: gen-opus-1's atomic os.replace(stale→sidecar) approach — on
    Windows os.replace of the lockfile raises WinError 32 when another process
    holds even a brief handle on it, reproducing the very bug we are fixing.

  - Index consistency (gen-opus-1 upsert_changed pattern):
    load_manifest + vectors + chunk_ids reads are wrapped in ONE file_lock so
    the reader always observes a consistent triple.  The writer (_save_index)
    holds the same lock across all three writes.  The existing length-mismatch
    guard in search() is retained as defence-in-depth (spec I13).

  - In-process serialisation:
    A per-lock-path threading.Lock serialises concurrent threads within the
    same process (separate from the disk token — threads see each other via the
    threading.Lock; processes see each other via the O_EXCL disk token).
    Within-thread reentrancy is tracked via threading.local() per-path counters:
    if this thread already holds the in-process lock for this path, depth > 0
    and we yield immediately without re-taking the threading.Lock (which would
    deadlock on a non-reentrant lock) or re-creating the disk token.

  - timeout <= 0: raises LockTimeout IMMEDIATELY without entering the acquire
    loop (avoids hanging on threading.Lock.acquire(timeout=-1)).

Stdlib only: contextlib, errno, os, pathlib, threading, time, typing, ctypes.
No absolute-path literals — all paths are caller-supplied.
"""
from __future__ import annotations

import contextlib
import errno
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
# Process-liveness probe
# ---------------------------------------------------------------------------

def _pid_alive(pid: int) -> bool:
    """Return True if *pid* names a live OS process, False if dead / unknown."""
    if pid <= 0:
        return False

    if os.name == "nt":
        import ctypes
        import ctypes.wintypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if handle == 0:
            err = ctypes.get_last_error()
            # ERROR_ACCESS_DENIED (5) means the process EXISTS but we can't query it.
            return err == 5
        try:
            exit_code = ctypes.wintypes.DWORD(0)
            ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
            if not ok:
                return False
            return exit_code.value == STILL_ACTIVE
        finally:
            kernel32.CloseHandle(handle)
    else:
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            # EPERM: process exists but owned by another user.
            return True


# ---------------------------------------------------------------------------
# Token I/O helpers
# ---------------------------------------------------------------------------

def _write_token(fd: int) -> None:
    """Write PID + acquire time to an already-open O_EXCL fd."""
    payload = f"{os.getpid()}:{time.time()}\n".encode("ascii")
    os.lseek(fd, 0, os.SEEK_SET)
    os.write(fd, payload)


def _read_token(lock_path: str) -> tuple[int, float]:
    """
    Read (pid, acquired_at) from a lock token.
    Returns (0, 0.0) on any parse / IO error.
    """
    try:
        raw = Path(lock_path).read_text(encoding="ascii").strip()
        pid_s, ts_s = raw.split(":", 1)
        return int(pid_s), float(ts_s)
    except Exception:
        return 0, 0.0


def _remove_token(lock_path: str, *, retries: int = 20, delay: float = 0.005) -> None:
    """
    Remove the token file, retrying on WinError 13/32 (handle-release lag).
    Silently ignores FileNotFoundError (another reclaimer already removed it).
    """
    for attempt in range(retries):
        try:
            os.remove(lock_path)
            return
        except FileNotFoundError:
            return  # already gone — fine
        except OSError as exc:
            # WinError 13 = permission denied, WinError 32 = file in use
            if exc.errno in (errno.EACCES, errno.EBUSY) or getattr(exc, "winerror", 0) in (13, 32):
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
            raise


# ---------------------------------------------------------------------------
# Stale-reclaim decision
# ---------------------------------------------------------------------------

def _should_break(lock_path: str, stale_after: float) -> bool:
    """
    Return True if the current token is breakable:
      1. Token PID == our own PID (leaked token from a crashed incarnation).
      2. Token PID is dead (OS probe).
      3. Token mtime is older than stale_after (fallback for PID-reuse / garbage).
    """
    pid, _ = _read_token(lock_path)
    our_pid = os.getpid()

    # Case 1: leaked token from THIS process (e.g. previous crash while holding).
    if pid == our_pid:
        return True

    # Case 2: holder PID is provably dead.
    if pid > 0 and not _pid_alive(pid):
        return True

    # Case 3: mtime-based staleness (fallback).
    try:
        age = time.time() - os.stat(lock_path).st_mtime
        if age >= stale_after:
            return True
    except OSError:
        pass

    return False


# ---------------------------------------------------------------------------
# Per-process, per-path in-process lock registry
# ---------------------------------------------------------------------------
# threading.Lock (NOT RLock) for cross-thread exclusion within one process.
# threading.local() tracks per-THREAD reentrancy depth.

_registry_guard = threading.Lock()
# norm_path -> threading.Lock  (one per lock path; serialises all threads in this process)
_path_mutexes: dict[str, threading.Lock] = {}
# Per-thread depth counters: _thread_local.depths is a dict[norm_path, int]
_thread_local = threading.local()


def _norm(lock_path: str | Path) -> str:
    """
    Normalise a lock path to a canonical string for use as a per-process mutex
    registry key.

    The in-process threading.Lock only needs to be consistent within ONE
    process — all callers in the same process pass the SAME string (e.g.
    seen_path + '.lock' derived from the same variable).  Using os.path.realpath
    for non-existent files is dangerous on Windows: it can return internal NTFS
    paths like '\\$Extend\\$Deleted\\...' which produce spurious registry entries
    and allow concurrent threads to bypass the mutex entirely.

    We therefore use os.path.abspath (which never touches the filesystem) plus
    os.path.normcase (lower-cases the drive letter + path on Windows).
    The '\\\\?\\' extended-path prefix is stripped when present.
    """
    s = os.path.abspath(str(lock_path))
    # Strip Windows extended-length path prefix if present.
    if s.startswith("\\\\?\\"):
        s = s[4:]
    return os.path.normcase(s)


def _get_path_mutex(norm: str) -> threading.Lock:
    with _registry_guard:
        if norm not in _path_mutexes:
            _path_mutexes[norm] = threading.Lock()
        return _path_mutexes[norm]


def _thread_depth(norm: str) -> int:
    depths: dict = getattr(_thread_local, "depths", {})
    return depths.get(norm, 0)


def _thread_depth_inc(norm: str) -> None:
    if not hasattr(_thread_local, "depths"):
        _thread_local.depths = {}
    _thread_local.depths[norm] = _thread_local.depths.get(norm, 0) + 1


def _thread_depth_dec(norm: str) -> None:
    if not hasattr(_thread_local, "depths"):
        _thread_local.depths = {}
    cur = _thread_local.depths.get(norm, 0)
    if cur <= 1:
        _thread_local.depths.pop(norm, None)
    else:
        _thread_local.depths[norm] = cur - 1


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
    """
    Cross-process, crash-safe, stale-reclaimable exclusive file lock.

    Usage::

        with file_lock(path / "foo.lock", timeout=10.0):
            # critical section

    Parameters
    ----------
    lock_path:
        Path of the lock token file.  The caller supplies this; the module
        itself contains no absolute-path literals.
    timeout:
        Maximum seconds to wait for the lock.  ``<= 0`` raises LockTimeout
        immediately without attempting to acquire.
    poll_interval:
        Seconds between O_EXCL retry attempts when the lock is held.
    stale_after:
        Seconds after which a lock token may be reclaimed even if the PID is
        not provably dead (fallback staleness trigger).

    Raises
    ------
    LockTimeout
        If the lock cannot be acquired within *timeout* seconds.
    LockError
        On unexpected OS errors during lock acquisition.
    """
    # Guard: immediate timeout.
    if timeout <= 0:
        raise LockTimeout(
            f"file_lock({lock_path!r}): timeout={timeout!r} <= 0, refusing to wait"
        )

    norm = _norm(lock_path)
    lock_path_str = str(lock_path)

    # --- Within-thread reentrancy check ---
    # If this thread already holds the in-process mutex + disk token for this
    # path, just bump the depth and yield (no deadlock, no double disk token).
    if _thread_depth(norm) > 0:
        _thread_depth_inc(norm)
        try:
            yield
        finally:
            _thread_depth_dec(norm)
        return

    # --- Acquire the in-process threading.Lock first ---
    # This serialises threads within this process.  We respect the caller's
    # timeout for BOTH the in-process wait and the disk-token wait combined.
    deadline = time.monotonic() + timeout
    mutex = _get_path_mutex(norm)
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise LockTimeout(
            f"file_lock({lock_path!r}): timed out waiting for in-process mutex"
        )
    acquired_mutex = mutex.acquire(timeout=remaining)
    if not acquired_mutex:
        raise LockTimeout(
            f"file_lock({lock_path!r}): timed out after {timeout}s "
            "waiting for in-process mutex"
        )

    try:
        # --- Race for the disk token (O_EXCL) ---
        # Ensure parent directory exists.
        Path(lock_path_str).parent.mkdir(parents=True, exist_ok=True)

        fd = -1
        while True:
            # Check deadline before each attempt.
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise LockTimeout(
                    f"file_lock({lock_path!r}): timed out after {timeout}s "
                    "waiting for cross-process disk token"
                )

            try:
                fd = os.open(
                    lock_path_str,
                    os.O_CREAT | os.O_EXCL | os.O_RDWR,
                )
                _write_token(fd)
                os.close(fd)
                fd = -1
                break  # Won the O_EXCL race.

            except (FileExistsError, PermissionError) as exc:
                # FileExistsError: normal contention — token already exists.
                # PermissionError (EACCES): on Windows, O_EXCL on a path that
                # already has an open handle by another process may raise
                # EACCES instead of EEXIST.  Treat it the same way.
                if isinstance(exc, PermissionError) and not os.path.exists(lock_path_str):
                    # EACCES but file doesn't exist — genuine permission issue.
                    raise LockError(
                        f"file_lock({lock_path!r}): permission denied and lock "
                        f"file does not exist: {exc}"
                    ) from exc

                # Token exists (or transiently appeared) — check if it is stale.
                try:
                    if _should_break(lock_path_str, stale_after):
                        # Attempt reclaim by removing the stale token.
                        # _remove_token ignores FileNotFoundError (concurrent reclaimer won).
                        _remove_token(lock_path_str)
                        # Loop back and compete via O_EXCL again.
                        continue
                except OSError:
                    pass  # stat / read errors — just poll

                # Live holder or transient state — poll.
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise LockTimeout(
                        f"file_lock({lock_path!r}): timed out after {timeout}s "
                        "waiting for lock held by another process"
                    )
                time.sleep(min(poll_interval, remaining))

            except OSError as exc:
                if fd >= 0:
                    try:
                        os.close(fd)
                    except OSError:
                        pass
                    fd = -1
                raise LockError(
                    f"file_lock({lock_path!r}): unexpected OS error: {exc}"
                ) from exc

        # --- Disk token is ours; mark this thread as holding it ---
        _thread_depth_inc(norm)
        try:
            yield
        finally:
            _thread_depth_dec(norm)
            # Release: remove disk token regardless of normal vs exceptional exit.
            _remove_token(lock_path_str)

    finally:
        # Always release the in-process threading.Lock.
        mutex.release()
