"""Registrar-related entities.

Registrar staff are `users` with role=REGISTRAR. This module holds the
`staff_assignments` table which maps staff to the document types they handle.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from models.document_type import DocumentType
    from models.user import User


class StaffAssignment(TimestampMixin, Base):
    __tablename__ = "staff_assignments"
    __table_args__ = (
        UniqueConstraint("staff_id", "document_type_id", name="uq_staff_assignments_staff_doctype"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    staff_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    document_type_id: Mapped[int] = mapped_column(
        ForeignKey("document_types.id", ondelete="CASCADE"), index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    staff: Mapped["User"] = relationship(back_populates="staff_assignments")
    document_type: Mapped["DocumentType"] = relationship(back_populates="staff_assignments")
