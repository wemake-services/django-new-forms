"""Pydantic schemas for form validation."""

from typing import Final

import pydantic

_MIN_NAME_LENGTH: Final = 2
_MAX_NAME_LENGTH: Final = 100

_MIN_AGE: Final = 0
_MAX_AGE: Final = 120


class ContactDTO(pydantic.BaseModel):
    """DTO for contact information."""

    name: str = pydantic.Field(
        min_length=_MIN_NAME_LENGTH,
        max_length=_MAX_NAME_LENGTH,
    )
    age: int = pydantic.Field(ge=_MIN_AGE, le=_MAX_AGE)
