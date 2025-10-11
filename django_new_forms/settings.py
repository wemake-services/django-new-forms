from typing import Final, cast

from django.conf import settings
from django.utils.module_loading import import_string

from django_new_forms.backends.base import BaseBackend

NEW_FORMS_BACKEND: Final = getattr(
    settings,
    'NEW_FORMS_BACKEND',
    'django_new_forms.backends.pydantic.PydanticBackend',
)


def get_backend() -> type[BaseBackend]:
    """Get the configured validation backend class."""
    return cast(
        type[BaseBackend],
        (
            import_string(NEW_FORMS_BACKEND)
            if isinstance(NEW_FORMS_BACKEND, str)
            else NEW_FORMS_BACKEND
        ),
    )
