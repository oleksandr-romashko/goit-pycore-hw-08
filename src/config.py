"""
Configuration module for the application.

This module loads environment variables from a `.env` file (if present) using `python-dotenv`
and exposes configuration settings such as DEBUG mode for use throughout the application.

Attributes:
    DEBUG (bool): Indicates whether the application is running in debug mode.
                  Set via the DEBUG variable in the .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
