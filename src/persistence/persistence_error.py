"""
Custom persistence error module.
"""


class PersistenceError(Exception):
    """Custom error class for persistence-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
