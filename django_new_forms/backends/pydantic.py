from typing_extensions import final

from django_new_forms.backends.base import BaseBackend


@final
class PydanticBackend(BaseBackend):
    """Backend for Pydantic."""
