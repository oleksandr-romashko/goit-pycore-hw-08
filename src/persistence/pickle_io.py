"""
Module for basic data persistence using the pickle module.

Provides functions to save and load an AddressBook instance to and from a file
using binary serialization (pickle format).

Note: This module does not handle any exceptions or file-related checks.
It is intended to be used as a low-level I/O layer, with error handling
delegated to higher-level modules.

Functions:
    - save_data: Serialize and save an AddressBook instance to a file.
    - load_data: Deserialize and load an AddressBook instance from a file.
"""

import pickle
from services.address_book.address_book import AddressBook


def load_data(filename: str) -> AddressBook:
    """
    Load and deserialize an AddressBook instance from a file using pickle.

    Args:
        filename (str): The file path to load the data from.

    Returns:
        AddressBook: The deserialized AddressBook instance.

    Raises:
        Any file I/O errors or pickle errors are not handled here
        and will propagate to the caller.
    """
    with open(filename, "rb") as fh:
        return pickle.load(fh)


def save_data(book: AddressBook, filename: str) -> None:
    """
    Serialize and save the AddressBook instance to a file using pickle.

    Args:
        book (AddressBook): The AddressBook instance to save.
        filename (str): The file path where the data will be saved.

    Raises:
        Any file I/O errors or pickle errors are not handled here
        and will propagate to the caller.
    """
    with open(filename, "wb") as fh:
        pickle.dump(book, fh)
