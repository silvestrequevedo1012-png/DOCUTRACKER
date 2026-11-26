from __future__ import annotations

from typing import Callable

import flet as ft

from components.auth_card import auth_card, primary_button_style
from utils.constants import Palette


def build_register_view(
    page: ft.Page,
    on_submit: Callable[[dict], str | None],
    on_back_click: Callable[[], None],
) -> ft.Control:
    """`on_submit(values)` returns an error message, or None on success."""
    first = ft.TextField(label="First name", expand=True)
    last = ft.TextField(label="Last name", expand=True)
    email = ft.TextField(label="Email address", keyboard_type=ft.KeyboardType.EMAIL)
    number = ft.TextField(label="Student number", hint_text="e.g. 2024-00123")
    course = ft.TextField(label="Course / Program", hint_text="e.g. BS Computer Science")
    year = ft.Dropdown(
        label="Year level", value="1", expand=True,
        options=[ft.DropdownOption(key=str(i), text=f"Year {i}") for i in range(1, 7)],
    )
    contact = ft.TextField(label="Contact number (optional)", keyboard_type=ft.KeyboardType.PHONE,
                           expand=True)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True,
                            helper="8+ characters with upper, lower case and a number")
    confirm = ft.TextField(label="Confirm password", password=True, can_reveal_password=True)
    error = ft.Text("", size=13, color=Palette.DANGER, visible=False)
    spinner = ft.ProgressRing(width=18, height=18, stroke_width=2, visible=False)

    def handle(e=None) -> None:
        submit.disabled = True
        spinner.visible = True
        error.visible = False
        page.update()
        problem = on_submit({
            "first_name": first.value or "", "last_name": last.value or "",
            "email": email.value or "", "student_number": number.value or "",
            "course": course.value or "", "year_level": year.value or "",
            "contact_number": contact.value or "", "password": password.value or "",
            "confirm_password": confirm.value or "",
        })
        if problem:  # on success the router has already moved to the login screen
            error.value = problem
            error.visible = True
            submit.disabled = False
            spinner.visible = False
            page.update()

    submit = ft.Button(content="Create account", style=primary_button_style(), on_click=handle)

    return auth_card(
        "Create your account",
        "Student registration",
        [
            ft.Row([first, last]),
            email,
            number,
            course,
            ft.Row([year, contact]),
            password,
            confirm,
            error,
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[submit, spinner]),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Text("Already registered?", size=13),
                    ft.TextButton("Sign in", on_click=lambda e: on_back_click()),
                ],
            ),
        ],
        width=520,
    )
