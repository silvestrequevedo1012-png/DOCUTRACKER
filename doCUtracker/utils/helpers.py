"""Small reusable helpers (logging setup, time, error formatting)."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils.exceptions import DocuTrackError


def configure_logging(level: str = "INFO", log_dir: Path | None = None) -> None:
    """Configure console + rotating file logging (idempotent)."""
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(level)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    root.addHandler(console)

    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / "docutrack.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def user_message_for(exc: Exception) -> str:
    """Centralised mapping from exception to a safe, user-facing message."""
    if isinstance(exc, DocuTrackError):
        return exc.message
    logging.getLogger(__name__).exception("Unhandled exception", exc_info=exc)
    return "Something went wrong. Please try again or contact support."
