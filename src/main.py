"""Assistant bot application to manage a contact list via command-line interface."""
import sys
import logging

from colorama import init, Style

from config import DEBUG

from cli.command_handlers import (
    handle_hello,
    handle_all,
    handle_add,
    handle_change,
    handle_phone,
    handle_add_birthday,
    handle_show_birthday,
    handle_birthdays,
    handle_help,
    handle_exit,
    handle_unknown,
)
from decorators.keyboard_interrupt_error import keyboard_interrupt_error
from services.address_book.address_book import AddressBook
from utils.constants import (
    MSG_WELCOME_MESSAGE_TITLE,
    MSG_WELCOME_MESSAGE_SUBTITLE,
    MSG_INPUT_PROMPT,
    MENU_HELP_STR,
    MSG_INVALID_EMPTY_COMMAND,
)
from utils.input_parser import parse_input
from utils.log_config import init_logging


# Initialize the environment
init_logging(logging.DEBUG if DEBUG else logging.INFO)  # Logging
init(autoreset=True)  # Colorama for Windows compatibility


def print_greeting(help_text: str = "") -> None:
    """Print the welcome message and optional help text."""
    print(Style.BRIGHT + f"\n{MSG_WELCOME_MESSAGE_TITLE}".upper())
    print(f"\n{MSG_WELCOME_MESSAGE_SUBTITLE}:")
    print(f"\n{help_text}")


def get_user_input() -> str:
    """Prompt the user for a command and return the input string."""
    return input(f"\n{MSG_INPUT_PROMPT}: ")


@keyboard_interrupt_error(handle_exit)
def main():
    """Main function to run the assistant bot.

    Handles user input, command dispatching, and help generation
    for an Assistant bot CLI application.
    """

    book = AddressBook()

    # Display initial greeting and help text
    print_greeting(MENU_HELP_STR)

    while True:
        # Read user input
        user_input = get_user_input()
        if not user_input:
            print(f"{MSG_INVALID_EMPTY_COMMAND}.")
            continue

        # Get command and arguments from input string
        command, args = parse_input(user_input)

        # Match input command with one from the menu
        match command:
            case "hello":
                print(handle_hello())
            case "all":
                print(handle_all(book))
            case "add":
                print(handle_add(args, book))
            case "change":
                print(handle_change(args, book))
            case "phone":
                print(handle_phone(args, book))
            case "add-birthday":
                print(handle_add_birthday(args, book))
            case "show-birthday":
                print(handle_show_birthday(args, book))
            case "birthdays":
                print(handle_birthdays(book))
            case "help":
                print(handle_help())
            case "exit" | "close":
                # Terminates the application
                handle_exit()
            case _:
                print(handle_unknown())


@keyboard_interrupt_error(handle_exit)
def main_alternative():
    """
    Main function to run the assistant bot using a data-driven menu configuration.

    Handles user input, command dispatching, and help generation
    for an Assistant bot CLI application.
    """
    book = AddressBook()

    menu = {
        "hello": {
            # Help for the menu item structure:
            # A string showing expected arguments help text
            # in <command> (required argument)
            # or [command] (optional argument) format
            # or empty if none are required.
            "args_str": "",
            # A string describing what this command does
            "description": "Greet the user",
            # The function that handles this command
            "handler": lambda _, __: handle_hello(),
            "visible": True,
        },
        "all": {
            "args_str": "",
            "description": "Display all contacts",
            "handler": lambda _, book: handle_all(book),
            "visible": True,
        },
        "add": {
            "args_str": "<name> <phone>",
            "description": "Add a new contact or add phone to the existing one",
            "handler": handle_add,
            "visible": True,
        },
        "change": {
            "args_str": "<name> <old_phone> <new_phone>",
            "description": "Update contact's phone number",
            "handler": handle_change,
            "visible": True,
        },
        "phone": {
            "args_str": "<name>",
            "description": "Show contact's phone number",
            "handler": handle_phone,
            "visible": True,
        },
        "add-birthday": {
            "args_str": "<name> <birthday_date>",
            "description": "Add a birthday to the specified contact",
            "handler": handle_add_birthday,
            "visible": True,
        },
        "show-birthday": {
            "args_str": "<name>",
            "description": "Show the birthday of the specified contact",
            "handler": handle_show_birthday,
            "visible": True,
        },
        "birthdays": {
            "args_str": "",
            "description": "Show upcoming birthdays within the upcoming week",
            "handler": lambda _, book: handle_birthdays(book),
            "visible": True,
        },
        "help": {
            "args_str": "",
            "description": "Show available commands (this menu)",
            "handler": lambda _, __: help_text,
            "visible": True,
        },
        "exit": {
            # Aliases as possible alternative commands,
            # e.g., 'exit' can also be triggered by 'close'
            "aliases": ["close"],
            "args_str": "",
            "description": "Exit the app",
            "handler": lambda _, __: handle_exit(),
            "visible": True,
        },
    }

    def generate_help_text():
        """
        Generate formatted help text from available commands.

        Returns:
            str: Aligned list of commands with their descriptions.
        """
        help_entries = []

        # Prepare all command strings with their details
        for command, metadata in menu.items():
            # Skip commands that are hidden from help (visible=False by design)
            if not metadata.get("visible", True):
                continue

            # Format aliases: "exit (or close)"
            aliases = metadata.get("aliases", [])
            alias_str = f" (or {', '.join(aliases)})" if aliases else ""

            # Build the command string with arguments
            command_str = f"{command}{alias_str} {metadata['args_str']}".strip()

            # Append command string and description to the help list
            help_entries.append((command_str, metadata["description"]))

        # Sort the help entries alphabetically
        # Turned off for now
        # help_entries.sort(key=lambda x: x[0])

        # Find the longest command string to align the output
        max_command_length = 0
        if help_entries:
            max_command_length = max(len(cmd_str) for cmd_str, _ in help_entries)

        # Format help lines with aligned commands and descriptions
        formatted_help_lines = [
            f"{cmd_str.ljust(max_command_length)} - {description}"
            for cmd_str, description in help_entries
        ]

        return "\n".join(formatted_help_lines)

    def resolve_command(cmd: str) -> str:
        """
        Resolves a user input command to its canonical form.

        Checks if the input command matches a registered command in the menu.
        If not found, attempts to resolve it via known aliases.

        Args:
            cmd (str): The command input string entered by the user.

        Returns:
            str: The matched canonical command string, or an empty string if not recognized.
        """
        for item in menu:
            if cmd.lower == item.lower():
                return item

        # Resolve aliases
        for key, meta in menu.items():
            aliases = [alias.lower() for alias in meta.get("aliases", [])]
            if cmd in aliases:
                return key

        # Fallback if command not found
        return ""

    help_text = generate_help_text()

    # Display initial greeting and help text
    print_greeting(help_text)

    while True:
        # Read user input
        user_input = get_user_input()
        if not user_input:
            print(f"{MSG_INVALID_EMPTY_COMMAND}.")
            continue

        # Get command and arguments from input string
        command, args = parse_input(user_input)

        # Match input command with command from the menu
        command = resolve_command(command)
        metadata = menu.get(command)
        if not metadata:
            print(handle_unknown())
            continue

        # Call handling function
        handler = metadata.get("handler")
        result = handler(args, book)
        if result:
            print(result)


if __name__ == "__main__":
    # Choose solution approach
    if "--alternative" in sys.argv:
        # Launch in the alternative mode (Data-Driven Menu)
        main_alternative()
    else:
        # Launch in the typical mode (menu handling in match case)
        main()
