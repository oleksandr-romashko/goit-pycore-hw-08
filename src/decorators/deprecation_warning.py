"""
Decorator to log usage of deprecated or transitional functions.

Intended for marking temporary functions that are planned for removal or refactoring.
Emits a debug log message each time the function is called.
"""
import functools
import logging

from utils.constants import DEFAULT_TRANSITION_REASON


def transition_warning(
    reason: str = "This function is transitional and will be removed in a future version.",
):
    """
    Decorator to mark functions as deprecated during transition.
    Emits a DeprecationWarning (once per call site) and logs a debug message.

    Args:
        reason (str): Custom deprecation message.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.debug(
                DEFAULT_TRANSITION_REASON,
                func.__name__,
                reason,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
