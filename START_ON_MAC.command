#!/bin/bash

# 1. Navigate to the folder where this script is located
cd "$(dirname "$0")"

echo "==========================================="
echo "Starting PredictCare (BMH Hospital) Setup"
echo "==========================================="

# 2. Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in the system PATH."
    echo "Please install Python from python.org and try again."
    read -p "Press any key to exit..."
    exit 1
fi

# 3. Check and Create Virtual Environment
if [ ! -d ".venv" ]; then
    echo "[INFO] Creating virtual environment... This might take a minute."
    python3 -m venv .venv
    
    echo "[INFO] Activating virtual environment..."
    source .venv/bin/activate
    
    echo "[INFO] Installing required dependencies..."
    pip install -r requirements.txt
    
    echo "[INFO] Applying database migrations..."
    python manage.py migrate
else
    echo "[INFO] Virtual environment found. Activating..."
    source .venv/bin/activate
fi

# 4. Open the browser to the app's URL (waits 2 seconds for server to warm up)
(sleep 2 && open "http://127.0.0.1:8000") &

# 5. Start the Server
echo "[INFO] Starting Application Server..."
python manage.py runserver
