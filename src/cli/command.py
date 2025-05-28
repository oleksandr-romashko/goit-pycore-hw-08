"""
This module defines the Command enumeration used to represent the set of available
user commands in the application. Commands are defined as string values using the StrEnum
base class to ensure both enum capabilities and string compatibility.

Typical usage includes parsing user input and mapping it to specific command logic,
such as adding a contact, displaying all entries, or exiting the application.
"""

from enum import StrEnum


class Command(StrEnum):
    """
    Enumeration of supported CLI commands.

    Each command corresponds to a user action within the application.

    The use of StrEnum allows commands to be compared directly to string inputs.
    """

    HELLO = "hello"
    ALL = "all"
    ADD = "add"
    CHANGE = "change"
    DELETE = "delete"
    PHONE = "phone"
    DELETE_PHONE = "delete-phone"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    DELETE_BIRTHDAY = "delete-birthday"
    BIRTHDAYS = "birthdays"
    HELP = "help"
    EXIT = "exit"
    CLOSE = "close"
