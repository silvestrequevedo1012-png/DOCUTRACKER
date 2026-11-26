from __future__ import annotations

import flet as ft

from components.dashboard_card import dashboard_card
from middleware.authentication import AuthenticatedUser
from utils.constants import Palette


def build_admin_dashboard(user: AuthenticatedUser) -> ft.Control:
    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(f"Welcome, {user.full_name}", size=22, weight=ft.FontWeight.BOLD, color=Palette.NAVY),
            ft.Text("System statistics appear here once administration is built (Phase 6).",
                    size=13, color=Palette.TEXT),
            ft.Row(wrap=True, spacing=16, run_spacing=16, controls=[
                dashboard_card("Users", "0", ft.Icons.PEOPLE_OUTLINE),
                dashboard_card("Document types", "0", ft.Icons.FOLDER_OUTLINED, Palette.ACCENT),
                dashboard_card("All requests", "0", ft.Icons.DESCRIPTION_OUTLINED, Palette.WARNING),
                dashboard_card("Audit events", "0", ft.Icons.HISTORY, Palette.SUCCESS),
            ]),
        ],
    )
