@echo off
:: Activate virtual environment (optional, if you're using one)
:: If you have a virtual environment, adjust the path accordingly
:: call venv\Scripts\activate

:: Run the Python script with any passed arguments, or without arguments if none are provided
python src\main.py %*
