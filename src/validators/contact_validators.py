"""
Validators for contact management commands.

Each function validates input arguments or contact data before executing a command
by calling appropriate validation function.

Called validators may raise ValidationError with descriptive messages if
validation fails.
"""

from datetime import date

from services.address_book.phone import Phone
from utils.constants import (
    MSG_CONTACT_EXISTS,
    MSG_NO_CONTACTS,
    MSG_CONTACT_NOT_FOUND,
    MSG_PHONE_NUMBER_EXISTS,
    MSG_PHONE_NUMBER_NOT_FOUND,
    MSG_BIRTHDAY_DUPLICATE,
)
from utils.date_utils import format_date_str
from validators.errors import ValidationError


def ensure_contacts_storage_not_empty(contacts: dict) -> None:
    """
    Ensures that the contacts dictionary is not empty.

    Args:
        contacts (dict): Dictionary of contacts.

    Raises:
        ValidationError: If no contacts exist.
    """
    if not contacts:
        raise ValidationError(MSG_NO_CONTACTS)


def ensure_contact_not_in_contacts_storage(username: str, contacts: dict) -> None:
    """
    Ensures the contact with the given username does not already exist (case-insensitive).

    Args:
        username (str): username key to be checked.
        contacts (dict): Existing contacts dictionary.

    Raises:
        ValidationError: If contact already exists or is in a different case.
    """
    for contact in contacts.values():
        contact_name = contact.name.value
        # Check for exact match
        if contact_name == username:
            raise ValidationError(f"{MSG_CONTACT_EXISTS.format(username)}.")

        # Check for case-insensitive match
        if contact_name.casefold() == username.casefold():
            raise ValidationError(
                f"{MSG_CONTACT_EXISTS.format(username)}, "
                f"but under a different name: '{contact_name}'."
            )


def ensure_contact_is_in_contacts_storage(
    username: str, contacts: dict[str, any]
) -> any:
    """
    Ensures a contact with the provided username exists, case-insensitively.

    Args:
        username (str): username to check.
        contacts (dict): Dictionary of contacts.

    Raises:
        ValidationError: If contact doesn't exist or name differs by case.
    """
    match = next((c for c in contacts if c.casefold() == username.casefold()), None)

    if not match:
        raise ValidationError(f"{MSG_CONTACT_NOT_FOUND.format(username)}.")

    # If there's a match with a different case, let the user know
    if match != username:
        raise ValidationError(
            f"{MSG_CONTACT_NOT_FOUND.format(username)}. "
            f"However, a contact with a similar name exists as '{match}'. "
            f"Did you mean '{match}'?"
        )

    return contacts[match]


def ensure_phone_not_in_contact(phone_number: str, record) -> None:
    """
    Ensures the specified phone number is not already present in the contact's phone list.

    Checks for the exact match.

    Args:
        phone_number (str): Phone number to check.
        record: Contact record containing a list of phone objects.

    Raises:
        ValidationError: If the phone number already exists in the contact.
    """
    for phone_obj in record.phones:
        if phone_obj.value == phone_number:
            raise ValidationError(
                MSG_PHONE_NUMBER_EXISTS.format(record.name, phone_number)
            )


def ensure_phone_is_in_contact(phone_number: str, record) -> tuple[int, Phone]:
    """
    Validates that a given phone number exists in the contact and returns its position.

    Args:
        phone_number (str): Phone number to find.
        record: Contact record containing a list of phone objects.

    Returns:
        tuple[int, Phone]: Index and phone object if found.

    Raises:
        ValidationError: If the phone number is not found.
    """
    if not record.phones:
        raise ValidationError(
            MSG_PHONE_NUMBER_NOT_FOUND.format(phone_number, record.name)
        )

    for idx, phone in enumerate(record.phones):
        if phone.value == phone_number:
            return idx, phone

    raise ValidationError(MSG_PHONE_NUMBER_NOT_FOUND.format(phone_number, record.name))


def ensure_birthday_in_contact_not_duplicate(birthday: date, record):
    """
    Checks if the provided birthday is already assigned to the contact.

    Args:
        birthday (date): Birthday to validate.
        record: Contact record with an existing birthday.

    Raises:
        ValidationError: If the birthday is the same as the one already set.
    """
    if birthday == record.birthday.value:
        username = record.name
        date_str = format_date_str(record.birthday.value)
        raise ValidationError(MSG_BIRTHDAY_DUPLICATE.format(username, date_str))
