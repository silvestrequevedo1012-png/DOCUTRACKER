from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select

from models.user import User
from repositories.base_repository import BaseRepository
from utils.constants import UserRole


class UserRepository(BaseRepository):
    def get_by_id(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self._session.scalar(select(User).where(User.email == email.lower()))

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def exists_with_role(self, role: UserRole) -> bool:
        count = self._session.scalar(select(func.count(User.id)).where(User.role == role))
        return bool(count)

    def add(self, user: User) -> User:
        self._session.add(user)
        self._session.flush()
        return user

    def touch_login(self, user: User, when: datetime, new_hash: str | None = None) -> None:
        user.last_login_at = when
        if new_hash:
            user.password_hash = new_hash
