from __future__ import annotations

import flet as ft

from components.dashboard_card import dashboard_card
from middleware.authentication import AuthenticatedUser
from utils.constants import Palette


def build_registrar_dashboard(user: AuthenticatedUser) -> ft.Control:
    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(f"Welcome, {user.full_name}", size=22, weight=ft.FontWeight.BOLD, color=Palette.NAVY),
            ft.Text("Request queues appear here once request processing is built (Phase 4).",
                    size=13, color=Palette.TEXT),
            ft.Row(wrap=True, spacing=16, run_spacing=16, controls=[
                dashboard_card("New requests", "0", ft.Icons.INBOX_OUTLINED),
                dashboard_card("Awaiting payment", "0", ft.Icons.PAYMENTS_OUTLINED, Palette.WARNING),
                dashboard_card("In processing", "0", ft.Icons.AUTORENEW, Palette.ACCENT),
                dashboard_card("Ready for release", "0", ft.Icons.CHECK_CIRCLE_OUTLINE, Palette.SUCCESS),
            ]),
        ],
    )
