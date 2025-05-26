"""
This module defines the Record class for managing a contact's name,
phone numbers, and birthday.
"""
from services.address_book.birthday import Birthday
from services.address_book.name import Name
from services.address_book.phone import Phone

from validators.errors import ValidationError
from validators.contact_validators import (
    ensure_phone_not_in_contact,
    ensure_phone_is_in_contact,
    ensure_birthday_in_contact_not_duplicate,
)
from validators.field_validators import (
    validate_date_format,
    validate_birthday_is_in_the_past,
)


class Record:
    """
    A class for storing contact information, including the contact's name,
    birthday, and phone numbers.

    Attributes:
        name (Name): The contact's name (required).
        phones (list[Phone]): A list of phones associated with the contact.
        birthday (Birthday | None): The contact's birthday if set.

    Methods:
        - add_phone(phone_number): Adds a new phone.
        - find_phone(phone_number): Finds and returns a phone.
        - edit_phone(old, new): Edits an existing phone.
        - remove_phone(phone_number): Removes a phone.
        - add_birthday(date): Adds or updates birthday.
        - to_dict(): Returns the record as a dictionary.
    """

    def __init__(self, username: str):
        self.name: Name = Name(username)
        self.birthday: Birthday | None = None
        self.phones: list[Phone] = []

    def __str__(self):
        name_info = f"{self.name}"
        birthday_optional_info = f"birthday: {self.birthday}, " if self.birthday else ""
        phones_info = (
            f"phones: {'; '.join(phone.value for phone in self.phones) or 'none'}"
        )
        return f"{name_info} : {birthday_optional_info}{phones_info}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(name={repr(self.name)}"
            f", birthday={repr(self.birthday)}"
            f", phones={repr(self.phones)})"
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.name == other.name
                and self.birthday == other.birthday
                and self.phones == other.phones
            )
        return NotImplemented

    def __contains__(self, item):
        if isinstance(item, Phone):
            return item in self.phones
        if isinstance(item, Birthday):
            return self.birthday == item
        return False

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the contact record.

        Returns:
            dict: A dictionary with name, list of phones, and optional birthday.
        """
        return {
            "name": self.name.to_dict(),
            "phones": [phone.to_dict() for phone in self.phones],
            "birthday": self.birthday.to_dict() if self.birthday else None,
        }

    def add_phone(self, phone_number: str) -> None:
        """
        Adds a phone number to the record.

        Raises:
            ValidationError: If the phone number already exists.
        """
        ensure_phone_not_in_contact(phone_number, self)
        new_phone = Phone(phone_number)
        self.phones.append(new_phone)

    def find_phone(self, phone_number: str) -> Phone:
        """
        Finds and returns a phone number object from the record.

        Returns:
            Phone: The phone object if found.

        Raises:
            ValidationError: If the phone is not found in the record.
        """
        _, phone = ensure_phone_is_in_contact(phone_number, self)
        return phone if phone else None

    def edit_phone(self, prev_phone_number: str, new_phone_number: str) -> None:
        """
        Updates an existing phone with a new phone number.

        Raises:
            ValidationError: If the new phone number already exists
            or if the old phone number is not found.
        """
        ensure_phone_not_in_contact(new_phone_number, self)
        _, phone = ensure_phone_is_in_contact(prev_phone_number, self)
        phone.update_phone(new_phone_number)

    def remove_phone(self, phone_number: str) -> None:
        """
        Removes a phone from the record.

        Raises:
            ValidationError: If the phone number does not exist.
        """
        idx, _ = ensure_phone_is_in_contact(phone_number, self)
        self.phones.pop(idx)

    def add_birthday(self, date: str) -> None:
        """
        Adds a birthday date to the record.

        If adding birthday is set with other value, updates it.

        Raises:
            ValidationError: If the new birthday date duplicates the existing one.
        """
        date_obj = validate_date_format(date)
        validate_birthday_is_in_the_past(date_obj)

        new_birthday = Birthday(date_obj)

        if not self.birthday:
            # Add birthday when record has no birthday
            self.birthday = new_birthday
            return

        ensure_birthday_in_contact_not_duplicate(new_birthday.value, self)

        # Update (replace) existing birthday
        self.birthday = new_birthday


if __name__ == "__main__":
    # TESTS

    # Test creation of a Record instance
    test_record_1 = Record("Alice")
    assert test_record_1.name.value == "Alice"
    assert len(test_record_1.phones) == 0
    assert str(test_record_1) == "Alice : phones: none"
    assert (
        repr(test_record_1)
        == "Record(name=Name(value='Alice'), birthday=None, phones=[])"
    )

    # Test try creation of a Record instance with empty name
    try:
        test_record_1 = Record("")
    except ValidationError as exc:
        assert str(exc) == "Username cannot be empty or just whitespace."
    else:
        assert (
            False
        ), "Should raise Validation error when creating record with empty name"

    # Test add a phone number
    test_record_1.add_phone("1234567890")
    assert len(test_record_1.phones) == 1
    assert Phone("1234567890") in test_record_1
    assert str(test_record_1) == "Alice : phones: 1234567890"
    assert repr(test_record_1) == (
        "Record(name=Name(value='Alice'), "
        "birthday=None, "
        "phones=[Phone(value='1234567890')])"
    )

    test_record_1.add_phone("0987654321")
    assert len(test_record_1.phones) == 2
    assert Phone("1234567890") in test_record_1
    assert Phone("0987654321") in test_record_1
    assert str(test_record_1) == "Alice : phones: 1234567890; 0987654321"
    assert repr(test_record_1) == (
        "Record(name=Name(value='Alice'), "
        "birthday=None, "
        "phones=[Phone(value='1234567890'), Phone(value='0987654321')])"
    )

    # Test find phone
    TEST_FIND_USERNAME = "Bob"
    TEST_FIND_PHONE_NUMBER_1 = "1234567890"
    TEST_FIND_PHONE_NUMBER_2 = "0987654321"
    TEST_FIND_PHONE_NUMBER_UNKNOWN = "9999999999"

    test_record_find_phone = Record(TEST_FIND_USERNAME)
    test_record_find_phone.add_phone(TEST_FIND_PHONE_NUMBER_1)
    test_record_find_phone.add_phone(TEST_FIND_PHONE_NUMBER_2)

    test_found_phone_number_1 = test_record_find_phone.find_phone(
        TEST_FIND_PHONE_NUMBER_1
    )
    assert test_found_phone_number_1 is not None
    assert test_found_phone_number_1.value == TEST_FIND_PHONE_NUMBER_1

    test_found_phone_number_2 = test_record_find_phone.find_phone(
        TEST_FIND_PHONE_NUMBER_2
    )
    assert test_found_phone_number_2 is not None
    assert test_found_phone_number_2.value == TEST_FIND_PHONE_NUMBER_2

    try:
        test_record_find_phone.find_phone(TEST_FIND_PHONE_NUMBER_UNKNOWN)
    except ValidationError as exc:
        assert str(exc) == (
            f"Phone number '{TEST_FIND_PHONE_NUMBER_UNKNOWN}' "
            f"for contact '{TEST_FIND_USERNAME}' not found."
        )
    else:
        assert False, "Should raise Validation error when phone number not found"

    # Test edit a phone
    TEST_EDIT_USERNAME = "Charlie"
    TEST_EDIT_PHONE_NUMBER_1 = "1111111111"
    TEST_EDIT_PHONE_NUMBER_2 = "2222222222"
    TEST_EDIT_PHONE_NUMBER_3 = "3333333333"
    TEST_EDIT_PHONE_NUMBER_4 = "4444444444"
    TEST_EDIT_PHONE_NUMBER_UNKNOWN = "9999999999"

    test_record_edit = Record(TEST_EDIT_USERNAME)
    test_record_edit.add_phone(TEST_EDIT_PHONE_NUMBER_1)
    test_record_edit.add_phone(TEST_EDIT_PHONE_NUMBER_2)

    test_record_edit.edit_phone(TEST_EDIT_PHONE_NUMBER_1, TEST_EDIT_PHONE_NUMBER_3)
    assert Phone(TEST_EDIT_PHONE_NUMBER_3) in test_record_edit

    try:
        test_record_edit.edit_phone(
            TEST_EDIT_PHONE_NUMBER_UNKNOWN, TEST_EDIT_PHONE_NUMBER_4
        )
    except ValidationError as exc:
        assert str(exc) == (
            f"Phone number '{TEST_EDIT_PHONE_NUMBER_UNKNOWN}' "
            f"for contact '{TEST_EDIT_USERNAME}' not found."
        )
    else:
        assert False, "Should raise Validation error when old phone number not found"

    try:
        test_record_edit.edit_phone(TEST_EDIT_PHONE_NUMBER_2, TEST_EDIT_PHONE_NUMBER_3)
    except ValidationError as exc:
        assert str(exc) == (
            f"Contact '{TEST_EDIT_USERNAME}' "
            f"has '{TEST_EDIT_PHONE_NUMBER_3}' phone number already."
        )
    else:
        assert False, "Should raise Validation error when new phone already exists"

    # Test remove a phone
    TEST_REMOVE_USERNAME = "Denis"
    TEST_REMOVE_PHONE_NUMBER_1 = "1111111111"
    TEST_REMOVE_PHONE_NUMBER_2 = "2222222222"
    TEST_REMOVE_PHONE_NUMBER_UNKNOWN = "9999999999"

    test_record_remove = Record(TEST_REMOVE_USERNAME)
    test_record_remove.add_phone(TEST_REMOVE_PHONE_NUMBER_1)
    test_record_remove.add_phone(TEST_REMOVE_PHONE_NUMBER_2)

    assert len(test_record_remove.phones) == 2
    test_record_remove.remove_phone(TEST_REMOVE_PHONE_NUMBER_1)
    assert len(test_record_remove.phones) == 1
    assert test_record_remove.phones[0].value == TEST_REMOVE_PHONE_NUMBER_2

    try:
        test_record_remove.remove_phone(TEST_REMOVE_PHONE_NUMBER_UNKNOWN)
    except ValidationError as exc:
        assert str(exc) == (
            f"Phone number '{TEST_REMOVE_PHONE_NUMBER_UNKNOWN}' "
            f"for contact '{TEST_REMOVE_USERNAME}' not found."
        )
    else:
        assert (
            False
        ), "Should raise Validation error when try to delete non existing phone number"

    # Test add birthday
    TEST_BIRTHDAY_USERNAME = "Mike"
    TEST_BIRTHDAY_DATE_STR = "05.05.2005"
    TEST_BIRTHDAY_DATE_STR_UPDATE = "06.06.2006"

    test_birthday = Birthday(TEST_BIRTHDAY_DATE_STR)
    test_birthday_updated = Birthday(TEST_BIRTHDAY_DATE_STR_UPDATE)

    test_record_birthday = Record(TEST_BIRTHDAY_USERNAME)
    assert test_record_birthday.birthday is None
    assert str(test_record_birthday) == f"{TEST_BIRTHDAY_USERNAME} : phones: none"

    test_record_birthday.add_birthday(TEST_BIRTHDAY_DATE_STR)
    assert test_birthday in test_record_birthday

    try:
        test_record_birthday.add_birthday(TEST_BIRTHDAY_DATE_STR)
    except ValidationError as exc:
        TEST_ERR_MSG_BIRTHDAY_DUPLICATE = (
            f"Birthday for '{TEST_BIRTHDAY_USERNAME}' "
            f"is already set to '{TEST_BIRTHDAY_DATE_STR}'."
        )
        assert str(exc) == TEST_ERR_MSG_BIRTHDAY_DUPLICATE
    else:
        assert (
            False
        ), "Should raise Validation error when the same birthday date is set already."
    assert test_birthday in test_record_birthday

    test_record_birthday.add_birthday(TEST_BIRTHDAY_DATE_STR_UPDATE)
    assert test_birthday_updated in test_record_birthday

    print("Record tests passed.")
