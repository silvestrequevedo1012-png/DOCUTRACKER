"""DocuTrack entry point."""
from __future__ import annotations

import logging

import flet as ft

from config import get_settings
from container import AppContainer, build_container
from router import AppRouter
from utils.helpers import configure_logging

logger = logging.getLogger(__name__)


def build_app(container: AppContainer):
    """Create the Flet target. Runs once per connected user/page."""
    db_ok = container.database.check_connection()

    def main(page: ft.Page) -> None:
        AppRouter(page, container.auth_controller, container.settings, db_ok).start()

    return main


def run() -> None:
    settings = get_settings()
    configure_logging(settings.log_level, log_dir=settings.upload_dir.parent.parent / "logs")
    logger.info("Starting %s (%s)", settings.app_name, settings.app_env)
    container = build_container(settings)
    runner = getattr(ft, "run", None) or ft.app  # Flet >=1.0 uses ft.run
    try:
        runner(build_app(container))
    finally:
        container.database.dispose()


if __name__ == "__main__":
    run()
