"""Authentication business logic: registration, login, staff creation."""
from __future__ import annotations

import logging
import threading
from datetime import datetime, timedelta

from config import Settings
from database.connection import Database
from middleware.authentication import AuthenticatedUser
from middleware.authorization import require_role
from models.student import Student
from models.user import User
from repositories.audit_repository import AuditRepository
from repositories.student_repository import StudentRepository
from repositories.user_repository import UserRepository
from utils.constants import UserRole
from utils.exceptions import AuthenticationError, ConflictError
from utils.helpers import utcnow
from utils.security import DUMMY_HASH, hash_password, needs_rehash, verify_password
from utils.validators import CreateStaffInput, RegisterInput

logger = logging.getLogger(__name__)

INVALID_CREDENTIALS = "Invalid email or password."


class LoginAttemptTracker:
    """In-memory brute-force protection (per email)."""

    def __init__(self, max_attempts: int, lockout_minutes: int) -> None:
        self._max = max_attempts
        self._lockout = timedelta(minutes=lockout_minutes)
        self._state: dict[str, tuple[int, datetime | None]] = {}
        self._lock = threading.Lock()

    def check(self, key: str) -> None:
        with self._lock:
            count, locked_until = self._state.get(key, (0, None))
            if locked_until is not None:
                remaining = locked_until - utcnow()
                if remaining.total_seconds() > 0:
                    minutes = max(1, int(remaining.total_seconds() // 60) + 1)
                    raise AuthenticationError(
                        f"Too many failed attempts. Try again in {minutes} minute(s)."
                    )
                del self._state[key]  # lockout expired

    def record_failure(self, key: str) -> None:
        with self._lock:
            count, _ = self._state.get(key, (0, None))
            count += 1
            locked_until = utcnow() + self._lockout if count >= self._max else None
            self._state[key] = (count, locked_until)

    def reset(self, key: str) -> None:
        with self._lock:
            self._state.pop(key, None)


class AuthService:
    def __init__(self, database: Database, settings: Settings) -> None:
        self._db = database
        self._tracker = LoginAttemptTracker(settings.max_login_attempts, settings.lockout_minutes)

    # -- registration -------------------------------------------------
    def register_student(self, data: RegisterInput) -> int:
        with self._db.session_scope() as session:
            users, students, audit = (
                UserRepository(session), StudentRepository(session), AuditRepository(session)
            )
            if users.email_exists(data.email):
                raise ConflictError("An account with this email already exists.")
            if students.number_exists(data.student_number):
                raise ConflictError("This student number is already registered.")

            user = users.add(User(
                email=data.email,
                password_hash=hash_password(data.password),
                first_name=data.first_name,
                last_name=data.last_name,
                role=UserRole.STUDENT,
            ))
            students.add(Student(
                user_id=user.id,
                student_number=data.student_number,
                course=data.course,
                year_level=data.year_level,
                contact_number=data.contact_number,
            ))
            audit.log("USER_REGISTERED", user_id=user.id, entity_type="user", entity_id=user.id)
            return user.id

    # -- login --------------------------------------------------------
    def authenticate(self, email: str, password: str, ip: str | None = None) -> AuthenticatedUser:
        key = email.lower()
        self._tracker.check(key)

        failure: str | None = None
        result: AuthenticatedUser | None = None
        with self._db.session_scope() as session:
            users, audit = UserRepository(session), AuditRepository(session)
            user = users.get_by_email(key)
            password_ok = verify_password(user.password_hash if user else DUMMY_HASH, password)

            if user is None or not password_ok:
                failure = INVALID_CREDENTIALS
                audit.log("LOGIN_FAILED", user_id=user.id if user else None,
                          details={"email": key}, ip_address=ip)
            elif not user.is_active:
                failure = "This account has been deactivated. Contact the registrar."
                audit.log("LOGIN_BLOCKED_INACTIVE", user_id=user.id, ip_address=ip)
            else:
                new_hash = hash_password(password) if needs_rehash(user.password_hash) else None
                users.touch_login(user, utcnow(), new_hash)
                audit.log("LOGIN_SUCCESS", user_id=user.id, ip_address=ip)
                result = AuthenticatedUser(user.id, user.email, user.full_name, user.role)

        # Raise outside the transaction so the audit entry is committed.
        if result is None:
            if failure == INVALID_CREDENTIALS:
                self._tracker.record_failure(key)
            raise AuthenticationError(failure or INVALID_CREDENTIALS)
        self._tracker.reset(key)
        return result

    def record_logout(self, actor: AuthenticatedUser) -> None:
        with self._db.session_scope() as session:
            AuditRepository(session).log("LOGOUT", user_id=actor.user_id)

    # -- staff management (admin only, enforced here) -----------------
    def create_staff_user(self, actor: AuthenticatedUser | None, data: CreateStaffInput) -> int:
        admin = require_role(actor, UserRole.ADMIN)
        with self._db.session_scope() as session:
            users, audit = UserRepository(session), AuditRepository(session)
            if users.email_exists(data.email):
                raise ConflictError("An account with this email already exists.")
            user = users.add(User(
                email=data.email,
                password_hash=hash_password(data.password),
                first_name=data.first_name,
                last_name=data.last_name,
                role=data.role,
            ))
            audit.log("STAFF_CREATED", user_id=admin.user_id, entity_type="user",
                      entity_id=user.id, details={"role": data.role.value})
            return user.id

    # -- bootstrap (called only by the seed script) --------------------
    def bootstrap_admin(self, email: str, password: str) -> int | None:
        """Create the first admin if none exists. Returns the new id, else None."""
        with self._db.session_scope() as session:
            users, audit = UserRepository(session), AuditRepository(session)
            if users.exists_with_role(UserRole.ADMIN):
                return None
            user = users.add(User(
                email=email.lower(),
                password_hash=hash_password(password),
                first_name="System",
                last_name="Administrator",
                role=UserRole.ADMIN,
            ))
            audit.log("ADMIN_BOOTSTRAPPED", user_id=user.id, entity_type="user", entity_id=user.id)
            return user.id
