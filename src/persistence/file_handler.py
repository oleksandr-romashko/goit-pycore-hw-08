"""
High-level persistence layer for AddressBook application.

This module provides safe functions for loading and saving AddressBook data,
with error handling for common file system issues.

Responsibilities:
- Orchestrate loading and saving of AddressBook instances.
- Handle I/O errors gracefully and consistently.
- Expose a safe API for the rest of the application.

Exceptions:
- PersistenceError: Raised for issues during loading or saving (e.g., permissions, invalid path).
"""

import logging

from persistence import pickle_io
from persistence.persistence_error import PersistenceError
from services.address_book.address_book import AddressBook

from utils.constants import (
    DEFAULT_FILENAME,
    MSG_FILE_NO_PERMISSION,
    MSG_FILE_ERR_UNEXPECTED_ERR,
    LOG_FILE_LOAD_SUCCESS,
    LOG_FILE_SAVE_SUCCESS,
    LOG_FILE_NO_FILE_CREATED,
    LOG_FILE_ERR_NO_PERMISSION,
    LOG_FILE_ERR_IS_DIRECTORY,
    LOG_FILE_ERR_OS_ERR,
    LOG_FILE_ERR_UNEXPECTED_ERR,
)


def load_address_book(filename: str = DEFAULT_FILENAME) -> AddressBook:
    """
    Load an AddressBook instance from a file.

    If the file does not exist, return an empty AddressBook.
    For other errors, raise a PersistenceError.

    Args:
        filename (str): The file path to load from. Defaults to DEFAULT_FILENAME.

    Returns:
        AddressBook: The loaded AddressBook instance, or a new one if the file is missing.
    """
    try:
        result = pickle_io.load_data(filename)
        logging.debug(LOG_FILE_LOAD_SUCCESS, filename)
        return result
    except FileNotFoundError:
        # Expected case: no file yet, start fresh
        logging.debug(LOG_FILE_NO_FILE_CREATED)
        return AddressBook()
    except PermissionError as exc:
        logging.error(LOG_FILE_ERR_NO_PERMISSION, filename, "loading")
        raise PersistenceError(MSG_FILE_NO_PERMISSION) from exc
    except IsADirectoryError as exc:
        logging.error(LOG_FILE_ERR_IS_DIRECTORY, filename, "loading")
        raise PersistenceError(MSG_FILE_ERR_UNEXPECTED_ERR.format("loading")) from exc
    except OSError as exc:
        logging.error(LOG_FILE_ERR_OS_ERR, "reading", filename, exc)
        raise PersistenceError(MSG_FILE_ERR_UNEXPECTED_ERR.format("loading")) from exc
    except Exception as exc:
        logging.error(LOG_FILE_ERR_UNEXPECTED_ERR, "loading", filename, exc)
        raise PersistenceError(MSG_FILE_ERR_UNEXPECTED_ERR.format("loading")) from exc


def save_address_book(book: AddressBook, filename: str = DEFAULT_FILENAME) -> None:
    """
    Save an AddressBook instance to a file.

    Args:
        book (AddressBook): The AddressBook instance to save.
        filename (str): The file path where the data will be saved. Defaults to DEFAULT_FILENAME.

    Raises:
        PersistenceError: If saving fails due to permissions, file errors, or unexpected issues.
    """
    try:
        pickle_io.save_data(book, filename)
        logging.debug(LOG_FILE_SAVE_SUCCESS, filename)
    except PermissionError as exc:
        logging.error(LOG_FILE_ERR_NO_PERMISSION, filename, "saving")
        raise PersistenceError(MSG_FILE_NO_PERMISSION) from exc
    except IsADirectoryError as exc:
        logging.error(LOG_FILE_ERR_IS_DIRECTORY, filename, "saving")
        raise PersistenceError(MSG_FILE_ERR_UNEXPECTED_ERR.format("saving")) from exc
    except OSError as exc:
        logging.error(LOG_FILE_ERR_OS_ERR, "writing", filename, exc)
        raise PersistenceError(MSG_FILE_ERR_UNEXPECTED_ERR.format("saving")) from exc
    except Exception as exc:
        logging.error(LOG_FILE_ERR_UNEXPECTED_ERR, "saving", filename, exc)
        raise PersistenceError(MSG_FILE_ERR_UNEXPECTED_ERR.format("saving")) from exc
