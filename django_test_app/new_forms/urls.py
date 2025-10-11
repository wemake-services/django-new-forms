"""URL configuration for new_forms app."""

from django.urls import path

from .views import ContactFormView

app_name = 'new_forms'

urlpatterns = [
    path('', ContactFormView.as_view(), name='contact_form'),
]
