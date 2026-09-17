try:
    import pydantic
except ImportError:  # pragma: no cover
    raise ImportError(
        'Pydantic support requires the pydantic extra: '
        "pip install 'django-new-forms[pydantic]'",
    ) from None

from collections.abc import Mapping, Sequence
from typing import Any, ClassVar

from typing_extensions import override

from django_new_forms.backends.base import BaseBackend, ValidationIssue


class PydanticBackend(BaseBackend):
    """Validate submitted values with a Pydantic type adapter."""

    validation_error: ClassVar[type[Exception]] = pydantic.ValidationError

    @classmethod
    @override
    def validate_model(cls, model: Any) -> None:
        """Ensure that Pydantic can build a validator for ``model``."""
        pydantic.TypeAdapter(model)

    @classmethod
    @override
    def from_python(
        cls,
        unstructured: Mapping[str, Any],
        model: Any,
        *,
        strict: bool | None,
    ) -> Any:
        """Parse submitted values into a Pydantic-supported model."""
        return pydantic.TypeAdapter(model).validate_python(
            unstructured,
            strict=strict,
        )

    @classmethod
    @override
    def normalize_validation_error(
        cls,
        exc: Exception,
    ) -> Sequence[ValidationIssue]:
        """Convert a Pydantic error into backend-independent issues."""
        if not isinstance(exc, pydantic.ValidationError):
            raise TypeError(
                f'Expected pydantic.ValidationError, got {type(exc)!r}',
            )
        return tuple(
            ValidationIssue(
                location=tuple(error['loc']),
                message=error['msg'],
                code=error['type'],
                context=error.get('ctx'),
            )
            for error in exc.errors(
                include_url=False,
                include_context=True,
            )
        )
