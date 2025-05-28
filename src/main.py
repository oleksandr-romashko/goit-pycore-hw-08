"""Assistant bot application to manage a contact list via command-line interface."""
import sys
import logging

import colorama

from config import DEBUG

from cli.command import Command
from cli.command_handlers import (
    handle_load_app_data,
    handle_hello,
    handle_all,
    handle_add,
    handle_change,
    handle_delete,
    handle_phone,
    handle_add_birthday,
    handle_show_birthday,
    handle_birthdays,
    handle_help,
    handle_exit,
    handle_empty,
    handle_unknown,
)
from decorators.keyboard_interrupt_error import keyboard_interrupt_error
from utils.constants import (
    MSG_WELCOME_MESSAGE_TITLE,
    MSG_WELCOME_MESSAGE_SUBTITLE,
    MSG_INPUT_PROMPT,
)
from utils.input_parser import parse_input
from utils.log_config import init_logging

# TODO:
# - Add __getstate__ __setstate__ for pickle operations with state = copy.copy(self.__dict__).
# - (Optional) Future enhancement: Investigate options for storing global obj __book в src/services/contacts_manager.py as non-global object.
# - (Optional) Move prints into handler.
# - (Optional) Future enhancement: add handling remove_phone function.
# - (Optional) Future enhancement: Add app state data file locking while app in
#                                  use by another instance, e.g using 'portalocker'.

# Initialize the environment
init_logging(logging.DEBUG if DEBUG else logging.INFO)  # Logging
colorama.init(autoreset=True)  # Colorama for Windows compatibility


def get_user_input() -> str:
    """Prompt the user for a command and return the input string."""
    return input(f"\n{MSG_INPUT_PROMPT}: ")


@keyboard_interrupt_error(handle_exit)
def main():
    """Main function to run the assistant bot.

    Handles user input, command dispatching, and help generation
    for an Assistant bot CLI application.
    """
    # Display initial greeting
    print(colorama.Style.BRIGHT + f"\n{MSG_WELCOME_MESSAGE_TITLE}".upper())

    # Load previously saved app data, if any
    handle_load_app_data()

    # Display initial help message
    print(f"\n{MSG_WELCOME_MESSAGE_SUBTITLE}:\n")
    print(handle_help())

    while True:
        # Read user input
        user_input = get_user_input()

        # Handle empty input guard
        if not user_input:
            print(handle_empty())
            continue

        # Get command and parse arguments from input string
        command, args = parse_input(user_input)

        # Match input command with one from the menu using simple command dispatcher
        match command:
            case Command.HELLO:
                print(handle_hello())
            case Command.ALL:
                print(handle_all())
            case Command.ADD:
                print(handle_add(args))
            case Command.CHANGE:
                print(handle_change(args))
            case Command.DELETE:
                print(handle_delete(args))
            case Command.PHONE:
                print(handle_phone(args))
            case Command.ADD_BIRTHDAY:
                print(handle_add_birthday(args))
            case Command.SHOW_BIRTHDAY:
                print(handle_show_birthday(args))
            case Command.BIRTHDAYS:
                print(handle_birthdays())
            case Command.HELP:
                print(handle_help())
            case Command.EXIT | Command.CLOSE:
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

    menu = {
        Command.HELLO: {
            # Help for a menu item structure:
            #
            # A string showing expected arguments help text:
            #   <command> (required argument)
            #   [command] (optional argument) format
            #   empty if none are required.
            "args_str": "",
            # A string describing what this command does
            "description": "Greet the user",
            # The function that handles this command
            "handler": lambda _: handle_hello(),
            # Visibility flag - to show item or not in displayed help menu
            "visible": True,
        },
        Command.ALL: {
            "args_str": "",
            "description": "Display all contacts",
            "handler": lambda _: handle_all(),
            "visible": True,
        },
        Command.ADD: {
            "args_str": "<name> <phone>",
            "description": "Add a new contact or add phone to the existing one",
            "handler": handle_add,
            "visible": True,
        },
        Command.CHANGE: {
            "args_str": "<name> <old_phone> <new_phone>",
            "description": "Update contact's phone number",
            "handler": handle_change,
            "visible": True,
        },
        Command.DELETE: {
            "args_str": "<name>",
            "description": "Delete a contact",
            "handler": handle_delete,
            "visible": True,
        },
        Command.PHONE: {
            "args_str": "<name>",
            "description": "Show contact's phone number",
            "handler": handle_phone,
            "visible": True,
        },
        Command.ADD_BIRTHDAY: {
            "args_str": "<name> <birthday_date>",
            "description": "Add a birthday to the specified contact",
            "handler": handle_add_birthday,
            "visible": True,
        },
        Command.SHOW_BIRTHDAY: {
            "args_str": "<name>",
            "description": "Show the birthday of the specified contact",
            "handler": handle_show_birthday,
            "visible": True,
        },
        Command.BIRTHDAYS: {
            "args_str": "",
            "description": "Show upcoming birthdays within the upcoming week",
            "handler": lambda _: handle_birthdays(),
            "visible": True,
        },
        Command.HELP: {
            "args_str": "",
            "description": "Show available commands (this menu)",
            "handler": lambda _: handle_help(help_text),
            "visible": True,
        },
        Command.EXIT: {
            # Aliases as possible alternative commands,
            # e.g., 'exit' can also be triggered by 'close'
            "aliases": ["close"],
            "args_str": "",
            "description": "Exit the app",
            "handler": lambda _: handle_exit(),
            "visible": True,
        },
    }

    def generate_help_text(menu):
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
        cmd = cmd.lower()
        for item in menu:
            if cmd == item.lower():
                return item

        # Resolve aliases
        for key, meta in menu.items():
            aliases = [alias.lower() for alias in meta.get("aliases", [])]
            if cmd in aliases:
                return key

        # Fallback if command not found
        return ""

    help_text = generate_help_text(menu)

    # Display initial greeting
    print(colorama.Style.BRIGHT + f"\n{MSG_WELCOME_MESSAGE_TITLE}".upper())

    # Load previously saved app data, if any
    handle_load_app_data()

    # Display initial help message
    print(f"\n{MSG_WELCOME_MESSAGE_SUBTITLE}:\n")
    print(handle_help(help_text))

    while True:
        # Read user input
        user_input = get_user_input()

        # Handle empty input guard
        if not user_input:
            print(handle_empty())
            continue

        # Get command and parse arguments from input string
        command, args = parse_input(user_input)

        # Match input command with command from the menu
        command = resolve_command(command)
        metadata = menu.get(command)
        if not metadata:
            print(handle_unknown())
            continue

        # Call handling function
        handler = metadata.get("handler")
        result = handler(args)
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
