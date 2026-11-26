from __future__ import annotations

import flet as ft

from components.dashboard_card import dashboard_card
from middleware.authentication import AuthenticatedUser
from utils.constants import Palette


def build_student_dashboard(user: AuthenticatedUser) -> ft.Control:
    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(f"Welcome, {user.full_name}", size=22, weight=ft.FontWeight.BOLD, color=Palette.NAVY),
            ft.Text("Live request data appears here once document requests are built (Phase 3).",
                    size=13, color=Palette.TEXT),
            ft.Row(wrap=True, spacing=16, run_spacing=16, controls=[
                dashboard_card("My requests", "0", ft.Icons.DESCRIPTION_OUTLINED),
                dashboard_card("In progress", "0", ft.Icons.AUTORENEW, Palette.WARNING),
                dashboard_card("Ready for release", "0", ft.Icons.CHECK_CIRCLE_OUTLINE, Palette.SUCCESS),
                dashboard_card("Notifications", "0", ft.Icons.NOTIFICATIONS_NONE, Palette.ACCENT),
            ]),
        ],
    )
