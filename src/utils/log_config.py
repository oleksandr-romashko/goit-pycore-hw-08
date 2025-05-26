import logging


def init_logging(level: int = logging.INFO):
    """
    Sets up basic logging configuration.

    Args:
        level (int): Logging level, e.g., logging.DEBUG, logging.INFO.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
