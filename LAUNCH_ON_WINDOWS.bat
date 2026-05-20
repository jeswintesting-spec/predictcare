@echo off
cd /d "%~dp0"

:: 1. Activate Environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found.
    pause
    exit
)

:: 2. Open Browser
start http://127.0.0.1:8000

:: 3. Run Server
echo Starting PredictCare (BMH Hospital)...
python manage.py runserver
pause
