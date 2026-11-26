from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, JsonType, TimestampMixin

if TYPE_CHECKING:
    from models.document_request import DocumentRequest
    from models.registrar import StaffAssignment


class DocumentType(TimestampMixin, Base):
    __tablename__ = "document_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    processing_days: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    # Template list of requirement names copied into each new request,
    # e.g. ["Valid ID", "Clearance form"].
    requirements_template: Mapped[list] = mapped_column(JsonType, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True, nullable=False)

    requests: Mapped[list["DocumentRequest"]] = relationship(back_populates="document_type")
    staff_assignments: Mapped[list["StaffAssignment"]] = relationship(
        back_populates="document_type", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<DocumentType id={self.id} code={self.code!r}>"
