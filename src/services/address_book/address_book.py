"""
Module for managing an address book of contact records.

This module defines the AddressBook class, which serves as a container
and manager for multiple contact records. It supports adding, retrieving,
searching, and displaying records. Each record typically includes a name
and a list of associated phone numbers.
"""
from datetime import date, timedelta
from collections import UserDict

from services.address_book.record import Record

from utils.date_utils import is_leap_year, parse_date
from utils.text_utils import format_contacts_output
from validators.errors import ValidationError
from validators.args_validators import validate_argument_type
from validators.contact_validators import (
    ensure_contacts_storage_not_empty,
    ensure_contact_not_in_contacts_storage,
    ensure_contact_is_in_contacts_storage,
)


class AddressBook(UserDict):
    """
    A class for storing and managing contact records.

    Attributes:
        data (dict): A dictionary where keys are contact names and values are Record objects.

    Functionality:
        - Add new contacts
        - Find contacts by name or phone
        - Delete contacts
        - Display all records in aligned output
    """

    def __str__(self) -> str:
        """
        Returns a formatted string listing all contacts.

        Raises:
            ValidationError: If the address book is empty.
        """
        ensure_contacts_storage_not_empty(self.data)
        return format_contacts_output(self.to_dict())

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the entire address book.

        Each key is a contact name, and the value is a dictionary of contact details.

        Returns:
            dict: Dictionary of contacts with serialized record data.
        """
        return {key: record.to_dict() for key, record in self.data.items()}

    def add_record(self, contact: Record) -> None:
        """
        Adds a new contact record to the address book.

        Args:
            contact (Record): The contact to add.

        Raises:
            ValidationError: If the contact already exists.
            TypeError: If contact is of incorrect type

        Returns:
            str: A message confirming the addition.
        """
        validate_argument_type(contact, Record)

        # Prevent from overwriting existing entities
        ensure_contact_not_in_contacts_storage(contact.name.value, self.data)

        username = contact.name.value
        self.data[username] = contact

    def find(self, username: str) -> Record:
        """
        Finds a contact by name.

        Args:
            username (str): Partial or full name to search for (case-insensitive).

        Raises:
            ValidationError: If no contacts are found or the name is not found.

        Returns:
            Record: The matching contact.
        """
        ensure_contacts_storage_not_empty(self.data)
        contact = ensure_contact_is_in_contacts_storage(username, self.data)
        return contact

    def find_match(self, search_term: str = "") -> list[Record]:
        """
        Searches for contacts by name or phone number.

        Args:
            search_term (str): The term to search for (partial, case-insensitive match).

        Raises:
            ValidationError: If address book is empty.

        Returns:
            list[Record]: List of matched contacts.
        """
        ensure_contacts_storage_not_empty(self)

        matches = []

        if not search_term:
            matches = list(self.data.values())
        else:
            for record in self.data.values():
                if search_term.casefold() in record.name.value.casefold():
                    # Full match, case insensitive
                    matches.append(record)
                else:
                    # Partial match, case insensitive
                    if any(
                        search_term.casefold() in phone.value.casefold()
                        for phone in record.phones
                    ):
                        matches.append(record)

        if not matches:
            return []

        return matches

    def delete(self, username: str) -> None:
        """
        Deletes a contact from the address book.

        Args:
            username (str): Name of the contact to delete.

        Raises:
            ValidationError: If the contact does not exist.

        Returns:
            str: A message confirming deletion.
        """
        ensure_contact_is_in_contacts_storage(username, self.data)
        self.data.pop(username)

    def get_upcoming_birthdays(
        self, today: str = None, upcoming_period_days: int = 7
    ) -> list[dict[str, str | date]]:
        """
        Returns a list of users who have birthdays within the upcoming period from today.

        Each user is a dict with keys "name" and "birthday" in format "YYYY.MM.DD".
        The returned list contains dicts with "name" and the upcoming
        "congratulation_date" in string format (YYYY-MM-DD).

        :param today: The date to start checking from (default: current date).
        :param upcoming_period_days: Number of days ahead to check for birthdays (default: 7).
        :return: List of users with upcoming birthdays sorted by date.
        """
        # Assign today each time function is called, not once during function definition
        if today is None:
            today_obj = date.today()
        else:
            today_obj = parse_date(today)

        # Empty data guard
        if not self.data:
            return []

        user_congratulations = []

        for record in self.data.values():
            # Retrieve birthday object
            birthday = record.birthday

            # Guard records without assigned birthday
            if not birthday:
                continue

            # Handle the case if birthday is today or upcoming
            # Handle the case for February 29 birthday
            if birthday.value.month == 2 and birthday.value.day == 29:
                if is_leap_year(today_obj.year):
                    # For leap years, keep February 29
                    birthday_this_year = birthday.value.replace(year=today_obj.year)
                else:
                    # For non-leap years, set birthday to March 1
                    birthday_this_year = birthday.value.replace(
                        year=today_obj.year, month=3, day=1
                    )
            else:
                # For other birthdays, just replace the year
                birthday_this_year = birthday.value.replace(year=today_obj.year)

            # Handle the case if birthday has passed, adjust to next year
            if birthday_this_year < today_obj:
                # If it's a February 29 birthday in a non-leap year,
                # adjust it to March 1 of next year
                if birthday_this_year.month == 2 and birthday_this_year.day == 29:
                    if not is_leap_year(today_obj.year + 1):
                        birthday_this_year = birthday_this_year.replace(
                            year=today_obj.year + 1, month=3, day=1
                        )
                    else:
                        birthday_this_year = birthday_this_year.replace(
                            year=today_obj.year + 1
                        )
                else:
                    # Otherwise just move it to the next year
                    birthday_this_year = birthday_this_year.replace(
                        year=today_obj.year + 1
                    )

            # Filter dates in upcoming period range and add them to the congratulations list
            from_date = today_obj
            till_date = today_obj + timedelta(upcoming_period_days)
            is_in_upcoming_rage = from_date <= birthday_this_year <= till_date
            if is_in_upcoming_rage:
                congratulation_date = birthday_this_year
                # Move weekend congratulation to the following Monday
                if birthday_this_year.weekday() == 5:  # Saturday moved to Monday
                    congratulation_date += timedelta(days=2)
                elif birthday_this_year.weekday() == 6:  # Sunday moved to Monday
                    congratulation_date += timedelta(days=1)

                # Add congratulation date object to the list
                user_congratulations.append(
                    {
                        "name": record.name.value,
                        "congratulation": congratulation_date,
                        "congratulation_actual": birthday_this_year,
                    }
                )

        # Sort congratulations by date
        user_congratulations.sort(
            key=lambda user: (user["congratulation"], user["name"].casefold())
        )

        return user_congratulations


if __name__ == "__main__":
    # Basic tests to verify AddressBook logic

    # Setup

    test_book = AddressBook()
    assert len(test_book.data) == 0

    test_record_1 = Record("Alice")
    test_record_1.add_phone("1234567890")

    test_record_2 = Record("Bob")
    test_record_2.add_phone("9876543210")
    test_record_2.add_phone("7233232321")

    test_record_3 = Record("Alex")
    test_record_3.add_phone("9875554446")

    test_record_empty = Record("NoPhone")

    # Test __str__ with 0 records
    TEST_BOOK_STR_NO_CONTACTS = (
        "You don't have contacts yet, but you can add one anytime."
    )
    try:
        str(test_book)
    except ValidationError as exc:
        assert str(exc) == TEST_BOOK_STR_NO_CONTACTS
    else:
        assert False, "Should raise Validation error"

    # Test add contact - incorrect type
    try:
        test_book.add_record(object())
    except TypeError as exc:
        assert str(exc) == "Expected type 'Record', but received type 'object'."
    else:
        assert False, "Should raise TypeError error when incorrect type"
    assert len(test_book.data) == 0

    # Test add contact - first contact
    test_book.add_record(test_record_1)
    assert len(test_book.data) == 1

    # Test __str__ with 1 record
    TEST_MSG_BOOK_STR_1_CONTACT = "You have 1 contact:\n  Alice : phones 1234567890"
    assert str(test_book) == TEST_MSG_BOOK_STR_1_CONTACT

    # Test add contact - second contact
    test_book.add_record(test_record_2)
    assert len(test_book.data) == 2

    # Test __str__ with 2 records
    TEST_MSG_BOOK_STR_2_CONTACTS = (
        "You have 2 contacts:\n"
        "  Alice : phones 1234567890\n"
        "  Bob   : phones 9876543210, 7233232321"
    )
    assert str(test_book) == TEST_MSG_BOOK_STR_2_CONTACTS

    # Test add contact - record with empty phones as third contact
    test_book.add_record(test_record_empty)
    assert len(test_book.data) == 3

    # Test __str__ with 3 records
    TEST_MSG_BOOK_STR_3_CONTACTS = (
        "You have 3 contacts:\n"
        "  Alice   : 1234567890\n"
        "  Bob     : 9876543210; 7233232321\n"
        "  NoPhone : "
    )

    # Test add contact - add existing contact
    try:
        test_book.add_record(test_record_2)
    except ValidationError as exc:
        TEST_MSG_CONTACT_ALREADY_EXISTS = "Contact with username 'Bob' already exists."
        assert str(exc) == TEST_MSG_CONTACT_ALREADY_EXISTS
    else:
        assert False, "Should raise Validation error"
    assert len(test_book.data) == 3

    # Test find - found contact
    TEST_FIND_USERNAME = "Alice"
    TEST_USERNAME_PHONE = "1234567890"
    found_contact = test_book.find(TEST_FIND_USERNAME)
    assert found_contact
    assert found_contact.name.value == TEST_FIND_USERNAME
    assert len(found_contact.phones) == 1
    assert found_contact.phones[0].value == TEST_USERNAME_PHONE

    # Test find - contact not found
    try:
        test_book.find("Unknown_name")
    except ValidationError as exc:
        TEST_MSG_CONTACT_NOT_FOUND = "Contact 'Unknown_name' not found."
        assert str(exc) == TEST_MSG_CONTACT_NOT_FOUND
    else:
        assert False, "Should raise Validation error"

    # Test find match - search for username match
    # single result
    test_match_book_1 = AddressBook()

    TEST_MATCH_USERNAME_TERM = "aL"

    TEST_MATCH_USERNAME_1 = "Alex"
    TEST_MATCH_PHONE_NUMBER_1 = "9875554446"
    test_match_record_1 = Record(TEST_MATCH_USERNAME_1)
    test_match_record_1.add_phone(TEST_MATCH_PHONE_NUMBER_1)
    test_match_book_1.add_record(test_match_record_1)

    test_match_username_result = test_match_book_1.find_match(TEST_MATCH_USERNAME_TERM)
    assert len(test_match_username_result) == 1
    assert test_match_record_1 in test_match_username_result

    # multiple results
    test_match_book_2 = AddressBook()

    TEST_MATCH_USERNAME_2 = "Alice"
    TEST_MATCH_PHONE_NUMBER_2 = "1234567890"
    test_match_record_2 = Record(TEST_MATCH_USERNAME_2)
    test_match_record_2.add_phone(TEST_MATCH_PHONE_NUMBER_2)

    TEST_MATCH_USERNAME_3 = "Bob"
    TEST_MATCH_PHONE_NUMBER_3 = "7233232321"
    test_match_record_3 = Record(TEST_MATCH_USERNAME_3)
    test_match_record_3.add_phone(TEST_MATCH_PHONE_NUMBER_3)

    test_match_book_2.add_record(test_match_record_1)
    test_match_book_2.add_record(test_match_record_2)
    test_match_book_2.add_record(test_match_record_3)

    TEST_MATCH_OUTPUT_TEXT = (
        f"Found 2 matches for '{TEST_MATCH_USERNAME_TERM}':\n"
        "  Alex  : 9875554446\n"
        "  Alice : 1234567890"
    )
    test_match_username_result = test_match_book_2.find_match(TEST_MATCH_USERNAME_TERM)
    assert len(test_match_username_result) == 2
    assert test_match_record_1 in test_match_username_result
    assert test_match_record_2 in test_match_username_result
    assert test_match_record_3 not in test_match_username_result

    # Test find match - search for phone number match
    test_match_book = AddressBook()

    test_match_record_1 = Record("Alice")
    test_match_record_1.add_phone("1234567890")

    test_match_record_2 = Record("Bob")
    test_match_record_2.add_phone("9876543210")
    test_match_record_2.add_phone("7233232321")

    test_match_record_3 = Record("Alex")
    test_match_record_3.add_phone("9875554446")

    test_match_record_4 = Record("NoPhone")

    test_match_book.add_record(test_match_record_1)
    test_match_book.add_record(test_match_record_2)
    test_match_book.add_record(test_match_record_3)
    test_match_book.add_record(test_match_record_4)

    # single result
    TEST_MATCH_PHONE_SEARCH_TERM_1 = "876"
    test_match_phone_result_1 = test_match_book.find_match(
        TEST_MATCH_PHONE_SEARCH_TERM_1
    )
    assert len(test_match_phone_result_1) == 1
    assert any(
        [
            TEST_MATCH_PHONE_SEARCH_TERM_1 in phone.value
            for phone in test_match_phone_result_1[0].phones
        ]
    )
    # multiple results
    TEST_MATCH_PHONE_SEARCH_TERM_2 = "987"
    test_match_phone_result_2 = test_match_book.find_match(
        TEST_MATCH_PHONE_SEARCH_TERM_2
    )
    assert len(test_match_phone_result_2) == 2
    assert any(
        [
            TEST_MATCH_PHONE_SEARCH_TERM_1 in phone.value
            for phone in test_match_phone_result_2[0].phones
        ]
    )
    assert any(
        [
            TEST_MATCH_PHONE_SEARCH_TERM_2 in phone.value
            for phone in test_match_phone_result_2[1].phones
        ]
    )

    # Test find match - no matches
    TEST_MATCH_PHONE_SEARCH_TERM_UNKNOWN = "unknown"
    test_match_unknown_result = test_match_book.find_match(
        TEST_MATCH_PHONE_SEARCH_TERM_UNKNOWN
    )
    assert not test_match_unknown_result

    # Test find match - empty term
    TEST_MATCH_PHONE_SEARCH_TERM_EMPTY = ""
    test_match_empty_result = test_match_book.find_match(
        TEST_MATCH_PHONE_SEARCH_TERM_EMPTY
    )
    assert len(test_match_empty_result) == 4

    # Test delete contact
    test_delete_book = AddressBook()

    test_delete_record_1 = Record("Alice")
    test_delete_record_1.add_phone("1234567890")

    test_delete_record_2 = Record("Bob")
    test_delete_record_2.add_phone("9876543210")
    test_delete_record_2.add_phone("7233232321")

    test_delete_record_3 = Record("Alex")
    test_delete_record_3.add_phone("9875554446")

    test_delete_record_4 = Record("NoPhone")

    test_delete_book.add_record(test_match_record_1)
    test_delete_book.add_record(test_match_record_2)
    test_delete_book.add_record(test_match_record_3)
    test_delete_book.add_record(test_match_record_4)

    assert len(test_delete_book.data) == 4
    try:
        test_delete_book.delete("unknown_when_with_contacts")
    except ValidationError as exc:
        assert str(exc) == "Contact 'unknown_when_with_contacts' not found."
    else:
        assert False, "Should raise Validation error"
    assert len(test_delete_book.data) == 4

    try:
        test_delete_book.delete("alex")
    except ValidationError as exc:
        assert str(exc) == (
            "Contact 'alex' not found. However, a contact with a similar "
            "name exists as 'Alex'. Did you mean 'Alex'?"
        )
    else:
        assert False, "Should raise Validation error"
    assert len(test_delete_book.data) == 4

    try:
        test_delete_book.delete("     Alex   ")
    except ValidationError as exc:
        assert str(exc) == "Contact '     Alex   ' not found."
    else:
        assert False, "Should raise Validation error"
    assert len(test_delete_book.data) == 4

    test_delete_book.delete("Alex")
    assert "Alex" not in test_delete_book.data
    assert len(test_delete_book.data) == 3

    test_delete_book.delete("Alice")
    assert "Alice" not in test_delete_book.data
    assert len(test_delete_book.data) == 2

    test_delete_book.delete("Bob")
    assert "Bob" not in test_delete_book.data
    assert len(test_delete_book.data) == 1

    test_delete_book.delete("NoPhone")
    assert "NoPhone" not in test_delete_book.data
    assert len(test_delete_book.data) == 0

    try:
        test_delete_book.delete("unknown_when_no_contacts")
    except ValidationError as exc:
        assert str(exc) == "Contact 'unknown_when_no_contacts' not found."
    else:
        assert False, "Should raise Validation error"
    assert len(test_delete_book.data) == 0

    # Test __str__ with 0 records after all have been deleted
    TEST_MSG_BOOK_STR_NO_CONTACTS_AFTER_DELETION = (
        "You don't have contacts yet, but you can add one anytime."
    )
    try:
        str(test_delete_book)
    except ValidationError as exc:
        assert str(exc) == TEST_MSG_BOOK_STR_NO_CONTACTS_AFTER_DELETION
    else:
        assert False, "Should raise Validation error"

    # Test birthdays
    book_birthdays = AddressBook()

    birthday_record_no_birthday = Record("David")

    birthday_record_1 = Record("Alice")
    birthday_record_1.add_birthday("04.01.2001")

    birthday_record_2 = Record("Bob")
    birthday_record_2.add_birthday("01.01.2002")

    birthday_record_3 = Record("Charlie")
    birthday_record_3.add_birthday("31.12.2003")

    # birthdays - test no records ends up empty list
    birthdays_empty_expected = []
    birthdays_empty_result = book_birthdays.get_upcoming_birthdays()
    assert birthdays_empty_expected == birthdays_empty_result

    # birthdays - test record with no birthday are ignored
    book_birthdays.add_record(birthday_record_no_birthday)
    birthdays_no_birthday_expected = []
    birthdays_no_birthday_result = book_birthdays.get_upcoming_birthdays()
    assert birthdays_no_birthday_expected == birthdays_no_birthday_result

    # birthdays - test single record + move birthday from weekend to closest weekday
    book_birthdays.add_record(birthday_record_1)
    birthdays_one_expected = [
        {
            "name": "Alice",
            "congratulation": date(2025, 1, 6),
            "congratulation_actual": date(2025, 1, 4),
        }
    ]
    birthdays_one_result = book_birthdays.get_upcoming_birthdays(today="01.01.2025")
    assert birthdays_one_expected == birthdays_one_result

    # birthdays - test two records + sort elements by date
    book_birthdays.add_record(birthday_record_2)
    birthdays_two_expected = [
        {"name": "Bob", "congratulation_date": "01.01.2025"},
        {"name": "Alice", "congratulation_date": "06.01.2025"},
    ]
    birthdays_two_expected = [
        {
            "name": "Bob",
            "congratulation": date(2025, 1, 1),
            "congratulation_actual": date(2025, 1, 1),
        },
        {
            "name": "Alice",
            "congratulation": date(2025, 1, 6),
            "congratulation_actual": date(2025, 1, 4),
        },
    ]
    birthdays_two_result = book_birthdays.get_upcoming_birthdays(today="01.01.2025")
    assert birthdays_two_expected == birthdays_two_result

    # birthdays - test three records when birthdays out of upcoming period are ignored
    book_birthdays.add_record(birthday_record_3)
    birthdays_three_expected = [
        {
            "name": "Bob",
            "congratulation": date(2025, 1, 1),
            "congratulation_actual": date(2025, 1, 1),
        },
        {
            "name": "Alice",
            "congratulation": date(2025, 1, 6),
            "congratulation_actual": date(2025, 1, 4),
        },
    ]
    birthdays_three_result = book_birthdays.get_upcoming_birthdays(today="01.01.2025")
    assert birthdays_three_expected == birthdays_three_result

    # birthdays - test three records when upcoming passes new year + adding year to upcoming
    # Note: for "Alice" closest work day after weekend in 2026 is 05.01, not like in 2025 06.01
    birthdays_passing_new_year_expected = [
        {
            "name": "Charlie",
            "congratulation": date(2025, 12, 31),
            "congratulation_actual": date(2025, 12, 31),
        },
        {
            "name": "Bob",
            "congratulation": date(2026, 1, 1),
            "congratulation_actual": date(2026, 1, 1),
        },
        {
            "name": "Alice",
            "congratulation": date(2026, 1, 5),
            "congratulation_actual": date(2026, 1, 4),
        },
    ]
    birthdays_passing_new_year_result = book_birthdays.get_upcoming_birthdays(
        today="30.12.2025"
    )
    assert birthdays_passing_new_year_expected == birthdays_passing_new_year_result

    # birthdays - additional test of upcoming period of whole year
    birthdays_upcoming_period_1_expected = [
        {
            "name": "Bob",
            "congratulation": date(2025, 1, 1),
            "congratulation_actual": date(2025, 1, 1),
        },
        {
            "name": "Alice",
            "congratulation": date(2025, 1, 6),
            "congratulation_actual": date(2025, 1, 4),
        },
        {
            "name": "Charlie",
            "congratulation": date(2025, 12, 31),
            "congratulation_actual": date(2025, 12, 31),
        },
    ]
    birthdays_upcoming_period_1_result = book_birthdays.get_upcoming_birthdays(
        today="01.01.2025", upcoming_period_days=365
    )
    assert birthdays_upcoming_period_1_expected == birthdays_upcoming_period_1_result

    # birthdays - additional test of upcoming period of whole year with correct sorting
    birthdays_upcoming_period_2_expected = [
        {
            "name": "Alice",
            "congratulation": date(2025, 1, 6),
            "congratulation_actual": date(2025, 1, 4),
        },
        {
            "name": "Charlie",
            "congratulation": date(2025, 12, 31),
            "congratulation_actual": date(2025, 12, 31),
        },
        {
            "name": "Bob",
            "congratulation": date(2026, 1, 1),
            "congratulation_actual": date(2026, 1, 1),
        },
    ]
    birthdays_upcoming_period_2_result = book_birthdays.get_upcoming_birthdays(
        today="03.01.2025", upcoming_period_days=365
    )
    assert birthdays_upcoming_period_2_expected == birthdays_upcoming_period_2_result

    print("AddressBook tests passed.")
