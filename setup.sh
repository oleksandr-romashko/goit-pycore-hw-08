#!/bin/bash

# Step 1: Create a virtual environment if not already created
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
else
  echo "⚠️ Virtual environment already exists."
fi

# Step 2: Activate the virtual environment
if [ -f ".venv/bin/activate" ]; then
  echo "Activating the virtual environment..."
  source ./.venv/bin/activate
else
  echo "❌ Virtual environment activation failed. Please check the environment setup."
  exit 1
fi

# Step 3: Install required packages from requirements.txt (if it exists)
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip3 install -r requirements.txt
else
  echo "❌ No requirements.txt found."
fi

# Step 4: Install the git hook scripts for pre-commit
echo "Setting up pre-commit hook for git..."
if pre-commit install; then
  echo "✅ pre-commit hook set up successfully."
else
  echo "❌ Failed to set up pre-commit hook. Is 'pre-commit' installed?"
fi
