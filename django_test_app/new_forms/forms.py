"""Django forms for the new_forms app."""

from django import forms

from django_new_forms.pydantic import PydanticForm

from .dtos import ContactDTO


class ContactForm(PydanticForm[ContactDTO]):
    """Form for contact information."""

    name = forms.CharField()
    age = forms.IntegerField()
