"""Input validation: simple helpers plus Pydantic schemas."""
from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator
from pydantic import ValidationError as PydanticValidationError

from utils.constants import UserRole
from utils.exceptions import ValidationError

_STUDENT_NO = re.compile(r"^[A-Za-z0-9\-]{4,30}$")
_PHONE = re.compile(r"^\+?[0-9\s\-]{7,20}$")


def is_valid_student_number(value: str) -> bool:
    return bool(_STUDENT_NO.fullmatch(value or ""))


def is_valid_phone(value: str) -> bool:
    return bool(_PHONE.fullmatch(value or ""))


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if len(password) > 128:
        raise ValueError("Password must be at most 128 characters long.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain a lowercase letter.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain an uppercase letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain a number.")
    return password


class LoginInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def _lower_email(cls, v: str) -> str:
        return v.lower()


class RegisterInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    student_number: str
    course: str = Field(min_length=2, max_length=150)
    year_level: int = Field(ge=1, le=8)
    contact_number: str | None = None
    password: str
    confirm_password: str

    @field_validator("email")
    @classmethod
    def _lower_email(cls, v: str) -> str:
        return v.lower()

    @field_validator("student_number")
    @classmethod
    def _student_number(cls, v: str) -> str:
        if not is_valid_student_number(v):
            raise ValueError("Use 4-30 letters, numbers or dashes.")
        return v

    @field_validator("contact_number")
    @classmethod
    def _contact(cls, v: str | None) -> str | None:
        if not v:
            return None
        if not is_valid_phone(v):
            raise ValueError("Enter a valid phone number.")
        return v

    @field_validator("password")
    @classmethod
    def _password(cls, v: str) -> str:
        return validate_password_strength(v)

    @model_validator(mode="after")
    def _passwords_match(self) -> "RegisterInput":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


class CreateStaffInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str
    role: UserRole

    @field_validator("email")
    @classmethod
    def _lower_email(cls, v: str) -> str:
        return v.lower()

    @field_validator("password")
    @classmethod
    def _password(cls, v: str) -> str:
        return validate_password_strength(v)

    @field_validator("role")
    @classmethod
    def _staff_role(cls, v: UserRole) -> UserRole:
        if v not in (UserRole.REGISTRAR, UserRole.ADMIN):
            raise ValueError("Staff accounts must be registrar or admin.")
        return v


_LABELS = {
    "first_name": "First name", "last_name": "Last name", "email": "Email",
    "student_number": "Student number", "course": "Course", "year_level": "Year level",
    "contact_number": "Contact number", "password": "Password",
    "confirm_password": "Confirm password", "role": "Role",
}


def parse_input(schema: type[BaseModel], data: dict):
    """Validate raw data; raise our ValidationError with a friendly message."""
    try:
        return schema(**data)
    except PydanticValidationError as exc:
        err = exc.errors()[0]
        field = str(err["loc"][-1]) if err.get("loc") else ""
        message = str(err["msg"]).removeprefix("Value error, ")
        if err["type"] == "missing" or (err["type"] == "string_too_short" and err.get("input") == ""):
            message = "This field is required."
        elif "valid email" in message.lower() or err["type"] == "value_error" and field == "email":
            message = "Enter a valid email address."
        label = _LABELS.get(field)
        raise ValidationError(f"{label}: {message}" if label else message) from exc
