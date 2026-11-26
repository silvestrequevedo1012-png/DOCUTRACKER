"""Database engine / session management. Instances are injected, not global."""
from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from config import Settings
from utils.exceptions import DatabaseError

logger = logging.getLogger(__name__)


class Database:
    """Owns the SQLAlchemy engine and session factory."""

    def __init__(self, settings: Settings) -> None:
        url = settings.database_url
        is_sqlite = url.startswith("sqlite")

        kwargs: dict = {"echo": settings.db_echo, "future": True}
        if is_sqlite:
            kwargs["connect_args"] = {"check_same_thread": False}
        else:
            kwargs.update(
                pool_size=settings.db_pool_size,
                max_overflow=settings.db_max_overflow,
                pool_pre_ping=True,
            )

        self._engine: Engine = create_engine(url, **kwargs)

        if is_sqlite:
            # SQLite ignores foreign keys unless this is enabled per connection.
            @event.listens_for(self._engine, "connect")
            def _enable_foreign_keys(dbapi_conn, _record) -> None:
                cur = dbapi_conn.cursor()
                cur.execute("PRAGMA foreign_keys=ON")
                cur.close()

        self._session_factory = sessionmaker(
            bind=self._engine, autoflush=False, expire_on_commit=False, future=True
        )

    @property
    def engine(self) -> Engine:
        return self._engine

    def new_session(self) -> Session:
        return self._session_factory()

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        """Transactional scope: commit on success, rollback on any error."""
        session = self.new_session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as exc:
            session.rollback()
            logger.exception("Database transaction failed")
            raise DatabaseError() from exc
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def check_connection(self) -> bool:
        """Return True if the database answers a trivial query."""
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            logger.exception("Database connectivity check failed")
            return False

    def dispose(self) -> None:
        self._engine.dispose()