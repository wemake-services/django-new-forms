from django.views.generic import FormView


class DrawOnlyView(FormView):  # type: ignore[type-arg]
    """View class to run external form validation."""
