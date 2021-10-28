@echo off
echo [32mGetting newest version of pylint[0m 
python -m pip install --upgrade pylint
echo.

echo [36mRunning linter on run.py[0m
pylint run.py

echo [36mRunning linter on config.py[0m
pylint config.py

echo [36mRunning linter on app/* directory[0m
pylint app