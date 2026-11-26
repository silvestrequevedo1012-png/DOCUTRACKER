"""Composition root: builds and wires all dependencies once."""
from __future__ import annotations

from dataclasses import dataclass

from config import Settings
from controllers.auth_controller import AuthController
from database.connection import Database
from middleware.authentication import SessionManager
from services.auth_service import AuthService


@dataclass
class AppContainer:
    settings: Settings
    database: Database
    sessions: SessionManager
    auth_service: AuthService
    auth_controller: AuthController


def build_container(settings: Settings) -> AppContainer:
    database = Database(settings)
    sessions = SessionManager(settings.session_timeout_minutes)
    auth_service = AuthService(database, settings)
    return AppContainer(
        settings=settings,
        database=database,
        sessions=sessions,
        auth_service=auth_service,
        auth_controller=AuthController(auth_service, sessions),
    )
