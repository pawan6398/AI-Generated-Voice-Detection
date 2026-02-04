#!/bin/bash

echo "Starting AI Voice Detection API..."
echo ""

cd "$(dirname "$0")"

if [ ! -f "venv/bin/python" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python -m venv venv"
    exit 1
fi

if [ ! -f "models/classifier.pkl" ]; then
    echo "Error: Model not found!"
    echo "Please run: python scripts/train_model.py"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
