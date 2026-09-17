from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactFormView(FormView[ContactForm]):
    """View for displaying and processing contact form."""

    form_class = ContactForm  # type: ignore[mutable-override]
    template_name = 'new_forms/contact_form.html'  # type: ignore[mutable-override]
    success_url = reverse_lazy('new_forms:contact_form')  # type: ignore[mutable-override]
