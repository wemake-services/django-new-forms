from typing_extensions import final


@final
class ValidationBackendError(Exception):
    """
    Exception raised when validation fails in the backend.

    This exception serves as a bridge between backend-specific
    validation errors (such as `pydantic.ValidationError`) and
    Django's form validation system.
    """
