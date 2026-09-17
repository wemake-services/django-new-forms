from typing import ClassVar, Generic

from django_new_forms.forms import ModernForm
from django_new_forms.serializers import BaseSerializer
from django_new_forms.serializers.pydantic import PydanticSerializer
from django_new_forms.typing import ModelT


class PydanticForm(ModernForm[ModelT], Generic[ModelT]):
    """Modern form validated exclusively by Pydantic."""

    serializer: ClassVar[type[BaseSerializer]] = PydanticSerializer
