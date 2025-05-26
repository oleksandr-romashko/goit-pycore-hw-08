"""
Provides a decorator for handling common input-related errors in command handlers.
"""
from validators.errors import ValidationError


def service_error(func):
    """
    Decorator for handling service-related errors in a service function.

    It catches and handles the following exceptions:
    - ValidationError: custom validation failure with a meaningful message
    - TypeError: when an argument is invalid type

    Returns:
        dict: A user-friendly error message, or the original function result
             if no exception is raised.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as exc:
            return {"message": str(exc)}
        except TypeError as exc:
            return {"message": str(exc)}

    return inner
