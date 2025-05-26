"""
Birthday field for storing and validating birth dates.

This module defines the `Birthday` class which extends `Field` and ensures
the birth date is valid on assignment or update, following the expected format.
"""

from datetime import date

from services.address_book.field import Field

from utils.constants import DATE_FORMAT_STR_REPRESENTATION
from utils.date_utils import format_date_str
from validators.args_validators import validate_argument_type
from validators.errors import ValidationError
from validators.field_validators import validate_date_format


class Birthday(Field):
    """
    Class for storing and validating birth dates.

    Ensures the date matches the expected birthday format during initialization
    and on value changes.
    """

    def __init__(self, date_value: str | date):
        """
        Initiates Birthday instance.

        Raises:
            TypeError: If date value is not one of incorrect types.
            ValidationError: If bad date format is provided.
        """
        date_obj = self._validate_and_parse_date(date_value)
        super().__init__(date_obj)

    def __str__(self):
        return format_date_str(self.value)

    def to_dict(self) -> str | None:
        """
        Return the birthday value as an ISO-formatted date string.

        Returns:
            str | None: The birthday in 'YYYY-MM-DD' format if set, otherwise None.
        """
        return self.value.isoformat() if self.value else None

    @Field.value.setter
    def value(self, date_value: str | date):
        """
        Sets a new validated birthday date value.

        Raises:
            TypeError: If date value is not one of incorrect types.
            ValidationError: If bad date format is provided.

        Overrides setter from parent adding validation.
        """
        date_obj = self._validate_and_parse_date(date_value)
        self._value = date_obj

    def _validate_and_parse_date(self, date_value: str | date) -> date:
        validate_argument_type(date_value, (str, date))
        if isinstance(date_value, str):
            date_value = validate_date_format(date_value)
        return date_value


if __name__ == "__main__":
    # TESTS

    # Test data
    TEST_DATE_STR_VALID = "02.03.2000"
    TEST_DATE_STR_VALID_REPR = "Birthday(value=datetime.date(2000, 3, 2))"
    TEST_DATE_STR_WITH_INVALID_FORMAT = "2000-03-02"
    TEST_DATE_STR_IN_THE_FUTURE = "01.01.2200"

    test_date_obj_valid = date(2000, 3, 2)
    test_date_obj_in_the_future = date(2200, 1, 1)

    # Test creation of instance with valid date string
    test_birthday_1 = Birthday(TEST_DATE_STR_VALID)
    assert isinstance(test_birthday_1.value, date)
    assert format_date_str(test_birthday_1.value) == TEST_DATE_STR_VALID

    # Test str and repr
    assert str(test_birthday_1) == TEST_DATE_STR_VALID
    assert repr(test_birthday_1) == TEST_DATE_STR_VALID_REPR

    # Test creation of instance with invalid date format string
    try:
        Birthday(TEST_DATE_STR_WITH_INVALID_FORMAT)
    except ValidationError as exc:
        TEST_ERR_MSG_INVALID_DATE_FORMAT_WHEN_INIT = (
            f"Invalid date format '{TEST_DATE_STR_WITH_INVALID_FORMAT}'. "
            f"Use {DATE_FORMAT_STR_REPRESENTATION} format."
        )
        assert str(exc) == TEST_ERR_MSG_INVALID_DATE_FORMAT_WHEN_INIT
    else:
        assert (
            False
        ), "Should raise Validation error when birthday date has invalid format"

    # Test creation of instance with date string in the future
    Birthday(TEST_DATE_STR_IN_THE_FUTURE)

    # Test direct assignment to Birthday instance value a valid date string
    test_birthday_2 = Birthday(TEST_DATE_STR_VALID)
    test_birthday_2.value = TEST_DATE_STR_VALID
    assert isinstance(test_birthday_2.value, date)
    assert format_date_str(test_birthday_2.value) == TEST_DATE_STR_VALID

    # Test direct assignment to Birthday instance value an invalid date format string
    test_birthday_3 = Birthday(TEST_DATE_STR_VALID)
    try:
        test_birthday_3.value = TEST_DATE_STR_WITH_INVALID_FORMAT
    except ValidationError as exc:
        TEST_ERR_MSG_INVALID_DATE_FORMAT_WHEN_ASSIGN_VALUE = (
            f"Invalid date format '{TEST_DATE_STR_WITH_INVALID_FORMAT}'. "
            f"Use {DATE_FORMAT_STR_REPRESENTATION} format."
        )
        assert str(exc) == TEST_ERR_MSG_INVALID_DATE_FORMAT_WHEN_ASSIGN_VALUE
    else:
        assert False, (
            "Should raise Validation error "
            "when updating Birthday instance value directly with invalid date string value"
        )
    assert isinstance(test_birthday_3.value, date)
    assert format_date_str(test_birthday_3.value) == TEST_DATE_STR_VALID

    # Test direct assignment to Birthday instance value a date string in the future
    test_birthday_4 = Birthday(TEST_DATE_STR_VALID)
    test_birthday_4.value = TEST_DATE_STR_IN_THE_FUTURE
    assert isinstance(test_birthday_4.value, date)
    assert format_date_str(test_birthday_4.value) == TEST_DATE_STR_IN_THE_FUTURE

    # Test creation of instance with valid date object
    test_birthday_5 = Birthday(test_date_obj_valid)
    assert isinstance(test_birthday_5.value, date)
    assert format_date_str(test_birthday_5.value) == TEST_DATE_STR_VALID

    # Test creation of instance with date object in the future
    Birthday(test_date_obj_in_the_future)

    # Test direct assignment to Birthday instance value a valid date object
    test_birthday_6 = Birthday(test_date_obj_valid)
    test_birthday_6.value = TEST_DATE_STR_VALID
    assert isinstance(test_birthday_6.value, date)
    assert format_date_str(test_birthday_6.value) == TEST_DATE_STR_VALID

    # Test direct assignment to Birthday instance value a date object in the future
    test_birthday_7 = Birthday(test_date_obj_valid)
    test_birthday_7.value = test_date_obj_in_the_future
    assert isinstance(test_birthday_7.value, date)
    assert format_date_str(test_birthday_7.value) == TEST_DATE_STR_IN_THE_FUTURE

    print("Birthday tests passed.")
