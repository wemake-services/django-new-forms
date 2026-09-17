from typing import final


@final
class FormConfigurationError(TypeError):
    """Raised when a concrete modern form is configured incorrectly."""


@final
class ParsedDataUnavailableError(AttributeError):
    """Raised when parsed data is requested before successful validation."""
