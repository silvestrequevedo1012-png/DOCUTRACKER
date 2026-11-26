"""Central application configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _get_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer.") from exc


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable '{name}'. "
            "Copy .env.example to .env and fill it in."
        )
    return value


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    debug: bool
    secret_key: str
    log_level: str
    upload_dir: Path

    database_url_override: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    db_pool_size: int
    db_max_overflow: int
    db_echo: bool

    # Security / sessions (Phase 2)
    session_timeout_minutes: int
    max_login_attempts: int
    lockout_minutes: int
    admin_email: str
    admin_password: str

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    smtp_from: str
    smtp_use_tls: bool

    @property
    def database_url(self) -> str:
        """DATABASE_URL wins (e.g. SQLite); otherwise build the PostgreSQL URL."""
        if self.database_url_override:
            return self.database_url_override
        return (
            f"postgresql+psycopg2://{quote_plus(self.db_user)}:"
            f"{quote_plus(self.db_password)}@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Build (once) and return the settings object."""
    return Settings(
        app_name=os.getenv("APP_NAME", "DocuTrack"),
        app_env=os.getenv("APP_ENV", "development"),
        debug=_get_bool("DEBUG", False),
        secret_key=_require("SECRET_KEY"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        upload_dir=BASE_DIR / os.getenv("UPLOAD_DIR", "assets/documents"),
        database_url_override=os.getenv("DATABASE_URL", ""),
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=_get_int("DB_PORT", 5432),
        db_name=os.getenv("DB_NAME", ""),
        db_user=os.getenv("DB_USER", ""),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_pool_size=_get_int("DB_POOL_SIZE", 5),
        db_max_overflow=_get_int("DB_MAX_OVERFLOW", 10),
        db_echo=_get_bool("DB_ECHO", False),
        session_timeout_minutes=_get_int("SESSION_TIMEOUT_MINUTES", 30),
        max_login_attempts=_get_int("MAX_LOGIN_ATTEMPTS", 5),
        lockout_minutes=_get_int("LOCKOUT_MINUTES", 15),
        admin_email=os.getenv("ADMIN_EMAIL", ""),
        admin_password=os.getenv("ADMIN_PASSWORD", ""),
        smtp_host=os.getenv("SMTP_HOST", ""),
        smtp_port=_get_int("SMTP_PORT", 587),
        smtp_user=os.getenv("SMTP_USER", ""),
        smtp_password=os.getenv("SMTP_PASSWORD", ""),
        smtp_from=os.getenv("SMTP_FROM", ""),
        smtp_use_tls=_get_bool("SMTP_USE_TLS", True),
    )
