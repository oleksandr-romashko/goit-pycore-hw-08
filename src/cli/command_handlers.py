"""
Command handlers for CLI application.

Each handler corresponds to a specific user command and includes input validation,
invokes business logic, and generates an appropriate response.
"""

import sys

from decorators.input_error import input_error
from services.contacts_manager import (
    show_all,
    add_contact,
    change_contact,
    show_phone,
    add_birthday,
    show_birthday,
    show_upcoming_birthdays,
)
from utils.constants import (
    MSG_HELLO_MESSAGE,
    MSG_APP_PURPOSE_MESSAGE,
    MSG_EXIT_MESSAGE,
    MENU_HELP_STR,
    INVALID_COMMAND_MESSAGE,
    MSG_HELP_AWARE_TIP,
)
from utils.text_utils import format_contacts_output, format_text_output
from validators.args_validators import ensure_args_have_n_arguments


# TODO: Optional future enhancement: add handling (delete_contact, remove_phone) functions


def handle_hello() -> str:
    """Returns a greeting message to the user."""
    # No validation checks here
    return f"{MSG_HELLO_MESSAGE}\n{MSG_APP_PURPOSE_MESSAGE}."


@input_error
def handle_all(book: dict) -> str:
    """
    Return a formatted string listing all saved contacts, their phone numbers and birthdays.

    Raises:
        ValidationError: If address book is empty.

    Input data example:
        {
            'Alex': {
                        'name': 'Alex',
                        'phones': ['1234567890', '0000000000'],
                        'birthday': None
                    },
            'Bob': {
                        'name': 'Bob',
                        'phones': ['0987654321'],
                        'birthday': '2010-05-21'
                    }
        }

    Args:
        book (AddressBook): The address book string representation.
    """
    # No validation checks here

    contacts_dict = show_all(book)
    return format_contacts_output(contacts_dict)


@input_error
def handle_add(args: list[str], book: dict) -> str:
    """
    Add a new contact.

    Expected arguments in 'args': [username, phone_number]
    """
    ensure_args_have_n_arguments(args, 2, "username and a phone number")
    username, phone_number = args
    result = add_contact(username, phone_number, book)
    return format_text_output(result)


@input_error
def handle_change(args: list[str], book: dict) -> str:
    """
    Change an existing contact's phone number.

    Expected arguments in 'args': [username, old_phone_number, new_phone_number]
    """
    ensure_args_have_n_arguments(
        args, 3, "username, old phone number and new phone number"
    )
    username, prev_phone_number, new_phone_number = args
    result = change_contact(username, prev_phone_number, new_phone_number, book)
    return format_text_output(result)


@input_error
def handle_phone(args: list[str], book: dict) -> str:
    """
    Return phone numbers for contacts matching the search term (partial match supported).

    Expected arguments in 'args': [search_term]
    """
    ensure_args_have_n_arguments(args, 1, "username")
    # Partial match is supported - the check if username is in the
    # contacts list (with partial match) is not checked by validator and
    # postponed further to the handler
    search_term = args[0]

    result = show_phone(search_term, book)
    return format_text_output(result)


@input_error
def handle_add_birthday(args: list[str], book: dict) -> str:
    """
    Adds a birthday to the specified contact.

    Expected arguments in 'args': [username, date]
    """
    ensure_args_have_n_arguments(args, 2, "username and a birthday")
    username, date = args
    result = add_birthday(username, date, book)
    return format_text_output(result)


@input_error
def handle_show_birthday(args: list[str], book: dict) -> str:
    """
    Displays the birthday of the specified contact.

    Expected arguments in 'args': [username]
    """
    ensure_args_have_n_arguments(args, 1, "username")
    username = args[0]
    result = show_birthday(username, book)
    return format_text_output(result, lines_offset="")


@input_error
def handle_birthdays(book: dict) -> str:
    """Displays all birthdays occurring in the upcoming week."""
    # No validation checks here
    result = show_upcoming_birthdays(book)
    return format_text_output(result)


def handle_help() -> str:
    """Returns formatted help menu."""
    # No validation here
    return MENU_HELP_STR


def handle_exit(prefix="", suffix=""):
    """Print a farewell message and terminate the program."""
    # No validation here
    print(f"{prefix}{MSG_EXIT_MESSAGE}{f' {suffix}' if suffix else ''}")
    sys.exit(0)


def handle_unknown() -> str:
    """Handles unknown commands by showing a fallback message."""
    # No validation here

    return f"{INVALID_COMMAND_MESSAGE}. {MSG_HELP_AWARE_TIP.capitalize()}."
