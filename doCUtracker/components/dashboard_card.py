from __future__ import annotations

import flet as ft

from utils.constants import Palette


def dashboard_card(title: str, value: str, icon: str, color: str = Palette.NAVY) -> ft.Control:
    return ft.Container(
        width=240,
        padding=20,
        bgcolor=Palette.WHITE,
        border_radius=12,
        border=ft.Border.all(1, Palette.BORDER),
        content=ft.Row(
            spacing=16,
            controls=[
                ft.Container(
                    width=48, height=48, border_radius=24, alignment=ft.Alignment.CENTER,
                    bgcolor=Palette.LIGHT_GRAY,
                    content=ft.Icon(icon, color=color, size=24),
                ),
                ft.Column(
                    spacing=2, tight=True,
                    controls=[
                        ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=Palette.TEXT),
                        ft.Text(title, size=12, color=Palette.TEXT),
                    ],
                ),
            ],
        ),
    )
