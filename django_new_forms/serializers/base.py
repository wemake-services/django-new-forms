import abc
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Serializer-independent representation of a validation error."""

    location: tuple[str | int, ...]
    message: str
    code: str | None = None
    context: Mapping[str, Any] | None = None


class BaseSerializer(abc.ABC):
    """Convert submitted Python values into a validated model."""

    validation_error: ClassVar[type[Exception]]

    @classmethod
    @abc.abstractmethod
    def validate_model(cls, model: Any) -> None:
        """Check that this serializer supports the given model type."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_python(
        cls,
        unstructured: Mapping[str, Any],
        model: Any,
        *,
        strict: bool | None,
    ) -> Any:
        """Parse submitted Python values into ``model``."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def serialize_validation_error(
        cls,
        exc: Exception,
    ) -> Sequence[ValidationIssue]:
        """Convert a serializer-specific error into validation issues."""
        raise NotImplementedError
