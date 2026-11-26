from __future__ import annotations

from typing import Callable

import flet as ft

from components.auth_card import auth_card, primary_button_style
from utils.constants import Palette


def build_login_view(
    page: ft.Page,
    on_submit: Callable[[str, str], str | None],
    on_register_click: Callable[[], None],
    notice: str | None = None,
) -> ft.Control:
    """`on_submit` returns an error message, or None when sign-in succeeded."""
    email = ft.TextField(label="Email address", prefix_icon=ft.Icons.EMAIL_OUTLINED,
                         keyboard_type=ft.KeyboardType.EMAIL, autofocus=True)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True,
                            prefix_icon=ft.Icons.LOCK_OUTLINE)
    message = ft.Text(notice or "", size=13, color=Palette.SUCCESS, visible=bool(notice))
    spinner = ft.ProgressRing(width=18, height=18, stroke_width=2, visible=False)

    def handle(e=None) -> None:
        sign_in.disabled = True
        spinner.visible = True
        message.visible = False
        page.update()
        error = on_submit(email.value or "", password.value or "")
        if error:  # on success the router has already replaced this screen
            message.value = error
            message.color = Palette.DANGER
            message.visible = True
            sign_in.disabled = False
            spinner.visible = False
            page.update()

    password.on_submit = handle
    email.on_submit = handle
    sign_in = ft.Button(content="Sign in", style=primary_button_style(), on_click=handle)

    return auth_card(
        "Welcome to DocuTrack",
        "School Document Request and Tracking System",
        [
            email,
            password,
            message,
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[sign_in, spinner]),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Text("New student?", size=13),
                    ft.TextButton("Create an account", on_click=lambda e: on_register_click()),
                ],
            ),
        ],
    )
