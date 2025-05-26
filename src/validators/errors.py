"""
Custom validation errors module.
"""


class ValidationError(ValueError):
    """Custom error for validation problems."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
