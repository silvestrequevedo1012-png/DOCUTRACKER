from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import flet as ft

from utils.constants import Palette, UserRole


@dataclass(frozen=True)
class NavItem:
    key: str
    label: str
    icon: str
    phase: int  # phase in which the screen is built (used by placeholders)


NAV_ITEMS: dict[UserRole, list[NavItem]] = {
    UserRole.STUDENT: [
        NavItem("dashboard", "Dashboard", ft.Icons.DASHBOARD_OUTLINED, 2),
        NavItem("new_request", "New Request", ft.Icons.NOTE_ADD_OUTLINED, 3),
        NavItem("tracking", "Track Requests", ft.Icons.TRACK_CHANGES, 5),
        NavItem("profile", "My Profile", ft.Icons.PERSON_OUTLINE, 3),
    ],
    UserRole.REGISTRAR: [
        NavItem("dashboard", "Dashboard", ft.Icons.DASHBOARD_OUTLINED, 2),
        NavItem("requests", "Requests", ft.Icons.INBOX_OUTLINED, 4),
        NavItem("processing", "Processing", ft.Icons.AUTORENEW, 4),
    ],
    UserRole.ADMIN: [
        NavItem("dashboard", "Dashboard", ft.Icons.DASHBOARD_OUTLINED, 2),
        NavItem("users", "Users", ft.Icons.PEOPLE_OUTLINE, 6),
        NavItem("documents", "Document Types", ft.Icons.FOLDER_OUTLINED, 6),
        NavItem("reports", "Reports", ft.Icons.BAR_CHART, 7),
    ],
}


def build_sidebar(
    items: list[NavItem], selected: str, on_select: Callable[[str], None]
) -> ft.Control:
    def make(item: NavItem) -> ft.Control:
        active = item.key == selected
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=12, horizontal=16),
            border_radius=8,
            bgcolor=Palette.NAVY_LIGHT if active else None,
            ink=True,
            on_click=lambda e, k=item.key: on_select(k),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(item.icon, color=Palette.WHITE, size=20),
                    ft.Text(item.label, color=Palette.WHITE, size=14,
                            weight=ft.FontWeight.W_600 if active else ft.FontWeight.NORMAL),
                ],
            ),
        )

    return ft.Container(
        width=230,
        bgcolor=Palette.NAVY,
        padding=ft.Padding.symmetric(vertical=20, horizontal=12),
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.DESCRIPTION, color=Palette.WHITE),
                        ft.Text("DocuTrack", size=20, weight=ft.FontWeight.BOLD, color=Palette.WHITE),
                    ],
                ),
                ft.Divider(color=Palette.NAVY_LIGHT),
                *[make(i) for i in items],
            ],
        ),
    )
