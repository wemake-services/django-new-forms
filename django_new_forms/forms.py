from collections.abc import Mapping
from typing import (
    Any,
    ClassVar,
    Generic,
    TypeVar,
    final,
    get_args,
    get_origin,
)

from django import forms
from django.core.exceptions import ValidationError
from typing_extensions import Sentinel, get_original_bases, override

from django_new_forms.exceptions import (
    FormConfigurationError,
    ParsedDataUnavailableError,
)
from django_new_forms.serializers import BaseSerializer, ValidationIssue
from django_new_forms.typing import EMPTY, ModelT


class ModernForm(forms.Form, Generic[ModelT]):  # noqa: WPS214
    """Render Django fields and validate their submitted values externally."""

    serializer: ClassVar[type[BaseSerializer]]
    model: ClassVar[Any | Sentinel] = EMPTY
    strict_validation: ClassVar[bool | None] = None

    _parsed_data: ModelT | Sentinel

    @override
    def __init_subclass__(cls) -> None:
        """Resolve and validate form configuration at class creation time."""
        super().__init_subclass__()
        model = cls._infer_model()
        if model is EMPTY:
            return

        serializer = getattr(cls, 'serializer', None)
        if (
            not isinstance(serializer, type)
            or not issubclass(serializer, BaseSerializer)
            or serializer is BaseSerializer
        ):
            raise FormConfigurationError(
                f'{cls!r} must define a concrete BaseSerializer subclass',
            )

        serializer.validate_model(model)
        cls.model = model

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create a form with no parsed model."""
        super().__init__(*args, **kwargs)
        self._parsed_data = EMPTY

    @property
    def parsed_data(self) -> ModelT:
        """Access to the externally parsed model after successful validation."""
        parsed_data = self._parsed_data
        if parsed_data is EMPTY:
            raise ParsedDataUnavailableError(
                'parsed_data is only available after successful validation',
            ) from None
        return parsed_data  # type: ignore[return-value]

    def provide_validation_data(self) -> Mapping[str, Any]:
        """Extract submitted widget values without Django field validation."""
        validation_data: dict[str, Any] = {}
        for name, field in self.fields.items():
            if field.disabled:
                validation_data[name] = self[name].initial
                continue

            html_name = self.add_prefix(name)
            if field.widget.value_omitted_from_data(
                self.data,
                self.files,
                html_name,
            ):
                continue
            validation_data[name] = field.widget.value_from_datadict(
                self.data,
                self.files,
                html_name,
            )
        return validation_data

    def get_error_field(self, issue: ValidationIssue) -> str | None:
        """Map a serializer issue to a Django form field, when possible."""
        if issue.location:
            candidate = str(issue.location[0])
            if candidate in self.fields:
                return candidate
        return None

    def format_validation_issue(
        self,
        issue: ValidationIssue,
    ) -> ValidationError:
        """Create a Django validation error from a normalized issue."""
        return ValidationError(
            issue.message,
            code=issue.code or 'invalid',
            params=None if issue.context is None else dict(issue.context),
        )

    @final
    def _clean_fields(self) -> None:
        """Skip Django field parsing and validation."""

    @final
    def _clean_form(self) -> None:
        """Run the configured external serializer validation."""
        if self.model is EMPTY:
            raise FormConfigurationError(
                f'{type(self)!r} is abstract and cannot validate data',
            )

        self._parsed_data = EMPTY

        try:
            parsed_data = self.serializer.from_python(
                self.provide_validation_data(),
                self.model,
                strict=self.strict_validation,
            )
        except self.serializer.validation_error as exc:
            for issue in self.serializer.serialize_validation_error(exc):
                self.add_error(
                    self.get_error_field(issue),
                    self.format_validation_issue(issue),
                )
        else:
            self._parsed_data = parsed_data

    @final
    def _post_clean(self) -> None:
        """Skip Django's post-clean validation stage."""

    @classmethod
    def _infer_model(cls) -> Any | Sentinel:
        """Infer the closest ``ModernForm`` model type argument."""
        inherited_model = getattr(cls, 'model', EMPTY)
        if inherited_model is not EMPTY:
            return inherited_model

        for base in get_original_bases(cls):
            origin = get_origin(base)
            arguments = get_args(base)
            if (
                isinstance(origin, type)
                and issubclass(origin, ModernForm)
                and arguments
            ):
                model = arguments[0]
                if isinstance(model, TypeVar):
                    return EMPTY
                return model
        return EMPTY
