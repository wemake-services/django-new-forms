"""Django forms for the new_forms app."""

from django import forms


class ContactForm(forms.Form):
    """Form for contact information."""

    name = forms.CharField()
    age = forms.IntegerField()
