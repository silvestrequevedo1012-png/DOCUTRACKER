from __future__ import annotations

from typing import Callable

import flet as ft

from components.navbar import build_navbar
from components.sidebar import NavItem, build_sidebar
from middleware.authentication import AuthenticatedUser
from utils.constants import Palette


def build_app_shell(
    user: AuthenticatedUser,
    nav_items: list[NavItem],
    selected: str,
    on_navigate: Callable[[str], None],
    on_logout: Callable[[], None],
    content: ft.Control,
) -> ft.Control:
    current = next((i for i in nav_items if i.key == selected), nav_items[0])
    return ft.Row(
        expand=True,
        spacing=0,
        controls=[
            build_sidebar(nav_items, selected, on_navigate),
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    build_navbar(current.label, user, on_logout),
                    ft.Container(
                        expand=True,
                        bgcolor=Palette.LIGHT_GRAY,
                        padding=24,
                        content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[content]),
                    ),
                ],
            ),
        ],
    )
