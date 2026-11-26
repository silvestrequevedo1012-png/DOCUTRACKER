"""Import every model so SQLAlchemy / Alembic see the full metadata."""
from models.audit_log import AuditLog
from models.document_request import (DocumentRequest, RequestRequirement,
                                     RequestStatusHistory, UploadedFile)
from models.document_type import DocumentType
from models.notification import Notification
from models.payment import Payment
from models.registrar import StaffAssignment
from models.student import Student
from models.user import User

__all__ = [
    "AuditLog", "DocumentRequest", "RequestRequirement", "RequestStatusHistory",
    "UploadedFile", "DocumentType", "Notification", "Payment", "StaffAssignment",
    "Student", "User",
]
