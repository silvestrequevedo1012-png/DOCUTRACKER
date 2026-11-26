"""Role-based access checks. Called from controllers AND services (defence in depth)."""
from __future__ import annotations

from middleware.authentication import AuthenticatedUser
from utils.constants import UserRole
from utils.exceptions import AuthenticationError, AuthorizationError


def require_authenticated(actor: AuthenticatedUser | None) -> AuthenticatedUser:
    if actor is None:
        raise AuthenticationError("Your session has expired. Please sign in again.")
    return actor


def require_role(actor: AuthenticatedUser | None, *roles: UserRole) -> AuthenticatedUser:
    user = require_authenticated(actor)
    if user.role not in roles:
        raise AuthorizationError()
    return user
