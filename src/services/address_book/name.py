"""
Name field for storing and validating contact names.

This module defines the `Name` class which extends `Field` and ensures
the contact name is valid on assignment.
"""

from services.address_book.field import Field

from validators.errors import ValidationError
from validators.field_validators import validate_username_length


class Name(Field):
    """
    Class for storing and validating contact names.

    Ensures the name is validated on initialization and value changes.
    """

    def __init__(self, username: str):
        username = username.strip()
        validate_username_length(username)
        super().__init__(username)

    @Field.value.setter
    def value(self, username: str):
        """
        Sets a new validated name value.

        Overrides setter from parent adding validation.
        """
        username = username.strip()
        validate_username_length(username)
        self._value = username


if __name__ == "__main__":
    # TESTS

    TEST_USERNAME_VALID = "Alice"
    TEST_USERNAME_VALID_SHORTEST = "Bc"
    TEST_USERNAME_VALID_LONGEST = "D" * 50
    TEST_USERNAME_INVALID_TOO_SHORT = "E"
    TEST_USERNAME_INVALID_TOO_LONG = "F" * 51

    # Test happy path
    Name(TEST_USERNAME_VALID)

    # Test shortest possible username
    Name(TEST_USERNAME_VALID_SHORTEST)

    # Test longest possible username
    Name(TEST_USERNAME_VALID_LONGEST)

    # Test too short username validation
    try:
        Name(TEST_USERNAME_INVALID_TOO_SHORT)
    except ValidationError as exc:
        TEST_ERR_MSG_TOO_SHORT = (
            f"Username '{TEST_USERNAME_INVALID_TOO_SHORT}' is too short "
            "and should have at least 2 symbols."
        )
        assert str(exc) == TEST_ERR_MSG_TOO_SHORT
    else:
        assert False, "Should raise Validation error when name is too short"

    # Test too long username validation
    try:
        Name(TEST_USERNAME_INVALID_TOO_LONG)
    except ValidationError as exc:
        TEST_ERR_MSG_TOO_LONG = (
            "Username 'FFFFFFFFFFFF...' is too long "
            "and should have not more than 50 symbols."
        )
        assert str(exc) == TEST_ERR_MSG_TOO_LONG
    else:
        assert False, "Should raise Validation error when name is too long"

    # Test direct name value assignment username validation
    test_name = Name(TEST_USERNAME_VALID)
    try:
        test_name.value = TEST_USERNAME_INVALID_TOO_SHORT
    except ValidationError as exc:
        TEST_ERR_MSG_TOO_SHORT_DIRECT_ASSIGNMENT = (
            f"Username '{TEST_USERNAME_INVALID_TOO_SHORT}' is too short "
            "and should have at least 2 symbols."
        )
        assert str(exc) == TEST_ERR_MSG_TOO_SHORT_DIRECT_ASSIGNMENT
    else:
        assert False, (
            "Should raise Validation error "
            "when assigning invalid username directly to value field"
        )
    assert test_name.value == TEST_USERNAME_VALID

    print("Name tests passed.")
