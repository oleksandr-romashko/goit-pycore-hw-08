"""
Decorator to handle graceful termination of CLI functions on KeyboardInterrupt.

This module provides a utility decorator that catches keyboard interruptions
(e.g., Ctrl+C) and invokes a user-defined callback for clean exits.
"""
from utils.constants import MSG_INTERRUPTED_BY_USER


def keyboard_interrupt_error(on_interrupt):
    """
    Decorator to handle KeyboardInterrupt exceptions in CLI apps.

    Args:
        on_interrupt (Callable): Function to call on KeyboardInterrupt.
                                 Must accept prefix and suffix keyword arguments.
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except KeyboardInterrupt:
                on_interrupt(prefix="\n", suffix=MSG_INTERRUPTED_BY_USER)

        return inner

    return wrapper
