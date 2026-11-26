from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from models.document_request import DocumentRequest
    from models.user import User


class Student(TimestampMixin, Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    student_number: Mapped[str] = mapped_column(
        String(30), unique=True, index=True, nullable=False
    )
    course: Mapped[str] = mapped_column(String(150), nullable=False)
    year_level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    contact_number: Mapped[str | None] = mapped_column(String(30))
    address: Mapped[str | None] = mapped_column(Text)
    birth_date: Mapped[date | None] = mapped_column(Date)

    user: Mapped["User"] = relationship(back_populates="student")
    requests: Mapped[list["DocumentRequest"]] = relationship(back_populates="student")

    def __repr__(self) -> str:
        return f"<Student id={self.id} number={self.student_number!r}>"
