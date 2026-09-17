from collections.abc import Mapping
from typing import Any, ClassVar, Generic, TypeVar, final, get_args, get_origin

from django import forms
from django.core.exceptions import ValidationError
from typing_extensions import get_original_bases, override

from django_new_forms.backends import BaseBackend, ValidationIssue
from django_new_forms.exceptions import (
    FormConfigurationError,
    ParsedDataUnavailableError,
)
from django_new_forms.typing import ModelT


class ModernForm(forms.Form, Generic[ModelT]):  # noqa: WPS214
    """Render Django fields and validate their submitted values externally."""

    backend: ClassVar[type[BaseBackend]]
    model: ClassVar[Any]
    strict: ClassVar[bool | None] = None
    is_abstract: ClassVar[bool] = True

    _parsed_data: ModelT
    _has_parsed_data: bool

    @override
    def __init_subclass__(cls) -> None:
        """Resolve and validate form configuration at class creation time."""
        super().__init_subclass__()
        model = cls._infer_model()
        if model is None:
            cls.is_abstract = True
            return

        backend = getattr(cls, 'backend', None)
        if (
            not isinstance(backend, type)
            or not issubclass(backend, BaseBackend)
            or backend is BaseBackend
        ):
            raise FormConfigurationError(
                f'{cls!r} must define a concrete BaseBackend subclass',
            )

        backend.validate_model(model)
        cls.model = model
        cls.is_abstract = False

    @property
    def parsed_data(self) -> ModelT:
        """Return the externally parsed model after successful validation."""
        if not getattr(self, '_has_parsed_data', False):
            raise ParsedDataUnavailableError(
                'parsed_data is only available after successful validation',
            ) from None
        return self._parsed_data

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
        """Map a backend issue to a Django form field, when possible."""
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
        """Run the configured external validation backend."""
        if self.is_abstract:
            raise FormConfigurationError(
                f'{type(self)!r} is abstract and cannot validate data',
            )

        self._has_parsed_data = False

        try:
            parsed_data = self.backend.from_python(
                self.provide_validation_data(),
                self.model,
                strict=self.strict,
            )
        except self.backend.validation_error as exc:
            for issue in self.backend.normalize_validation_error(exc):
                self.add_error(
                    self.get_error_field(issue),
                    self.format_validation_issue(issue),
                )
        else:
            self._parsed_data = parsed_data
            self._has_parsed_data = True

    @final
    def _post_clean(self) -> None:
        """Skip Django's post-clean validation stage."""

    @classmethod
    def _infer_model(cls) -> Any | None:
        """Infer the closest ``ModernForm`` model type argument."""
        inherited_model = getattr(cls, 'model', None)
        if inherited_model is not None:
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
                    return None
                return model
        return None
