import abc
from typing import Any

from django.forms import BaseForm

from django_new_forms.exceptions import ValidationBackendError
from django_new_forms.typing import ModelT


class BaseBackend(abc.ABC):
    """
    Abstract base class for all validation backends.

    This class defines the interface that all validation backends
    must implement to work with `django-new-forms`.
    Backends are responsible for validating form data against external
    validation libraries (such as `Pydantic`) and converting validation
    errors into Django form errors.
    """

    def __init__(self, model_strict: bool) -> None:  # noqa: FBT001
        """Allow to pass model strict."""
        self.model_strict = model_strict

    @abc.abstractmethod
    def validate(
        self,
        model_class: type[ModelT],
        form: BaseForm,
    ) -> ModelT:
        """
        Validate form data against the given model class.

        This method should validate the form's data against the provided model
        class using the backend's underlying validation library. If validation
        fails, it should raise a `ValidationBackendError` with the original
        validation error as the cause.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def attach_errors(
        self,
        form: BaseForm,
        exc: ValidationBackendError,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Attach validation errors from the backend to a Django form.

        This method converts backend-specific validation errors into Django
        form errors and attaches them to the provided form. The exact format
        of the error attachment depends on the backend implementation.
        """
        raise NotImplementedError
