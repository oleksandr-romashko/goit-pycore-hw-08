"""
Field base class for storing values in contact records.

This module defines the base `Field` class used for contact fields.
It provides basic storage and string conversion behavior.
"""

from dataclasses import dataclass


@dataclass(repr=False)
class Field:
    """
    Base class for contact record fields.

    Stores a single value and provides a default string representation.

    Provides common functionality including: __str__(), __repr__(), to_dict().
    Instances of Field are compared (__eq__) based on their stored value.
    """

    _value: any

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}(value={repr(self.value)})"

    def to_dict(self) -> str:
        """
        Return the string representation of the field value.

        Returns:
            str: The field value as a string.
        """
        return str(self.value)

    @property
    def value(self) -> any:
        """
        Retrieves the stored value of the field.

        This property provides read access to the internal `_value` attribute,
        which represents the field's content. It is used by subclasses to access
        or override the behavior of getting a field's value.

        Returns:
            Any: The current value stored in the field.
        """
        return self._value

    @value.setter
    def value(self, value: any) -> None:
        self._value = value


if __name__ == "__main__":
    # TESTS

    TEST_VALUE_STR = "some_value"
    TEST_VALUE_DATE = 42

    test_field_of_str = Field(TEST_VALUE_STR)
    assert isinstance(test_field_of_str.value, str)
    assert str(test_field_of_str) == TEST_VALUE_STR
    assert test_field_of_str == Field(TEST_VALUE_STR)  # __eq__ override test
    assert (
        repr(test_field_of_str) == "Field(value='some_value')"
    )  # __repr__ override test

    test_field_of_int = Field(TEST_VALUE_DATE)
    assert isinstance(test_field_of_int.value, int)
    assert str(test_field_of_int) == str(TEST_VALUE_DATE)
    assert test_field_of_int == Field(TEST_VALUE_DATE)  # __eq__ override test
    assert repr(test_field_of_int) == "Field(value=42)"  # __repr__ override test

    print("Field tests passed.")
