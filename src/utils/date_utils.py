"""
Utilities to work with dates (parsing, formatting, checking leap years, etc.).

This module provides helper functions for working with date values.
"""

from datetime import datetime, date

from utils.constants import DATE_FORMAT


def is_leap_year(year: int) -> bool:
    """Determines whether a given year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def parse_date(date_str: str) -> date:
    """Parses a date string into a `datetime.date` object."""
    return datetime.strptime(date_str, DATE_FORMAT).date()


def format_date_str(date_obj: date) -> str:
    """Converts a `datetime.date` object into a formatted string."""
    return date.strftime(date_obj, DATE_FORMAT)


if __name__ == "__main__":
    assert is_leap_year(2000) is True
    assert is_leap_year(2004) is True
    assert is_leap_year(2001) is False

    assert (format_date_str(date(2000, 1, 1))) == "01.01.2000"

    print("Date Utils tests passed.")
