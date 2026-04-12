# Quick Start Script for RagaRasa Local Development (PowerShell)
# Run with: powershell -ExecutionPolicy Bypass -File start_local_dev.ps1

Write-Host ""
Write-Host "============================================"
Write-Host "RagaRasa Music Therapy - Local Dev Setup" -ForegroundColor Cyan
Write-Host "============================================"
Write-Host ""

# Check if Python is installed
$pythonCheck = python --version 2>$null
if (-not $pythonCheck) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node is installed
$nodeCheck = node --version 2>$null
if (-not $nodeCheck) {
    Write-Host "ERROR: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Set paths
$BACKEND_PATH = "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\Backend"
$EMOTION_PATH = "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\emotion_recognition"
$FRONTEND_PATH = "C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\raga-rasa-soul-final-v2"

# Function to start service in new PowerShell window
function Start-ServiceWindow {
    param(
        [string]$Title,
        [string]$WorkingDir,
        [string]$Command
    )
    
    $scriptBlock = {
        param($dir, $cmd)
        Set-Location $dir
        Invoke-Expression $cmd
        Read-Host "Press Enter to close this window"
    }
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$WorkingDir'; $Command" -WindowName $Title
}

Write-Host "Starting all services..." -ForegroundColor Green
Write-Host ""

# Terminal 1: Backend
Write-Host "[1/3] Starting Backend API (FastAPI)..." -ForegroundColor Cyan
Write-Host "       Port: http://localhost:8000"
Write-Host "       Docs: http://localhost:8000/docs"
Write-Host ""

$backendCmd = ". .\venv\Scripts\Activate.ps1; python main.py"
Start-ServiceWindow -Title "RagaRasa Backend" -WorkingDir $BACKEND_PATH -Command $backendCmd

# Wait for backend to start
Start-Sleep -Seconds 3

# Terminal 2: Emotion Service
Write-Host "[2/3] Starting Emotion Recognition Service (Flask)..." -ForegroundColor Cyan
Write-Host "       Port: http://localhost:5000"
Write-Host "       Health: http://localhost:5000/health"
Write-Host ""

$emotionCmd = ". .\venv\Scripts\Activate.ps1; python api.py"
Start-ServiceWindow -Title "RagaRasa Emotion" -WorkingDir $EMOTION_PATH -Command $emotionCmd

# Wait for emotion service to start
Start-Sleep -Seconds 3

# Terminal 3: Frontend
Write-Host "[3/3] Starting Frontend (React + Vite)..." -ForegroundColor Cyan
Write-Host "       Port: http://localhost:5173"
Write-Host ""

$frontendCmd = "npm run dev"
Start-ServiceWindow -Title "RagaRasa Frontend" -WorkingDir $FRONTEND_PATH -Command $frontendCmd

Write-Host ""
Write-Host "============================================"
Write-Host "All services starting in separate windows" -ForegroundColor Green
Write-Host "============================================"
Write-Host ""
Write-Host "Wait 10-15 seconds for all services to start, then:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Open http://localhost:5173 in your browser"
Write-Host "2. Check for any errors in the terminal windows"
Write-Host "3. Verify all three services are running"
Write-Host ""
Write-Host "To stop all services:" -ForegroundColor Yellow
Write-Host "   - Close each terminal window, OR"
Write-Host "   - Run: Stop-Process -Name python, node"
Write-Host ""
Write-Host "For detailed setup instructions:" -ForegroundColor Yellow
Write-Host "   - See LOCAL_DEVELOPMENT_GUIDE.md"
Write-Host ""

Read-Host "Press Enter to close this window"
