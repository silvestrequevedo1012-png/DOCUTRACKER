"""Document request aggregate: request, requirements, uploaded files, status history."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Index,
                        Integer, String, Text, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin, enum_type
from utils.constants import RequestStatus, RequirementStatus

if TYPE_CHECKING:
    from models.document_type import DocumentType
    from models.payment import Payment
    from models.student import Student
    from models.user import User


class DocumentRequest(TimestampMixin, Base):
    __tablename__ = "document_requests"
    __table_args__ = (
        CheckConstraint("copies >= 1", name="ck_document_requests_copies_positive"),
        Index("ix_document_requests_student_status", "student_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reference_number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    document_type_id: Mapped[int] = mapped_column(
        ForeignKey("document_types.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    assigned_registrar_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    copies: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[RequestStatus] = mapped_column(
        enum_type(RequestStatus), default=RequestStatus.SUBMITTED, index=True, nullable=False
    )
    remarks: Mapped[str | None] = mapped_column(Text)
    # Opaque token embedded in the QR code for public verification (Phase 7).
    qr_token: Mapped[str | None] = mapped_column(String(64), unique=True)
    released_file_path: Mapped[str | None] = mapped_column(String(500))
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    student: Mapped["Student"] = relationship(back_populates="requests")
    document_type: Mapped["DocumentType"] = relationship(back_populates="requests")
    assigned_registrar: Mapped["User | None"] = relationship(foreign_keys=[assigned_registrar_id])
    requirements: Mapped[list["RequestRequirement"]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )
    files: Mapped[list["UploadedFile"]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )
    status_history: Mapped[list["RequestStatusHistory"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        order_by="RequestStatusHistory.created_at",
    )

    def __repr__(self) -> str:
        return f"<DocumentRequest ref={self.reference_number!r} status={self.status.value}>"


class RequestRequirement(TimestampMixin, Base):
    __tablename__ = "request_requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("document_requests.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[RequirementStatus] = mapped_column(
        enum_type(RequirementStatus), default=RequirementStatus.PENDING, nullable=False
    )
    reviewer_remarks: Mapped[str | None] = mapped_column(Text)

    request: Mapped["DocumentRequest"] = relationship(back_populates="requirements")
    files: Mapped[list["UploadedFile"]] = relationship(back_populates="requirement")


class UploadedFile(TimestampMixin, Base):
    __tablename__ = "uploaded_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("document_requests.id", ondelete="CASCADE"), index=True, nullable=False
    )
    requirement_id: Mapped[int | None] = mapped_column(
        ForeignKey("request_requirements.id", ondelete="SET NULL"), index=True
    )
    uploaded_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)

    request: Mapped["DocumentRequest"] = relationship(back_populates="files")
    requirement: Mapped["RequestRequirement | None"] = relationship(back_populates="files")
    uploaded_by: Mapped["User | None"] = relationship(foreign_keys=[uploaded_by_id])


class RequestStatusHistory(Base):
    """Append-only log of status transitions (only created_at, no updates)."""

    __tablename__ = "request_status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("document_requests.id", ondelete="CASCADE"), index=True, nullable=False
    )
    from_status: Mapped[RequestStatus | None] = mapped_column(enum_type(RequestStatus))
    to_status: Mapped[RequestStatus] = mapped_column(enum_type(RequestStatus), nullable=False)
    changed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    remarks: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    request: Mapped["DocumentRequest"] = relationship(back_populates="status_history")
    changed_by: Mapped["User | None"] = relationship(foreign_keys=[changed_by_id])
