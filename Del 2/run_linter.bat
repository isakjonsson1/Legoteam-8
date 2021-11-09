@echo off
echo [32mGetting newest version of pylint[0m 
python -m pip install --upgrade pylint
echo.

echo [36mRunning linter on run.py[0m
pylint main.py

echo [36mRunning linter on robot/* directory[0m
pylint robot

echo [36mRunning linter on app/* directory[0m
pylint app