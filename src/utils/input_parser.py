"""
Utility module for parsing user input into commands and arguments.

Provides a function to extract the command and associated arguments
from a raw input string, enabling structured command processing.
"""


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """
    Parse the user input into a command and its associated arguments.

    This function splits the input string into a command (the first word)
    and a list of arguments (the remaining words). The command is
    normalized to lowercase to ensure case-insensitive matching.

    Args:
        user_input (str): The raw input string entered by the user.

    Returns:
        tuple: A tuple containing the command (str) and the arguments (list of str).

    If the input is empty or contains only whitespace, it returns an empty command and no arguments.
    """
    # Handle the case where the input is empty or contains only whitespace
    if not user_input.strip():
        return "", []

    # Split the input into command and arguments
    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]

    return command, args
