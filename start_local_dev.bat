@echo off
REM Quick Start Script for RagaRasa Local Development
REM This script starts all three services in separate windows

echo.
echo ============================================
echo RagaRasa Music Therapy - Local Dev Setup
echo ============================================
echo.
echo Starting all services...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Set paths
set BACKEND_PATH="C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\Backend"
set EMOTION_PATH="C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\emotion_recognition"
set FRONTEND_PATH="C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\raga-rasa-soul-final-v2"

REM Terminal 1: Backend
echo.
echo [1/3] Starting Backend API (FastAPI)...
echo        Port: http://localhost:8000
echo        Docs: http://localhost:8000/docs
start "RagaRasa Backend" cmd /k "cd /d %BACKEND_PATH% && call venv\Scripts\activate.bat && python main.py"

REM Wait a moment
timeout /t 2 /nobreak

REM Terminal 2: Emotion Service
echo.
echo [2/3] Starting Emotion Recognition Service (Flask)...
echo        Port: http://localhost:5000
echo        Health: http://localhost:5000/health
start "RagaRasa Emotion" cmd /k "cd /d %EMOTION_PATH% && call venv\Scripts\activate.bat && python api.py"

REM Wait a moment
timeout /t 2 /nobreak

REM Terminal 3: Frontend
echo.
echo [3/3] Starting Frontend (React + Vite)...
echo        Port: http://localhost:5173
start "RagaRasa Frontend" cmd /k "cd /d %FRONTEND_PATH% && npm run dev"

echo.
echo ============================================
echo All services starting in separate windows
echo ============================================
echo.
echo Wait 10-15 seconds for all services to start, then:
echo.
echo 1. Open http://localhost:5173 in your browser
echo 2. Check for any errors in the terminal windows
echo 3. Verify all three services are running
echo.
echo To stop all services:
echo   - Close each terminal window, OR
echo   - Run: taskkill /F /IM python.exe /IM node.exe
echo.
echo For detailed setup instructions:
echo   - See LOCAL_DEVELOPMENT_GUIDE.md
echo.
pause
