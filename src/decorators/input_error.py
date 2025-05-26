"""
Provides a decorator for handling common input-related errors in command handlers.
"""
from utils.constants import (
    ERR_KEY_ERROR,
    ERR_INDEX_ERROR,
    ERR_VALUE_ERROR,
)
from validators.errors import ValidationError


def input_error(func):
    """
    Decorator for handling input-related errors in command handler functions.

    It catches and handles the following exceptions:
    - ValidationError: custom validation failure with a meaningful message
    - KeyError: when a requested key (e.g., contact name) is missing
    - IndexError: when not enough arguments are provided
    - ValueError: when an argument cannot be processed due to invalid value
    - TypeError: when an argument is invalid type

    Returns:
        str: A user-friendly error message, or the original function result
             if no exception is raised.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as exc:
            return str(exc)
        except KeyError:
            return ERR_KEY_ERROR
        except IndexError:
            return ERR_INDEX_ERROR
        except ValueError:
            return ERR_VALUE_ERROR
        except TypeError as exc:
            return str(exc)

    return inner
