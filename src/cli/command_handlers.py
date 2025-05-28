"""
Command handlers for CLI application.

Each handler corresponds to a specific user command and includes input validation,
invokes business logic, and generates an appropriate response.
"""

import sys

from decorators.input_error import input_error
from persistence.persistence_error import PersistenceError
from services.contacts_manager import (
    load_contacts,
    save_contacts,
    show_all,
    add_contact,
    change_contact,
    remove_contact,
    show_phone,
    remove_phone,
    remove_birthday,
    add_birthday,
    show_birthday,
    show_upcoming_birthdays,
)
from utils.constants import (
    MSG_HELLO_MESSAGE,
    MSG_APP_PURPOSE_MESSAGE,
    MSG_EXIT_MESSAGE,
    MENU_HELP_STR,
    MSG_INVALID_EMPTY_COMMAND,
    INVALID_COMMAND_MESSAGE,
    MSG_HELP_AWARE_TIP,
    MSG_SAVE_SUCCESS,
)
from utils.text_utils import format_contacts_output, format_text_output
from validators.args_validators import ensure_args_have_n_arguments


def handle_load_app_data():
    """
    Load application data (e.g., contacts) from persistent storage.

    If loading fails, the function gracefully exits the application.
    Should be called at the start of the application to initialize state.

    Raises:
        None. Exits the application on failure.
    """
    try:
        load_contacts()
    except PersistenceError as exc:
        err_message = f"\n{exc}" if exc else ""
        handle_exit(
            prefix="\n",
            message=f"Failed to load application data.{err_message} Exiting.",
            suffix="can't start the application",
            save_state_on_exit=False,
        )


def handle_hello() -> str:
    """Returns a greeting message to the user."""
    # No validation checks here
    return f"{MSG_HELLO_MESSAGE}\n{MSG_APP_PURPOSE_MESSAGE}."


@input_error
def handle_all() -> str:
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

    result = show_all()

    if result.get("message"):
        return format_text_output(result)

    return format_contacts_output(result)


@input_error
def handle_add(args: list[str]) -> str:
    """
    Add a new contact.

    Expected arguments in 'args': [username, phone_number]
    """
    ensure_args_have_n_arguments(args, 2, "username and a phone number")
    username, phone_number = args
    result = add_contact(username, phone_number)
    return format_text_output(result)


@input_error
def handle_change(args: list[str]) -> str:
    """
    Change an existing contact's phone number.

    Expected arguments in 'args': [username, old_phone_number, new_phone_number]
    """
    ensure_args_have_n_arguments(
        args, 3, "username, old phone number and new phone number"
    )
    username, prev_phone_number, new_phone_number = args
    result = change_contact(username, prev_phone_number, new_phone_number)
    return format_text_output(result)


@input_error
def handle_delete(args: list[str]) -> str:
    """
    Delete an existing contact.

    Expected arguments in 'args': [username]

    Args:
        args (list[str]): List containing the username of the contact to delete.

    Returns:
        str: Formatted text output indicating the result of the delete operation.
    """
    ensure_args_have_n_arguments(args, 1, "username")
    username = args[0]
    result = remove_contact(username)
    return format_text_output(result)


@input_error
def handle_phone(args: list[str]) -> str:
    """
    Return phone numbers for contacts matching the search term (partial match supported).

    Expected arguments in 'args': [search_term]
    """
    ensure_args_have_n_arguments(args, 1, "username")
    # Partial match is supported - the check if username is in the
    # contacts list (with partial match) is not checked by validator and
    # postponed further to the handler
    search_term = args[0]

    result = show_phone(search_term)
    return format_text_output(result)


@input_error
def handle_delete_phone(args: list[str]) -> str:
    """
    Delete an existing contact's phone number.

    Expected arguments in 'args': [username] [phone_number]

    Args:
        args (list[str]): List containing the username and phone number of the contact to delete.

    Returns:
        str: Formatted text output indicating the result of the delete operation.
    """
    ensure_args_have_n_arguments(args, 2, "username and a phone number")
    username, phone_number = args
    result = remove_phone(username, phone_number)
    return format_text_output(result)


@input_error
def handle_add_birthday(args: list[str]) -> str:
    """
    Adds a birthday to the specified contact.

    Expected arguments in 'args': [username, date]
    """
    ensure_args_have_n_arguments(args, 2, "username and a birthday")
    username, date = args
    result = add_birthday(username, date)
    return format_text_output(result)


@input_error
def handle_show_birthday(args: list[str]) -> str:
    """
    Displays the birthday of the specified contact.

    Expected arguments in 'args': [username]
    """
    ensure_args_have_n_arguments(args, 1, "username")
    username = args[0]
    result = show_birthday(username)
    return format_text_output(result, lines_offset="")


@input_error
def handle_delete_birthday(args: list[str]) -> str:
    """
    Delete an existing contact's birthday.

    Expected arguments in 'args': [username]

    Args:
        args (list[str]): List containing the username of the contact birthday to delete from.

    Returns:
        str: Formatted text output indicating the result of the delete operation.
    """
    ensure_args_have_n_arguments(args, 1, "username")
    username = args[0]
    result = remove_birthday(username)
    return format_text_output(result)


@input_error
def handle_birthdays() -> str:
    """Displays all birthdays occurring in the upcoming week."""
    # No validation checks here
    result = show_upcoming_birthdays()
    return format_text_output(result)


def handle_help(help_text: str = MENU_HELP_STR) -> str:
    """Returns formatted help menu."""
    # No validation here
    return help_text


def handle_exit(prefix="", message="", suffix="", save_state_on_exit=True):
    """Print a farewell message and terminate the program."""
    # No validation here

    if save_state_on_exit:
        try:
            save_contacts()
            message = MSG_SAVE_SUCCESS
        except PersistenceError as exc:
            message = f"ERROR: Could not save contacts. {exc}"
            if suffix:
                suffix = ", " + suffix
            suffix = "quitting without saving changes" + suffix

    print(
        f"{prefix}"
        f"{f'{message}\n' if message else ''}"
        f"{MSG_EXIT_MESSAGE}"
        f"{f' ({suffix})' if suffix else ''}"
    )
    sys.exit(0)


def handle_empty() -> str:
    """Handles empty command from user by showing a fallback message."""
    # No validation here

    return f"{MSG_INVALID_EMPTY_COMMAND}."


def handle_unknown() -> str:
    """Handles unknown commands by showing a fallback message."""
    # No validation here

    return f"{INVALID_COMMAND_MESSAGE}. {MSG_HELP_AWARE_TIP.capitalize()}."
