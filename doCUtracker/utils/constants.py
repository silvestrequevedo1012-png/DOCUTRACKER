"""Application-wide enumerations and constants."""
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    REGISTRAR = "registrar"
    ADMIN = "admin"


class RequestStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    REQUIREMENTS_NEEDED = "requirements_needed"
    APPROVED = "approved"
    REJECTED = "rejected"
    AWAITING_PAYMENT = "awaiting_payment"
    PAYMENT_VERIFIED = "payment_verified"
    PROCESSING = "processing"
    READY_FOR_RELEASE = "ready_for_release"
    RELEASED = "released"
    CANCELLED = "cancelled"


class RequirementStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    VERIFIED = "verified"
    REJECTED = "rejected"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    CASH = "cash"
    GCASH = "gcash"
    BANK_TRANSFER = "bank_transfer"
    OTHER = "other"


class NotificationType(str, Enum):
    INFO = "info"
    STATUS_UPDATE = "status_update"
    PAYMENT = "payment"
    REQUIREMENT = "requirement"
    RELEASE = "release"


# UI palette (navy / white / light gray)
class Palette:
    NAVY = "#0B2545"
    NAVY_LIGHT = "#13315C"
    ACCENT = "#1F6FEB"
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#F1F3F6"
    BORDER = "#D9DEE5"
    TEXT = "#1B2430"
    SUCCESS = "#2E7D32"
    WARNING = "#ED6C02"
    DANGER = "#C62828"
