"""Create a registrar (or admin) account by signing in as an administrator.

Usage:
    python -m database.create_staff
    python -m database.create_staff --role admin
"""
from __future__ import annotations

import argparse
from getpass import getpass

from config import get_settings
from container import build_container
from utils.helpers import configure_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a DocuTrack staff account.")
    parser.add_argument("--role", choices=["registrar", "admin"], default="registrar")
    args = parser.parse_args()

    settings = get_settings()
    configure_logging("WARNING")
    container = build_container(settings)
    auth = container.auth_controller

    print("Sign in as an administrator")
    admin_email = input("Admin email: ").strip()
    login = auth.login(admin_email, getpass("Admin password: "))
    if not login.success:
        raise SystemExit(f"Login failed: {login.message}")

    print(f"\nNew {args.role} account")
    first = input("First name: ").strip()
    last = input("Last name: ").strip()
    email = input("Email: ").strip()
    password = getpass("Password (8+ chars, upper, lower, number): ")
    confirm = getpass("Confirm password: ")
    if password != confirm:
        raise SystemExit("Passwords do not match.")

    result = auth.create_staff(
        login.data.token, first_name=first, last_name=last,
        email=email, password=password, role=args.role,
    )
    auth.logout(login.data.token)
    container.database.dispose()
    print(result.message if result.success else f"Failed: {result.message}")


if __name__ == "__main__":
    main()