"""Custom exception hierarchy used across all layers."""


class DocuTrackError(Exception):
    """Base class for all application errors. Safe to show `message` to users."""

    default_message = "An unexpected error occurred."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class ConfigurationError(DocuTrackError):
    default_message = "The application is not configured correctly."


class DatabaseError(DocuTrackError):
    default_message = "A database error occurred. Please try again."


class ValidationError(DocuTrackError):
    default_message = "The submitted data is invalid."


class AuthenticationError(DocuTrackError):
    default_message = "Invalid credentials or session expired."


class AuthorizationError(DocuTrackError):
    default_message = "You do not have permission to perform this action."


class NotFoundError(DocuTrackError):
    default_message = "The requested resource was not found."


class ConflictError(DocuTrackError):
    default_message = "The resource already exists or conflicts with another."


class BusinessRuleError(DocuTrackError):
    default_message = "This action is not allowed in the current state."
