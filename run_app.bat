@echo off
echo 🚀 Starting Audiobook AI Agent...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import streamlit, fitz, dotenv, pydub, requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Some dependencies are missing
    echo Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found
    echo Please create .env file from env_template.txt and add your Murf API key
    echo.
)

REM Start the application
echo 🌐 Launching Streamlit application...
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
streamlit run main.py

pause 