from __future__ import annotations

import flet as ft

from utils.constants import Palette


def auth_card(title: str, subtitle: str, controls: list[ft.Control], width: int = 440) -> ft.Control:
    """Centered white card used by the login and registration screens."""
    card = ft.Container(
        width=width,
        padding=32,
        bgcolor=Palette.WHITE,
        border_radius=12,
        border=ft.Border.all(1, Palette.BORDER),
        content=ft.Column(
            tight=True,
            spacing=14,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Icon(ft.Icons.DESCRIPTION, size=36, color=Palette.NAVY)],
                ),
                ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=Palette.NAVY,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(subtitle, size=13, color=Palette.TEXT, text_align=ft.TextAlign.CENTER),
                *controls,
            ],
        ),
    )
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        bgcolor=Palette.LIGHT_GRAY,
        padding=16,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[card],
        ),
    )


def primary_button_style() -> ft.ButtonStyle:
    return ft.ButtonStyle(
        bgcolor=Palette.NAVY,
        color=Palette.WHITE,
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.Padding.symmetric(vertical=14, horizontal=20),
    )
