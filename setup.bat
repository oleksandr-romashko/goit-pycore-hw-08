@echo off

:: Step 1: Create a virtual environment if not already created
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo ⚠️ Virtual environment already exists.
)

:: Step 2: Activate the virtual environment
echo Activating the virtual environment...
call .\.venv\Scripts\activate.bat

:: Step 3: Install required packages from requirements.txt (if it exists)
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo ❌ No requirements.txt found.
)

:: Step 4: Install the git hook scripts for pre-commit
echo Setting up pre-commit hook for git...
pre-commit install
if %ERRORLEVEL% equ 0 (
    echo ✅ pre-commit hook set up successfully.
) else (
    echo ❌ Failed to set up pre-commit hook. Is 'pre-commit' installed and on PATH?
)
