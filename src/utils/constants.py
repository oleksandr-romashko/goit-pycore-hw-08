"""
This module defines static messages, prompts, and configuration constants
used across the assistant bot application. These constants include UI strings,
user guidance text, validation rules, and formatting hints.
"""

# === CLI ===

# Welcome & Exit Messages
MSG_WELCOME_MESSAGE_TITLE = "Welcome to the assistant bot!"
MSG_WELCOME_MESSAGE_SUBTITLE = "Here you have the list of available options for you"
MSG_HELLO_MESSAGE = "How can I help you?"
MSG_APP_PURPOSE_MESSAGE = "If you'd like, I can help you manage your phone contacts"
MSG_EXIT_MESSAGE = "Good bye!"
MSG_INVALID_EMPTY_COMMAND = "No command entered. Please try again"
INVALID_COMMAND_MESSAGE = "Invalid command"

# UI Prompts
MSG_HELP_AWARE_TIP = "type 'help' for the available list of commands"
MSG_INPUT_PROMPT = f"Enter a command (or {MSG_HELP_AWARE_TIP})"

# Help Menu
MENU_HELP_STR = """hello                                 - Greet the user
all                                   - Display all contacts
add <name> <phone>                    - Add a new contact or add phone to the existing one
change <name> <old_phone> <new_phone> - Update contact's phone number
delete <name>                         - Delete a contact
phone <name>                          - Show contact's phone number(s)
delete-phone <name> <phone>           - Delete contact's phone number
add-birthday <name> <birthday_date>   - Add a birthday to the specified contact
show-birthday <name>                  - Show the birthday of the specified contact
delete-birthday <name>                - Delete birthday of the specified contact
birthdays                             - Show upcoming birthdays within the upcoming week
help                                  - Show available commands (this menu)
exit (or close)                       - Exit the app"""

# === CONTACT MANAGER ===

# Contacts messages and feedback
MSG_HAVE_CONTACTS = "You have {0} contact{1}"
MSG_CONTACT_ADDED = "Contact added."
MSG_CONTACT_UPDATED = "Contact updated."
MSG_CONTACT_DELETED = "Contact deleted."
MSG_PHONE_ADDED = "Phone added."
MSG_PHONE_UPDATED = "Phone updated."
MSG_PHONE_DELETED = "Phone deleted."
MSG_SHOW_NO_MATCHES = "No matches found."
MSG_SHOW_FOUND_MATCHES = "Found {0} match{1}"

MSG_BIRTHDAY_ADDED = "Birthday added."
MSG_BIRTHDAY_UPDATED = "Birthday updated."
MSG_BIRTHDAY_DELETED = "Birthday deleted."
MSG_BIRTHDAY_NO_BIRTHDAY = "No birthday found for {0}."
MSG_BIRTHDAY_UPCOMING_PERIOD_STR = "upcoming week"
MSG_BIRTHDAYS_NO_UPCOMING = "You have no birthday in {0}."
MSG_BIRTHDAYS_FOUND_MATCHES = "Found {0} birthday congratulation{1} in {2}"
MSG_BIRTHDAY_MOVED = "(moved to closest weekday from {0})"

# Error Handling Messages
ERR_KEY_ERROR = "Requested item not found."
ERR_INDEX_ERROR = "Missing or incomplete arguments."
ERR_VALUE_ERROR = "Invalid input value."
MSG_INTERRUPTED_BY_USER = "Application interrupted by user"
ERR_ARG_COUNT_ERROR = "You must provide {expected} non-empty argument{plural}{details}."
ERR_TYPE_ERROR = "Expected type '{expected}', but received type '{actual}'."

USERNAME_EMPTY_ERROR = "Username cannot be empty or just whitespace."
USERNAME_TOO_SHORT_ERROR = (
    "Username '{username}' is too short and should have at least {min_len} symbols."
)
USERNAME_TOO_LONG_ERROR = (
    "Username '{username}' is too long and should have not more than {max_len} symbols."
)
PHONE_EMPTY_ERROR = "Phone cannot be empty or just whitespace."
PHONE_INVALID_FORMAT_ERROR = (
    "Invalid phone number '{phone}'. Expected {format_description}."
)
DATE_FORMAT_INVALID_ERROR = (
    "Invalid date format '{value}'. Use {expected_format} format."
)
BIRTHDAY_IN_FUTURE_ERROR = "Given birthday date '{value}' can't be in the future."

# === MODELS ===

# Date & format constants
DATE_FORMAT = "%d.%m.%Y"
DATE_FORMAT_STR_REPRESENTATION = "DD.MM.YYYY"

# Text formatting defaults
DEFAULT_TRUNCATE_LENGTH = 8
DEFAULT_LINE_OFFSET = " " * 2
LINE_VALUE_GROUP_SEPARATION_SYMBOL = ":"
LINE_VALUE_LIST_SEPARATION_SYMBOL = ","

# === VALIDATORS ===

# Validator messages
MSG_LOAD_STORAGE_FIRST = "Book is not loaded. Call {0} first."
MSG_CONTACT_EXISTS = "Contact with username '{0}' already exists"
MSG_NO_CONTACTS = "You don't have contacts yet, but you can add one anytime."
MSG_CONTACT_NOT_FOUND = "Contact '{0}' not found"
MSG_PHONE_NUMBER_EXISTS = "Contact '{0}' has '{1}' phone number already."
MSG_PHONE_NUMBER_NOT_FOUND = "Phone number '{0}' for contact '{1}' not found."
MSG_BIRTHDAY_DUPLICATE = "Birthday for '{0}' is already set to '{1}'."

# Validation constraints
NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 50
MAX_DISPLAY_NAME_LEN = 15
PHONE_FORMAT_DESC_STR = "10 digits, optionally starting with '+'"

# === PERSISTENCE ===

# Filename to store app data
DEFAULT_FILENAME = "addressbook.pkl"

# User-facing error messages
MSG_SAVE_SUCCESS = "Contacts saved successfully."
MSG_FILE_NO_PERMISSION = (
    # "You do not have permission to access the contacts file. "
    # "Another application or process may be using it. "
    "Another application blocks this app resources. "
    "Please close other application and try again."
    # "Please close other programs and try again."
)
MSG_FILE_ERR_UNEXPECTED_ERR = "An unexpected error occurred while {0} contacts data."

# Logging templates
LOG_FILE_LOAD_SUCCESS = "Loaded address book from %s"
LOG_FILE_NO_FILE_CREATED = (
    "App data file not found. Creating fresh instance of AddressBook class"
)
LOG_FILE_SAVE_SUCCESS = "Saved address book to %s"
LOG_FILE_ERR_NO_PERMISSION = (
    "You do not have permission to access '%s' while %s contacts data"
)
LOG_FILE_ERR_IS_DIRECTORY = (
    "Expected a file, but found a directory at '%s' while %s contacts data"
)
LOG_FILE_ERR_OS_ERR = "OS error occurred while %s '%s': %s"
LOG_FILE_ERR_UNEXPECTED_ERR = "Unexpected error while %s data from '%s': %s"

# === DEPRECATION WARNING ===

# Default deprecation reason used in the transition_warning decorator
DEFAULT_TRANSITION_REASON = (
    "[TRANSITION DEBUG] This function '%s' is transitional "
    "and will be removed in a future version. %s"
)
