@echo off
echo Starting AI Voice Detection API...
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

if not exist "models\classifier.pkl" (
    echo Error: Model not found!
    echo Please run: python scripts\train_model.py
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
