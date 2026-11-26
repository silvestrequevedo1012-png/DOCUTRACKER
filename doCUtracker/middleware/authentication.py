"""Server-side session management (tokens live in memory on the server side)."""
from __future__ import annotations

import secrets
import threading
from dataclasses import dataclass
from datetime import datetime, timedelta

from utils.constants import UserRole
from utils.helpers import utcnow


@dataclass(frozen=True)
class AuthenticatedUser:
    """Detached, immutable view of the signed-in user (never an ORM object)."""

    user_id: int
    email: str
    full_name: str
    role: UserRole


class SessionManager:
    """Maps opaque random tokens to authenticated users, with sliding expiry."""

    def __init__(self, timeout_minutes: int) -> None:
        self._timeout = timedelta(minutes=timeout_minutes)
        self._sessions: dict[str, tuple[AuthenticatedUser, datetime]] = {}
        self._lock = threading.Lock()

    def create(self, user: AuthenticatedUser) -> str:
        token = secrets.token_urlsafe(32)
        with self._lock:
            self._sessions[token] = (user, utcnow() + self._timeout)
        return token

    def get(self, token: str | None) -> AuthenticatedUser | None:
        if not token:
            return None
        with self._lock:
            entry = self._sessions.get(token)
            if entry is None:
                return None
            user, expires_at = entry
            now = utcnow()
            if expires_at <= now:
                del self._sessions[token]
                return None
            self._sessions[token] = (user, now + self._timeout)  # sliding expiry
            return user

    def destroy(self, token: str | None) -> None:
        if token:
            with self._lock:
                self._sessions.pop(token, None)
