from typing import Any

from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy

from django_new_forms.views import NewFormView

from .dtos import ContactDTO
from .forms import ContactForm


class ContactFormView(NewFormView[ContactForm, ContactDTO]):
    """View for displaying and processing contact form."""

    form_class = ContactForm  # type: ignore[mutable-override]
    model_class = ContactDTO
    template_name = 'new_forms/contact_form.html'  # type: ignore[mutable-override]
    success_url = reverse_lazy('new_forms:contact_form')  # type: ignore[mutable-override]

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        """Handle GET request."""
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))
