from __future__ import annotations

from typing import Callable

import flet as ft

from middleware.authentication import AuthenticatedUser
from utils.constants import Palette


def build_navbar(title: str, user: AuthenticatedUser, on_logout: Callable[[], None]) -> ft.Control:
    return ft.Container(
        bgcolor=Palette.WHITE,
        padding=ft.Padding.symmetric(vertical=10, horizontal=24),
        border=ft.Border.only(bottom=ft.BorderSide(1, Palette.BORDER)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=Palette.NAVY),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Column(
                            spacing=0, tight=True, horizontal_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Text(user.full_name, size=13, weight=ft.FontWeight.W_600,
                                        color=Palette.TEXT),
                                ft.Text(user.role.value.capitalize(), size=11, color=Palette.ACCENT),
                            ],
                        ),
                        ft.IconButton(ft.Icons.LOGOUT, tooltip="Sign out", icon_color=Palette.NAVY,
                                      on_click=lambda e: on_logout()),
                    ],
                ),
            ],
        ),
    )
