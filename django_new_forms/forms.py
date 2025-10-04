from django.forms import Form


class DrawOnlyForm(Form):
    """
    Special form that does not validate at all.

    It only renders the content. All validation is external.
    """
