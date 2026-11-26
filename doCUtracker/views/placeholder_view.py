from __future__ import annotations

import flet as ft

from utils.constants import Palette


def build_placeholder(title: str, phase: int) -> ft.Control:
    return ft.Container(
        padding=40,
        bgcolor=Palette.WHITE,
        border_radius=12,
        border=ft.Border.all(1, Palette.BORDER),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.CONSTRUCTION, size=40, color=Palette.NAVY),
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=Palette.NAVY),
                ft.Text(f"This screen will be built in Phase {phase}.", color=Palette.TEXT),
            ],
        ),
    )
