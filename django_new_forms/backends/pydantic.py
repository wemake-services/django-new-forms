try:
    import pydantic
except ImportError:  # pragma: no cover
    print(  # noqa: WPS421
        'Looks like `pydantic` is not installed, '
        "consider using `pip install 'django-new-forms[pydantic]'`",
    )
    raise

from typing import Any

from django.forms import BaseForm, forms
from typing_extensions import final, override

from django_new_forms.backends.base import BaseBackend
from django_new_forms.exceptions import ValidationBackendError
from django_new_forms.typing import ModelT


@final
class PydanticBackend(BaseBackend):
    """
    Pydantic validation backend for `django-new-forms`.

    This backend integrates `Pydantic` models with Django `forms`,
    allowing you to validate form data against Pydantic models
    and convert Pydantic validation errors into Django form errors.
    """

    @override
    def validate(self, model_class: type[ModelT], form: BaseForm) -> ModelT:
        """Validate form data against a Pydantic model."""
        try:
            return self._validate_data(model_class, form)
        except pydantic.ValidationError as exc:
            raise ValidationBackendError from exc

    @override
    def attach_errors(
        self,
        form: forms.BaseForm,
        exc: pydantic.ValidationError,
        *,
        include_url: bool = False,  # TODO: d
        include_context: bool = False,
    ) -> None:
        """Attaches pydantic validation errors to Django forms."""
        for err in exc.errors(
            include_url=include_url,
            include_context=include_context,
        ):
            form.add_error(
                str(err['loc'][0]) if err['loc'] else None,
                err['msg'],
            )

    # Private API:
    @final
    def _validate_data(
        self,
        model_class: type[ModelT],
        form: BaseForm,
    ) -> ModelT:
        """Transform form data into pydantic model."""
        converted_values = self._query_dict(form)
        return model_class.model_validate(
            converted_values,
            strict=self.model_strict,
        )

    @final
    def _query_dict(self, form: BaseForm) -> dict[str, Any]:
        """Convert Django form data to a dictionary."""
        result_dict = {}
        for field_name in form.data:
            field_value = form.data.getlist(field_name)  # type: ignore[attr-defined]

            if self._is_multiple_field(form, field_name):
                result_dict[field_name] = field_value
            else:
                result_dict[field_name] = field_value[0]
        return result_dict

    @final
    def _is_multiple_field(self, form: BaseForm, field_name: str) -> bool:
        """Check if a form field is a multiple choice field."""
        return (
            'MultipleChoice'
            in form.fields.get(field_name).__class__.__qualname__
        )
