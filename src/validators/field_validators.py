"""
Validators for field values (name, phone, etc.).

Validators raise ValidationError with descriptive messages if validation fails.
"""
import re
from datetime import date as datetime_day

from utils.constants import (
    DATE_FORMAT_STR_REPRESENTATION,
    NAME_MIN_LENGTH,
    NAME_MAX_LENGTH,
    MAX_DISPLAY_NAME_LEN,
    PHONE_FORMAT_DESC_STR,
    USERNAME_EMPTY_ERROR,
    USERNAME_TOO_SHORT_ERROR,
    USERNAME_TOO_LONG_ERROR,
    PHONE_EMPTY_ERROR,
    PHONE_INVALID_FORMAT_ERROR,
    DATE_FORMAT_INVALID_ERROR,
    BIRTHDAY_IN_FUTURE_ERROR,
)
from utils.date_utils import parse_date, format_date_str
from utils.text_utils import truncate_string

from validators.errors import ValidationError


def validate_username_length(username: str) -> None:
    """
    Validates username against minimum and maximum allowed lengths.

    Args:
        username (str): name to validate.

    Raises:
        ValidationError: If username is too short or too long.
    """
    username = username.strip()

    if not username:
        raise ValidationError(USERNAME_EMPTY_ERROR)

    if len(username) < NAME_MIN_LENGTH:
        err_msg_too_short = USERNAME_TOO_SHORT_ERROR.format(
            username=username, min_len=NAME_MIN_LENGTH
        )
        raise ValidationError(err_msg_too_short)

    if len(username) > NAME_MAX_LENGTH:
        truncated_username = truncate_string(
            username,
            max_length=MAX_DISPLAY_NAME_LEN,
            include_suffix_in_text_max_length=True,
        )
        err_msg_too_long = USERNAME_TOO_LONG_ERROR.format(
            username=truncated_username, max_len=NAME_MAX_LENGTH
        )
        raise ValidationError(err_msg_too_long)


def validate_phone_number(phone: str) -> None:
    """
    Validates phone number format: 10 digits, optionally prefixed with '+'.

    Args:
        phone (str): phone number to validate.

    Raises:
        ValidationError: If phone number format is invalid.
    """
    phone = phone.strip()

    if not phone:
        raise ValidationError(PHONE_EMPTY_ERROR)

    # Remove all non-digit characters for counting digits, incl. "+" symbol
    digits_only = re.sub(r"\D", "", phone)

    if not len(digits_only) == 10:
        raise ValidationError(
            PHONE_INVALID_FORMAT_ERROR.format(
                phone=phone, format_description=PHONE_FORMAT_DESC_STR
            )
        )


def validate_date_format(value: str) -> datetime_day:
    """
    Validates and parses a date string into a date object.

    Args:
        value (str): The date string to validate, expected in the defined format.

    Returns:
        date: A `datetime.date` object representing the validated date string.

    Raises:
        ValidationError: If the input does not match the expected format.
    """
    try:
        date_obj = parse_date(value)
        return date_obj
    except ValueError as exc:
        error_msg = DATE_FORMAT_INVALID_ERROR.format(
            value=value, expected_format=DATE_FORMAT_STR_REPRESENTATION
        )
        raise ValidationError(error_msg) from exc


def validate_birthday_is_in_the_past(date: str) -> None:
    """
    Validates that the given birthday date passed or is today.

    Args:
        birthday (date): A `datetime.date` object representing the birthday.

    Raises:
        ValidationError: If the birthday is in the future.
    """
    today = date.today()
    if date > today:
        birthday_str = format_date_str(date)
        raise ValidationError(BIRTHDAY_IN_FUTURE_ERROR.format(value=birthday_str))
