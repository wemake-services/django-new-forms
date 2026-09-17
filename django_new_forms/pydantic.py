from typing import ClassVar, Generic

from django_new_forms.backends import BaseBackend
from django_new_forms.backends.pydantic import PydanticBackend
from django_new_forms.forms import ModernForm
from django_new_forms.typing import ModelT


class PydanticForm(ModernForm[ModelT], Generic[ModelT]):
    """Modern form validated exclusively by Pydantic."""

    backend: ClassVar[type[BaseBackend]] = PydanticBackend
