"""
Validators for command-line argument structure before further operations.

These functions check the number and presence of CLI arguments and types.
"""

from datetime import date

from utils.constants import ERR_ARG_COUNT_ERROR, ERR_TYPE_ERROR
from validators.errors import ValidationError


def ensure_args_have_n_arguments(
    args: list[str], expected: int, details: str = ""
) -> None:
    """
    Ensures the given number of non-empty arguments are provided.

    Args:
        args (list[str]): List of arguments.
        expected (int): The number of expected non-empty arguments.
        details (str, optional): Additional message for clarification.

    Raises:
        ValidationError: If the number of arguments is incorrect or any are empty.
    """
    if len(args) != expected or not all(arg.strip() for arg in args):
        plural = "s" if expected != 1 else ""
        details_formatted = f" ({details})" if details else ""
        msg = ERR_ARG_COUNT_ERROR.format(
            expected=expected, plural=plural, details=details_formatted
        )
        raise ValidationError(msg)


def validate_argument_type(obj: object, obj_type: any) -> None:
    """
    Ensures the provided object is of one of the expected types.

    Args:
        obj: The object to check.
        obj_type: The expected type or tuple/list of types.

    Raises:
        TypeError: If the object's type is incorrect.
    """
    if not isinstance(obj, obj_type):
        if isinstance(obj_type, (tuple, list)):
            expected = ", ".join([o_type.__name__ for o_type in obj_type])
        else:
            expected = obj_type.__name__

        actual = type(obj).__name__
        raise TypeError(ERR_TYPE_ERROR.format(expected=expected, actual=actual))


if __name__ == "__main__":
    # TESTS

    validate_argument_type("string", str)
    validate_argument_type("string", (str, date))
    validate_argument_type(date(2025, 5, 13), (str, date))

    try:
        validate_argument_type({}, str)
    except TypeError as exc:
        assert str(exc) == "Expected type 'str', but received type 'dict'."
    else:
        assert False, "Should raise TypeError error when type is not of expected type."

    try:
        validate_argument_type([], (str, date))
    except TypeError as exc:
        assert str(exc) == "Expected type 'str, date', but received type 'list'."
    else:
        assert False, "Should raise TypeError error when type is not of expected types."

    print("Args Validator tests passed.")
