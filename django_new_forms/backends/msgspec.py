from typing_extensions import final

from django_new_forms.backends.base import BaseBackend


@final
class MsgspecBackend(BaseBackend):
    """Backend for Msgspec."""
