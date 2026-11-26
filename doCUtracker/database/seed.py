"""Seed the first admin and default document types. Safe to run repeatedly.

Usage (after `alembic upgrade head`):  python -m database.seed
"""
from __future__ import annotations

from decimal import Decimal

from config import get_settings
from container import build_container
from models.document_type import DocumentType
from repositories.document_repository import DocumentRepository
from utils.helpers import configure_logging
from utils.exceptions import ValidationError
from utils.validators import LoginInput, parse_input, validate_password_strength

DEFAULT_DOCUMENT_TYPES = [
    ("TOR", "Transcript of Records", "Official record of grades.", "150.00", 7,
     ["Valid ID", "Clearance form", "Request letter"]),
    ("COE", "Certificate of Enrollment", "Proof of current enrollment.", "50.00", 2, ["Valid ID"]),
    ("COG", "Certificate of Grades", "Grades for a specific term.", "50.00", 2, ["Valid ID"]),
    ("GMC", "Good Moral Certificate", "Certificate of good moral character.", "50.00", 3,
     ["Valid ID", "Clearance form"]),
    ("HD", "Honorable Dismissal", "Required when transferring schools.", "200.00", 5,
     ["Valid ID", "Clearance form", "Request letter"]),
]


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    container = build_container(settings)

    if not settings.admin_email or not settings.admin_password:
        raise SystemExit("Set ADMIN_EMAIL and ADMIN_PASSWORD in .env before seeding.")
    try:
        parse_input(LoginInput, {"email": settings.admin_email, "password": "x"})
    except ValidationError:
        raise SystemExit(
            f"ADMIN_EMAIL '{settings.admin_email}' is not accepted. "
            "Use a normal address such as admin@docutrack.com (.local/.test are rejected)."
        )
    try:
        validate_password_strength(settings.admin_password)
    except ValueError as exc:
        raise SystemExit(f"ADMIN_PASSWORD is too weak: {exc}")

    admin_id = container.auth_service.bootstrap_admin(settings.admin_email, settings.admin_password)
    print("Admin created." if admin_id else "Admin already exists - skipped.")

    created = 0
    with container.database.session_scope() as session:
        repo = DocumentRepository(session)
        for code, name, desc, fee, days, reqs in DEFAULT_DOCUMENT_TYPES:
            if repo.get_by_code(code) is None:
                repo.add(DocumentType(code=code, name=name, description=desc,
                                      fee=Decimal(fee), processing_days=days,
                                      requirements_template=reqs))
                created += 1
    print(f"Document types added: {created}")
    container.database.dispose()


if __name__ == "__main__":
    main()
