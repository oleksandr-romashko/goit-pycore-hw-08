"""
Reusable string utilities for formatting, truncation, and other text operations.
"""

from datetime import date

from utils.constants import (
    DATE_FORMAT_STR_REPRESENTATION,
    DEFAULT_TRUNCATE_LENGTH,
    DEFAULT_LINE_OFFSET,
    LINE_VALUE_GROUP_SEPARATION_SYMBOL,
    LINE_VALUE_LIST_SEPARATION_SYMBOL,
    MSG_HAVE_CONTACTS,
    MSG_BIRTHDAY_MOVED,
)
from utils.date_utils import format_date_str


def truncate_string(
    string: str,
    max_length: int = DEFAULT_TRUNCATE_LENGTH,
    suffix: str = "...",
    include_suffix_in_text_max_length: bool = False,
) -> str:
    """
    Truncates the given string to a maximum length and optionally appends a suffix.

    Args:
        string (str): The input string to truncate.
        max_length (int): The maximum allowed total length of the result string.
        suffix (str): The suffix to append (e.g. "...").
        include_suffix_in_text_max_length (bool): Whether the suffix length
        counts toward max_length.

    Returns:
        str: The truncated string with or without suffix as specified.

    Raises:
        TypeError: If input types are invalid.

    Examples:
        >>> truncate_string("Hello world", 5)
        'Hello...'
        >>> truncate_string("Hello world", 5, include_suffix_in_max_length=True)
        'He...'
    """
    if not isinstance(string, str):
        raise TypeError(
            f"During truncation expected 'string' to be of type 'str', "
            f"but was '{type(string).__name__}'"
        )

    if not isinstance(max_length, int):
        raise TypeError(
            f"During truncation expected 'max_length' to be of type 'int', "
            f"but was '{type(max_length).__name__}'"
        )

    if not isinstance(suffix, str):
        raise TypeError(
            f"During truncation expected 'suffix' to be of type 'str', "
            f"but was '{type(suffix).__name__}'"
        )

    # Guard empty values
    if not string and not suffix:
        return ""

    string_length = len(string)

    # Nothing to truncate -> return original string
    if string_length <= max_length:
        return string

    # Case where suffix has no influence on result and just added to the end of the truncated string
    if not include_suffix_in_text_max_length:
        return f"{string[:max_length]}{suffix}"

    # Following is a case when suffix length matters

    if max_length <= 0:
        return ""

    suffix_length = len(suffix)

    # Truncate suffix only
    if suffix_length >= max_length:
        return suffix[-max_length:]

    # There is at least one symbol in the string
    string_slice_end = max_length - suffix_length
    sliced_string = string[:string_slice_end]
    return f"{sliced_string}{suffix}"


def format_contacts_output(contacts_dict: dict) -> str:
    """
    Formats the contact dictionary into a readable string.

    Args:
        contacts_dict (dict): A dictionary of contacts with their details.

    Returns:
        str: Formatted string output.
    """
    # Format output header and aligned lines
    count = len(contacts_dict)
    suffix = "" if count == 1 else "s"
    header = MSG_HAVE_CONTACTS.format(count, suffix)

    # Format output aligned lines
    items = []
    for name, details in contacts_dict.items():
        items.append(
            {
                "name": name,
                "phones": details.get("phones", []),
                "birthday": details.get("birthday"),
            }
        )

    # Sort by name (case-insensitive)
    items = sorted(items, key=lambda item: item["name"].casefold())

    return format_text_output(output_result={"message": header, "items": items})


def format_text_output(
    output_result: dict[str, str | list[dict]],
    lines_offset: str = DEFAULT_LINE_OFFSET,
) -> str:
    """
    Format the structured result dictionary into a human-readable text output.

    This function takes a result dictionary containing a message and optional list of items
    (such as contacts), and formats them into aligned multiline string output. Items are expected
    to contain keys like 'name', 'phones', 'birthday', or 'congratulation' (optionally with
    'congratulation_actual').

    Args:
        result (dict): A dictionary with the keys:
            - "message" (str): The main header or summary message.
            - "items" (list[dict], optional): A list of dictionaries containing item details.
        lines_offset (str, optional): A string prefix for each item line, e.g., indentation.

    Returns:
        str: A formatted string suitable for display in a CLI interface.

    Notes:
        - If no items are provided, only the message is returned.
        - The output aligns all item names to the same column width.
        - Special handling is applied to display congratulation dates with weekday adjustments.
    """
    message = output_result.get("message")
    items = output_result.get("items", [])

    if not items:
        return message

    lines = [f"{message}:"] if message else []
    max_name_len = max(len(item.get("name", "")) for item in items)
    has_birthday = any(
        item.get("birthday") and item.get("birthday") != "None" for item in items
    )
    for item in items:
        lines.append(__format_item(item, lines_offset, max_name_len, has_birthday))

    return "\n".join(lines)


def __format_item(
    item: dict, lines_offset: str, max_name_len: int, has_birthday: bool
) -> str:
    # name
    name = item.get("name", "")

    values = []

    # birthday
    birthday_raw = item.get(
        "birthday"
    )  # May be: None or "None" str or ISO format date str
    birthday = ""
    if birthday_raw and birthday_raw != "None":
        birthday_date_obj = date.fromisoformat(birthday_raw)
        formatted_birthday_date_str = format_date_str(birthday_date_obj)
        birthday = f"birthday {formatted_birthday_date_str}"
        values.append(birthday)
    elif has_birthday:
        birthday = " ".ljust(len(f"birthday {DATE_FORMAT_STR_REPRESENTATION}"))
        values.append(birthday)

    # phones
    phones_raw = item.get("phones")  # May be: None or "None" str or []
    phones_label = "phones "
    if isinstance(phones_raw, list):
        joined_phones = f"{LINE_VALUE_LIST_SEPARATION_SYMBOL} ".join(phones_raw)
        values.append(f"{phones_label}{joined_phones}")
    elif phones_raw and phones_raw != "None":
        values.append(phones_label)

    # upcoming congratulation date
    congratulation_raw = item.get("congratulation")
    congratulation = ""
    if congratulation_raw and congratulation_raw != "None":
        congratulation_date_obj = date.fromisoformat(congratulation_raw)
        formatted_congratulation_date_str = format_date_str(congratulation_date_obj)
        congratulation = f"{formatted_congratulation_date_str}"
    # additional note about moved congratulation date
    actual_raw = item.get("congratulation_actual")
    actual_info = ""
    if actual_raw and actual_raw != "None" and actual_raw != congratulation_raw:
        actual_date_obj = date.fromisoformat(actual_raw)
        actual_date_str = format_date_str(actual_date_obj)
        actual_info = f"{MSG_BIRTHDAY_MOVED.format(actual_date_str)}"
        congratulation = f"{congratulation} {actual_info}"
    if congratulation:
        values.append(congratulation)

    return (
        f"{lines_offset}{name.ljust(max_name_len)} : "
        f"{(' ' + LINE_VALUE_GROUP_SEPARATION_SYMBOL + ' ').join(values)}"
    )


if __name__ == "__main__":
    # TESTS

    # Truncate tests

    TEST_TRUNCATE_STRING = "Hello world!"
    # test tweaking string value
    assert truncate_string(TEST_TRUNCATE_STRING) == "Hello wo..."
    assert (
        truncate_string(TEST_TRUNCATE_STRING, include_suffix_in_text_max_length=True)
        == "Hello..."
    )
    assert truncate_string("12345678") == "12345678"
    assert (
        truncate_string("12345678", include_suffix_in_text_max_length=True)
        == "12345678"
    )
    assert truncate_string("abc") == "abc"
    assert truncate_string("abc", include_suffix_in_text_max_length=True) == "abc"
    assert truncate_string("") == ""
    assert truncate_string("", include_suffix_in_text_max_length=True) == ""
    # test tweaking max_length value
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=13) == TEST_TRUNCATE_STRING
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=13, include_suffix_in_text_max_length=True
        )
        == TEST_TRUNCATE_STRING
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=12) == TEST_TRUNCATE_STRING
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=12, include_suffix_in_text_max_length=True
        )
        == TEST_TRUNCATE_STRING
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=9) == "Hello wor..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=9, include_suffix_in_text_max_length=True
        )
        == "Hello ..."
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=3) == "Hel..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=3, include_suffix_in_text_max_length=True
        )
        == "..."
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=2) == "He..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=2, include_suffix_in_text_max_length=True
        )
        == ".."
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=1) == "H..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=1, include_suffix_in_text_max_length=True
        )
        == "."
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=0) == "..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=0, include_suffix_in_text_max_length=True
        )
        == ""
    )
    assert truncate_string(TEST_TRUNCATE_STRING, max_length=-1) == "Hello world..."
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, max_length=-1, include_suffix_in_text_max_length=True
        )
        == ""
    )
    # test tweaking suffix value
    assert truncate_string(TEST_TRUNCATE_STRING, suffix="###") == "Hello wo###"
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="###", include_suffix_in_text_max_length=True
        )
        == "Hello###"
    )
    assert truncate_string(TEST_TRUNCATE_STRING, suffix="123") == "Hello wo123"
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="123", include_suffix_in_text_max_length=True
        )
        == "Hello123"
    )
    assert truncate_string(TEST_TRUNCATE_STRING, suffix="") == "Hello wo"
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING, suffix="", include_suffix_in_text_max_length=True
        )
        == "Hello wo"
    )
    assert (
        truncate_string(TEST_TRUNCATE_STRING, suffix="12345678") == "Hello wo12345678"
    )
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING,
            suffix="12345678",
            include_suffix_in_text_max_length=True,
        )
        == "12345678"
    )
    assert (
        truncate_string(TEST_TRUNCATE_STRING, suffix="123456789") == "Hello wo123456789"
    )
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING,
            suffix="123456789",
            include_suffix_in_text_max_length=True,
        )
        == "23456789"
    )
    assert (
        truncate_string(TEST_TRUNCATE_STRING, suffix="1234567890")
        == "Hello wo1234567890"
    )
    assert (
        truncate_string(
            TEST_TRUNCATE_STRING,
            suffix="1234567890",
            include_suffix_in_text_max_length=True,
        )
        == "34567890"
    )
    assert truncate_string("", suffix="") == ""
    assert truncate_string("", suffix="", include_suffix_in_text_max_length=True) == ""

    try:
        truncate_string(123)
    except TypeError as exc:
        assert "expected 'string'" in str(exc)
    else:
        assert (
            False
        ), "Should raise TypeError when passed incorrect type into truncate_string"

    try:
        truncate_string("abc", max_length="5")
    except TypeError:
        pass
    else:
        assert False, "Should raise TypeError when max_length is not int"

    # test format_line_output

    TEST_FORMAT_TEXT_OUTPUT_1_1_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
        },
        lines_offset="  ",
    )
    TEST_FORMAT_TEXT_OUTPUT_1_1_EXPECTED = "Test message header"
    assert TEST_FORMAT_TEXT_OUTPUT_1_1_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_1_1_RESULT

    TEST_FORMAT_TEXT_OUTPUT_2_1_RESULT = format_text_output(
        output_result={
            "items": [
                {
                    "name": "test username",
                    "birthday": "2024-12-23",
                }
            ],
        },
        lines_offset="",
    )
    TEST_FORMAT_TEXT_OUTPUT_2_1_EXPECTED = "test username : birthday 23.12.2024"
    assert TEST_FORMAT_TEXT_OUTPUT_2_1_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_2_1_RESULT

    TEST_FORMAT_TEXT_OUTPUT_3_2_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username",
                    "phones": [],
                }
            ],
        },
    )
    TEST_FORMAT_TEXT_OUTPUT_3_2_EXPECTED = (
        "Test message header:\n  test username : phones "
    )
    assert TEST_FORMAT_TEXT_OUTPUT_3_2_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_3_2_RESULT

    TEST_FORMAT_TEXT_OUTPUT_3_3_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username",
                    "phones": ["1234567890"],
                }
            ],
        },
    )
    TEST_FORMAT_TEXT_OUTPUT_3_3_EXPECTED = (
        "Test message header:\n  test username : phones 1234567890"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_3_3_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_3_3_RESULT

    TEST_FORMAT_TEXT_OUTPUT_3_4_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username",
                    "phones": ["1234567890", "0987654321"],
                }
            ],
        },
    )
    TEST_FORMAT_TEXT_OUTPUT_3_4_EXPECTED = (
        "Test message header:\n  test username : phones 1234567890, 0987654321"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_3_4_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_3_4_RESULT

    TEST_FORMAT_TEXT_OUTPUT_3_5_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username 1",
                    "phones": ["1111111111"],
                },
                {
                    "name": "test username 2",
                    "phones": ["2222222222", "3333333333"],
                },
            ],
        },
    )
    TEST_FORMAT_TEXT_OUTPUT_3_5_EXPECTED = (
        "Test message header:\n"
        "  test username 1 : phones 1111111111\n"
        "  test username 2 : phones 2222222222, 3333333333"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_3_5_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_3_5_RESULT

    TEST_FORMAT_TEXT_OUTPUT_4_1_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username",
                    "birthday": "2024-12-23",
                    "phones": ["1234567890", "0987654321"],
                }
            ],
        },
    )
    TEST_FORMAT_TEXT_OUTPUT_4_1_EXPECTED = (
        "Test message header:\n"
        "  test username : birthday 23.12.2024 : phones 1234567890, 0987654321"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_4_1_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_4_1_RESULT

    TEST_FORMAT_TEXT_OUTPUT_5_1_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username 1",
                    "phones": ["1234567890", "0987654321"],
                },
                {
                    "name": "test username 2",
                    "birthday": "2024-12-23",
                    "phones": ["1111111111", "2222222222"],
                },
                {
                    "name": "test username 3",
                    "phones": ["3333333333"],
                },
                {
                    "name": "test username 4",
                    "birthday": "2024-12-24",
                    "phones": ["4444444444"],
                },
            ],
        },
        lines_offset="👤 ",
    )
    TEST_FORMAT_TEXT_OUTPUT_5_1_EXPECTED = (
        "Test message header:\n"
        "👤 test username 1 :                     : phones 1234567890, 0987654321\n"
        "👤 test username 2 : birthday 23.12.2024 : phones 1111111111, 2222222222\n"
        "👤 test username 3 :                     : phones 3333333333\n"
        "👤 test username 4 : birthday 24.12.2024 : phones 4444444444"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_5_1_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_5_1_RESULT

    TEST_FORMAT_TEXT_OUTPUT_6_1_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username 1",
                    "congratulation": "2024-12-23",
                }
            ],
        },
    )
    TEST_FORMAT_TEXT_OUTPUT_6_1_EXPECTED = (
        "Test message header:\n  test username 1 : 23.12.2024"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_6_1_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_6_1_RESULT

    TEST_FORMAT_TEXT_OUTPUT_6_2_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username 1",
                    "congratulation": "2024-12-28",
                    "congratulation_actual": "2024-12-30",
                }
            ],
        },
    )
    TEST_FORMAT_TEXT_OUTPUT_6_2_EXPECTED = (
        "Test message header:\n"
        "  test username 1 : 28.12.2024 (moved to closest weekday from 30.12.2024)"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_6_2_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_6_2_RESULT

    TEST_FORMAT_TEXT_OUTPUT_6_3_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username 1",
                    "congratulation": "2024-12-23",
                },
                {
                    "name": "test username 1",
                    "congratulation": "2024-12-28",
                    "congratulation_actual": "2024-12-30",
                },
            ],
        },
    )
    TEST_FORMAT_TEXT_OUTPUT_6_3_EXPECTED = (
        "Test message header:\n"
        "  test username 1 : 23.12.2024\n"
        "  test username 1 : 28.12.2024 (moved to closest weekday from 30.12.2024)"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_6_3_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_6_3_RESULT

    TEST_FORMAT_TEXT_OUTPUT_6_4_RESULT = format_text_output(
        output_result={
            "message": "Test message header",
            "items": [
                {
                    "name": "test username 1",
                    "congratulation": "2024-12-23",
                },
                {
                    "name": "test username 1",
                    "congratulation": "2024-12-28",
                    "congratulation_actual": "2024-12-30",
                },
            ],
        },
        lines_offset="👤 ",
    )
    TEST_FORMAT_TEXT_OUTPUT_6_4_EXPECTED = (
        "Test message header:\n"
        "👤 test username 1 : 23.12.2024\n"
        "👤 test username 1 : 28.12.2024 (moved to closest weekday from 30.12.2024)"
    )
    assert TEST_FORMAT_TEXT_OUTPUT_6_4_EXPECTED == TEST_FORMAT_TEXT_OUTPUT_6_4_RESULT

    print("Text Utils tests passed.")
