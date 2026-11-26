from __future__ import annotations

from dataclasses import dataclass

from controllers.base_controller import ActionResult, run_action
from middleware.authentication import AuthenticatedUser, SessionManager
from middleware.authorization import require_authenticated
from services.auth_service import AuthService
from utils.exceptions import AuthenticationError, ValidationError
from utils.validators import CreateStaffInput, LoginInput, RegisterInput, parse_input


@dataclass(frozen=True)
class LoginData:
    token: str
    user: AuthenticatedUser


class AuthController:
    def __init__(self, auth_service: AuthService, sessions: SessionManager) -> None:
        self._service = auth_service
        self._sessions = sessions

    def login(self, email: str, password: str) -> ActionResult:
        def action() -> LoginData:
            data = parse_input(LoginInput, {"email": email, "password": password})
            user = self._service.authenticate(data.email, data.password)
            return LoginData(self._sessions.create(user), user)

        result = run_action(action)
        # Malformed input should not reveal more than a bad login does.
        if not result.success and "Email:" in result.message:
            return ActionResult.fail("Enter a valid email address.")
        return result

    def register(self, **fields: str) -> ActionResult:
        def action() -> int:
            raw = dict(fields)
            try:
                raw["year_level"] = int(raw.get("year_level") or 0)
            except (TypeError, ValueError) as exc:
                raise ValidationError("Year level: select a valid year.") from exc
            data = parse_input(RegisterInput, raw)
            return self._service.register_student(data)

        return run_action(action, "Account created. You can now sign in.")

    def current_user(self, token: str | None) -> ActionResult:
        def action() -> AuthenticatedUser:
            user = self._sessions.get(token)
            if user is None:
                raise AuthenticationError("Your session has expired. Please sign in again.")
            return user

        return run_action(action)

    def logout(self, token: str | None) -> None:
        user = self._sessions.get(token)
        self._sessions.destroy(token)
        if user is not None:
            run_action(lambda: self._service.record_logout(user))

    def create_staff(self, token: str | None, **fields: str) -> ActionResult:
        def action() -> int:
            actor = require_authenticated(self._sessions.get(token))
            data = parse_input(CreateStaffInput, fields)
            return self._service.create_staff_user(actor, data)  # service enforces ADMIN

        return run_action(action, "Staff account created.")
