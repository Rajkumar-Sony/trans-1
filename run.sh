#!/bin/bash
# Excel Translator App - Run Script

echo "Starting Excel Translator App..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
    if [ $? -ne 0 ]; then
        echo "Setup failed. Please check the errors above."
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
python3 -c "import PyQt6, openpyxl, deepl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Dependencies not found. Installing..."
    pip install -r requirements.txt
fi

# Run the application
echo "Launching Excel Translator App..."
python3 main.py
