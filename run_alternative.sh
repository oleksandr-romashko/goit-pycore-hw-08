#!/bin/bash
# Activate virtual environment (optional, if you're using one)
# If you have a virtual environment, adjust the path accordingly
# source venv/bin/activate

# Run the Python script with any passed arguments, or without arguments if none are provided
python3 src/main.py "$@" "--alternative"
