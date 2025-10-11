from django.forms.forms import BaseForm
from typing_extensions import TypeVar

ModelT = TypeVar('ModelT')
FormT = TypeVar('FormT', bound=BaseForm)
