#!/bin/bash

# 1. Navigate to the folder where this script is located
cd "$(dirname "$0")"

# 2. Activate the virtual environment
# We check common locations for the venv folder
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Please ask IT to set it up once."
    read -p "Press any key to exit..."
    exit 1
fi

# 3. Open the browser to the app's URL (waits 2 seconds for server to warm up)
(sleep 2 && open "http://127.0.0.1:8000") &

# 4. Start the Server
echo "Starting PredictCare (BMH Hospital)..."
echo "Do not close this window while using the app."
python3 manage.py runserver
