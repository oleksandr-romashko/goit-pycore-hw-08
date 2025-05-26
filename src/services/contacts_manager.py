"""
Simple contact management module.

This module provides functions to manage a contact list using an AddressBook
instance.
It includes functionality to add new contacts, update phone numbers, and
retrieve contact details.

Functions:
- add_contact(username, phone_number, book): Adds a new contact or appends phone
  if contact exists.
- change_contact(username, prev_phone_number, new_phone_number, book): Changes
  an existing contact's phone number.
- show_phone(search_term, book): Shows the phone number(s) of a matching contact.
- show_all(book): Shows all saved contacts.
"""
from datetime import date as datetime_date

from decorators.service_error import service_error
from services.address_book.address_book import AddressBook
from services.address_book.record import Record
from utils.constants import (
    MSG_CONTACT_ADDED,
    MSG_CONTACT_UPDATED,
    MSG_CONTACT_DELETED,
    MSG_PHONE_ADDED,
    MSG_PHONE_UPDATED,
    MSG_PHONE_DELETED,
    MSG_SHOW_NO_MATCHES,
    MSG_SHOW_FOUND_MATCHES,
    MSG_BIRTHDAY_ADDED,
    MSG_BIRTHDAY_UPDATED,
    MSG_BIRTHDAY_NO_BIRTHDAY,
    MSG_BIRTHDAY_UPCOMING_PERIOD_STR,
    MSG_BIRTHDAYS_NO_UPCOMING,
    MSG_BIRTHDAYS_FOUND_MATCHES,
)
from validators.contact_validators import ensure_contacts_storage_not_empty


@service_error
def show_all(book: AddressBook) -> dict[str, str | list[dict[str, str]]]:
    """
    Return all contacts in the address book with their phone numbers.

    Args:
        book (AddressBook): The address book instance.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict[str, str | list[dict[str, str]]]: All contacts as structured data.
    """
    ensure_contacts_storage_not_empty(book)
    return book.to_dict()


@service_error
def add_contact(username: str, phone_number: str, book: AddressBook) -> dict[str, str]:
    """
    Add a new contact with a phone number, or append the phone if the contact already exists.

    Args:
        username (str): Name of the contact.
        phone_number (str): Phone number to add.
        book (AddressBook): The address book instance to update.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict[str, str]: Message indicating result.
    """
    contact = book.get(username)

    if contact:
        contact.add_phone(phone_number)
        return {
            "message": f"{MSG_CONTACT_UPDATED} {MSG_PHONE_ADDED}",
        }

    contact = Record(username)
    contact.add_phone(phone_number)
    book.add_record(contact)

    return {
        "message": MSG_CONTACT_ADDED,
    }


@service_error
def change_contact(
    username: str, prev_phone_number: str, new_phone_number: str, book: AddressBook
) -> dict[str, str]:
    """
    Update an existing contact's phone number.

    Args:
        username (str): Contact's name.
        prev_phone_number (str): Old phone number to replace.
        new_phone_number (str): New phone number to set.
        book (AddressBook): The address book instance containing the contact.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict[str, str]: Message indicating result.
    """
    contact = book.find(username)
    contact.edit_phone(prev_phone_number, new_phone_number)

    return {
        "message": MSG_PHONE_UPDATED,
    }


@service_error
def delete_contact(username: str, book: AddressBook) -> dict[str, str]:
    """
    Deletes a contact by name from the address book.

    Args:
        username (str): The name of the contact to delete.
        book (AddressBook): The address book instance.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict[str, str]: Message indicating result.
    """
    book.delete(username)

    return {
        "message": MSG_CONTACT_DELETED,
    }


@service_error
def show_phone(search_term: str, book: AddressBook) -> dict[str, str | list[dict]]:
    """
    Retrieve the phone number(s) for a contact matching the search term.

    Partial and case-insensitive matching is supported.

    Args:
        search_term (str): Search keyword (full or partial contact name).
        book (AddressBook): The address book instance to search.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict: Matching contact(s) and phone number(s) as structured data.
    """
    matches = book.find_match(search_term)

    if not matches:
        return {
            "message": MSG_SHOW_NO_MATCHES,
        }

    # Sort found matches alphabetically by name
    matches.sort(key=lambda record: record.name.value.casefold())

    # Form return dictionary object
    count = len(matches)
    suffix = "" if count == 1 else "es"
    search_prompt = f"{search_term}" if search_term else "empty search"
    message = f"{MSG_SHOW_FOUND_MATCHES.format(count, suffix)} for '{search_prompt}'"
    items = [
        {"name": record.name.value, "phones": [phone.value for phone in record.phones]}
        for record in matches
    ]

    return {
        "message": message,
        "items": items,
    }


@service_error
def remove_phone(username: str, phone_number: str, book: AddressBook) -> dict[str, str]:
    """
    Remove a phone number from a contact in the address book.

    Args:
        username (str): The name of the contact whose phone number is to be removed.
        phone_number (str): The phone number to remove from the contact.
        book (AddressBook): The address book containing the contact.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict[str, str]: Message indicating result.
    """
    contact = book.find(username)
    contact.remove_phone(phone_number)

    return {
        "message": f"{MSG_CONTACT_UPDATED} {MSG_PHONE_DELETED}",
    }


@service_error
def add_birthday(username: str, date: str, book: AddressBook) -> dict[str, str]:
    """
    Add a birthday to the specified contact.

    Args:
        username (str): Contact's name.
        date (str): Birthday in string format.
        book (AddressBook): Address book instance.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict[str, str]: Message indicating result.
    """
    contact = book.find(username)
    was_empty = contact.birthday is None

    contact.add_birthday(date)

    if was_empty:
        return {
            "message": MSG_BIRTHDAY_ADDED,
        }

    return {
        "message": MSG_BIRTHDAY_UPDATED,
    }


@service_error
def show_birthday(
    username: str, book: AddressBook
) -> dict[str, str | list[dict[str, str]]]:
    """
    Retrieve the birthday of the specified contact.

    Args:
        username (str): Contact's name.
        book (AddressBook): Address book instance.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict: Standardized output containing header and optional items.
    """
    contact = book.find(username)

    if not contact.birthday:
        return {
            "message": MSG_BIRTHDAY_NO_BIRTHDAY.format(username),
        }

    items = [
        {
            "name": username,
            "birthday": contact.birthday.value.isoformat(),
        }
    ]

    return {
        "items": items,
    }


@service_error
def show_upcoming_birthdays(book: AddressBook) -> dict[str, str | datetime_date]:
    """
    Retrieve birthdays occurring in the upcoming week.

    Args:
        book (AddressBook): Address book instance.

    Handles errors specified in service_error with appropriate user-friendly error message.

    Returns:
        dict[str, str]: Message indicating upcoming birthday result.
    """
    matches = book.get_upcoming_birthdays()

    if not matches:
        return {
            "message": MSG_BIRTHDAYS_NO_UPCOMING.format(
                MSG_BIRTHDAY_UPCOMING_PERIOD_STR
            ),
        }

    # Form return dictionary object
    count = len(matches)
    suffix = "" if count == 1 else "s"
    message = MSG_BIRTHDAYS_FOUND_MATCHES.format(
        count, suffix, MSG_BIRTHDAY_UPCOMING_PERIOD_STR
    )
    items = [
        {
            "name": match.get("name"),
            "congratulation": (
                match.get("congratulation").isoformat()
                if match.get("congratulation")
                else ""
            ),
            "congratulation_actual": (
                match.get("congratulation_actual").isoformat()
                if match.get("congratulation_actual")
                else ""
            ),
        }
        for match in matches
    ]

    return {
        "message": message,
        "items": items,
    }
