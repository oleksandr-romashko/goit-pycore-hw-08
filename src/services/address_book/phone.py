"""
Phone field for storing and validating phone numbers.

This module defines the `Phone` class which extends `Field` and ensures
the phone number is valid on assignment or update.
"""

from services.address_book.field import Field

from validators.errors import ValidationError
from validators.field_validators import validate_phone_number


class Phone(Field):
    """
    Class for storing and validating phone numbers.

    Ensures the phone number matches expected format during initialization and
    value changes.
    """

    def __init__(self, phone_number: str):
        phone_number = phone_number.strip()
        validate_phone_number(phone_number)
        super().__init__(phone_number)

    @Field.value.setter
    def value(self, phone_number: str):
        """
        Sets a new validated phone number value.

        Overrides setter from parent adding validation.
        """
        phone_number = phone_number.strip()
        validate_phone_number(phone_number)
        self._value = phone_number

    def update_phone(self, phone_number: str):
        """Updated phone number with a new one."""
        self.value = phone_number


if __name__ == "__main__":
    # TESTS

    # Test data
    TEST_VALID_PHONE_NUMBER_1 = "1234567890"
    TEST_VALID_PHONE_NUMBER_2 = "0987654321"
    TEST_INVALID_PHONE_NUMBER = "123"

    # Test creation of instance with valid phone number
    test_phone_1 = Phone(TEST_VALID_PHONE_NUMBER_1)
    assert test_phone_1.value == TEST_VALID_PHONE_NUMBER_1

    # Test creation of instance with invalid phone number
    try:
        Phone(TEST_INVALID_PHONE_NUMBER)
    except ValidationError as exc:
        TEST_ERR_MSG_INVALID_PHONE_NUMBER = (
            f"Invalid phone number '{TEST_INVALID_PHONE_NUMBER}'. "
            "Expected 10 digits, optionally starting with '+'."
        )
        assert str(exc) == TEST_ERR_MSG_INVALID_PHONE_NUMBER
    else:
        assert False, (
            "Should raise Validation error "
            "when creating Phone instance with invalid phone number value"
        )

    # Test direct assignment to Phone instance value a valid phone number
    test_phone_2 = Phone(TEST_VALID_PHONE_NUMBER_1)
    test_phone_2.value = TEST_VALID_PHONE_NUMBER_2
    assert test_phone_2.value == TEST_VALID_PHONE_NUMBER_2

    # Test direct assignment to Phone instance value an invalid phone number
    test_phone_3 = Phone(TEST_VALID_PHONE_NUMBER_1)
    try:
        test_phone_3.value = TEST_INVALID_PHONE_NUMBER
    except ValidationError as exc:
        TEST_ERR_MSG_INVALID_PHONE_NUMBER = (
            f"Invalid phone number '{TEST_INVALID_PHONE_NUMBER}'. "
            "Expected 10 digits, optionally starting with '+'."
        )
        assert str(exc) == TEST_ERR_MSG_INVALID_PHONE_NUMBER
    else:
        assert False, (
            "Should raise Validation error "
            "when updating Phone instance value directly "
            "with invalid phone number value"
        )
    assert test_phone_3.value == TEST_VALID_PHONE_NUMBER_1

    # Test update instance with valid phone number
    test_phone_4 = Phone(TEST_VALID_PHONE_NUMBER_1)
    test_phone_4.update_phone(TEST_VALID_PHONE_NUMBER_2)
    assert test_phone_4.value == TEST_VALID_PHONE_NUMBER_2

    # Test update instance with invalid phone number
    test_phone_5 = Phone(TEST_VALID_PHONE_NUMBER_1)
    try:
        test_phone_5.update_phone(TEST_INVALID_PHONE_NUMBER)
    except ValidationError as exc:
        TEST_ERR_MSG_INVALID_PHONE_NUMBER = (
            f"Invalid phone number '{TEST_INVALID_PHONE_NUMBER}'. "
            "Expected 10 digits, optionally starting with '+'."
        )
        assert str(exc) == TEST_ERR_MSG_INVALID_PHONE_NUMBER
    else:
        assert False, (
            "Should raise Validation error "
            "when updating Phone instance with invalid phone number value"
        )

    print("Phone tests passed.")
