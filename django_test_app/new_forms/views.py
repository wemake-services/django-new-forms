from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactFormView(FormView[ContactForm]):
    """View for displaying and processing contact form."""

    form_class = ContactForm
    template_name = 'new_forms/contact_form.html'
    success_url = reverse_lazy('new_forms:contact_form')
