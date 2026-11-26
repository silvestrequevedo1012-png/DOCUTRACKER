from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from utils.exceptions import DocuTrackError
from utils.helpers import user_message_for


@dataclass(frozen=True)
class ActionResult:
    """What controllers hand back to views."""

    success: bool
    message: str = ""
    data: Any = None

    @classmethod
    def ok(cls, data: Any = None, message: str = "") -> "ActionResult":
        return cls(True, message, data)

    @classmethod
    def fail(cls, message: str) -> "ActionResult":
        return cls(False, message)


def run_action(func: Callable[[], Any], success_message: str = "") -> ActionResult:
    """Execute func, converting any exception to a safe ActionResult."""
    try:
        return ActionResult.ok(func(), success_message)
    except DocuTrackError as exc:
        return ActionResult.fail(exc.message)
    except Exception as exc:  # noqa: BLE001 - last line of defence for the UI
        return ActionResult.fail(user_message_for(exc))
