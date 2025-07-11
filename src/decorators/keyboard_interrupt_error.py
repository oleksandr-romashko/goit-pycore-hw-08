"""
Decorator to handle graceful termination of CLI functions on KeyboardInterrupt.

This module provides a utility decorator that catches keyboard interruptions
(e.g., Ctrl+C) and invokes a user-defined callback for clean exits.
"""
import logging

from utils.constants import MSG_INTERRUPTED_BY_USER


def keyboard_interrupt_error(on_interrupt):
    """
    Decorator to handle KeyboardInterrupt exceptions in CLI apps.

    Args:
        on_interrupt (Callable): Function to call when a KeyboardInterrupt is caught.
                                 It must accept `prefix` keyword argument.
    Returns:
        Callable: The decorated function that handles KeyboardInterrupt gracefully.
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except KeyboardInterrupt:
                logging.debug(MSG_INTERRUPTED_BY_USER)
                on_interrupt(prefix="\n")

        return inner

    return wrapper
