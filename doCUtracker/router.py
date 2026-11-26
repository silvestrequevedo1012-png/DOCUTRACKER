"""Navigation + session handling for one Flet page (one per connected user)."""
from __future__ import annotations

import logging

import flet as ft

from components.app_shell import build_app_shell
from components.sidebar import NAV_ITEMS
from config import Settings
from controllers.auth_controller import AuthController
from middleware.authentication import AuthenticatedUser
from utils.constants import Palette, UserRole
from views.admin.dashboard_view import build_admin_dashboard
from views.auth.login_view import build_login_view
from views.auth.register_view import build_register_view
from views.placeholder_view import build_placeholder
from views.registrar.dashboard_view import build_registrar_dashboard
from views.student.dashboard_view import build_student_dashboard

logger = logging.getLogger(__name__)

_DASHBOARDS = {
    UserRole.STUDENT: build_student_dashboard,
    UserRole.REGISTRAR: build_registrar_dashboard,
    UserRole.ADMIN: build_admin_dashboard,
}


class AppRouter:
    def __init__(self, page: ft.Page, auth: AuthController, settings: Settings, db_ok: bool) -> None:
        self._page = page
        self._auth = auth
        self._settings = settings
        self._db_ok = db_ok
        self._token: str | None = None

    # -- lifecycle ----------------------------------------------------
    def start(self) -> None:
        page = self._page
        page.title = self._settings.app_name
        page.bgcolor = Palette.LIGHT_GRAY
        page.padding = 0
        page.theme = ft.Theme(color_scheme_seed=Palette.NAVY)
        try:
            page.window.min_width = 900
            page.window.min_height = 600
        except Exception:  # noqa: BLE001 - window options are desktop-only
            pass
        if not self._db_ok:
            self._render(self._fatal("Cannot reach the database. Check DATABASE_URL / DB_* in .env."))
        else:
            self.show_login()

    def _render(self, control: ft.Control) -> None:
        self._page.clean()
        self._page.add(control)
        self._page.update()

    @staticmethod
    def _fatal(message: str) -> ft.Control:
        return ft.Container(
            expand=True, alignment=ft.Alignment.CENTER,
            content=ft.Text(message, color=Palette.DANGER, size=16),
        )

    # -- auth screens -------------------------------------------------
    def show_login(self, notice: str | None = None) -> None:
        self._render(build_login_view(self._page, self._handle_login, self.show_register, notice))

    def show_register(self) -> None:
        self._render(build_register_view(self._page, self._handle_register, self.show_login))

    def _handle_login(self, email: str, password: str) -> str | None:
        result = self._auth.login(email, password)
        if not result.success:
            return result.message
        self._token = result.data.token
        self.show_app("dashboard")
        return None

    def _handle_register(self, values: dict) -> str | None:
        result = self._auth.register(**values)
        if not result.success:
            return result.message
        self.show_login(notice=result.message)
        return None

    def _handle_logout(self) -> None:
        self._auth.logout(self._token)
        self._token = None
        self.show_login(notice="You have been signed out.")

    # -- authenticated area -------------------------------------------
    def show_app(self, route: str = "dashboard") -> None:
        result = self._auth.current_user(self._token)
        if not result.success:  # expired or missing session
            self._token = None
            self.show_login(notice=result.message)
            return
        user: AuthenticatedUser = result.data
        items = NAV_ITEMS[user.role]
        if route == "dashboard":
            content = _DASHBOARDS[user.role](user)
        else:
            item = next((i for i in items if i.key == route), items[0])
            content = build_placeholder(item.label, item.phase)
        self._render(build_app_shell(user, items, route, self.show_app, self._handle_logout, content))
