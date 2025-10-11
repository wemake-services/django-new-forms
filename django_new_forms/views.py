from typing import Generic

from django.forms.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin
from typing_extensions import Any

from django_new_forms.backends import BaseBackend
from django_new_forms.exceptions import ValidationBackendError
from django_new_forms.settings import get_backend
from django_new_forms.typing import ModelT


class ProcessFormView(Generic[ModelT], View):
    """
    Base view for processing forms with external validation backends.

    This view extends Django's generic `View` to handle `form` processing
    using external validation libraries through pluggable backends.
    It validates form data against a specified `model_class` and
    handles validation errors by converting them to Django form errors.
    """

    model_class: type[ModelT]
    model_strict: bool = True

    def post(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        """Process form submission with external `validation_backend`."""
        form = self.get_form()  # type: ignore[attr-defined]
        backend = self.backend()

        try:
            model = backend.validate(self.model_class, form)
        except ValidationBackendError as exc:
            backend.attach_errors(form, exc)
            return self.form_invalid(form)  # type: ignore[attr-defined]
        else:
            return self.model_valid(model, form)

    def model_valid(self, model: ModelT, form: BaseForm) -> HttpResponse:
        """
        Handle valid form data.

        Called when form validation succeeds. Delegates to Django's
        `form_valid()` method for standard form processing.
        """
        return self.form_valid(form)  # type: ignore[attr-defined]

    @property
    def backend(self) -> type[BaseBackend]:
        """
        Get the validation backend class for this view.

        Returns the validation backend specified in `validation_backend`
        attribute, or falls back to the globally configured backend.
        """
        return get_backend()


class BaseFormView(FormMixin, ProcessFormView[ModelT]):
    """A base view for displaying a form."""


class FormView(TemplateResponseMixin, BaseFormView):
    """A view for displaying a form and rendering a template response."""
