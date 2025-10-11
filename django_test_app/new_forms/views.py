from typing import Any

from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy

from django_new_forms.views import FormView

from .dtos import ContactDTO
from .forms import ContactForm


class ContactFormView(FormView[ContactForm, ContactDTO]):
    """View for displaying and processing contact form."""

    form_class = ContactForm
    model_class = ContactDTO
    template_name = 'new_forms/contact_form.html'
    success_url = reverse_lazy('new_forms:contact_form')

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        """Handle GET request."""
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))
