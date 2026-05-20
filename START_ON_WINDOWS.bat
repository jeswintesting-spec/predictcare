@echo off
cd /d "%~dp0"

echo ===========================================
echo Starting PredictCare (BMH Hospital) Setup
echo ===========================================

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in the system PATH.
    echo Please install Python from python.org and try again.
    pause
    exit
)

:: 2. Check and Create Virtual Environment
if not exist ".venv\Scripts\activate.bat" (
    echo [INFO] Creating virtual environment... This might take a minute.
    python -m venv .venv
    
    echo [INFO] Activating virtual environment...
    call .venv\Scripts\activate.bat
    
    echo [INFO] Installing required dependencies...
    pip install -r requirements.txt
    
    echo [INFO] Applying database migrations...
    python manage.py migrate
) else (
    echo [INFO] Virtual environment found. Activating...
    call .venv\Scripts\activate.bat
)

:: 3. Open Browser
echo [INFO] Opening Web Browser...
start http://127.0.0.1:8000

:: 4. Run Server
echo [INFO] Starting Application Server...
python manage.py runserver

pause
