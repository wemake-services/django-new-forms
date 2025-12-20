from typing import final

import pydantic


@final
class ValidationBackendError(Exception):
    """
    Exception raised when validation fails in the backend.

    This exception serves as a bridge between backend-specific
    validation errors (such as `pydantic.ValidationError`) and
    Django's form validation system.
    """

    # TODO: refactor
    def __init__(self, original_exc: pydantic.ValidationError) -> None:
        """Allow to pass original exception."""
        self.original_exc = original_exc
