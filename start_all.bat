@echo off
echo =========================================
echo 🚀 Starting AI Music Player System
echo =========================================

REM -----------------------------------------
REM 🔐 FIX: ALLOW SCRIPT EXECUTION (PowerShell)
REM -----------------------------------------
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope Process -Force"

REM -----------------------------------------
REM 1️⃣ START EMOTION MODEL (FLASK)
REM -----------------------------------------
start "Emotion API" cmd /k ^
"cd /d C:\projects\emotion_recognition && ^
call venv\Scripts\activate && ^
python api.py"

REM -----------------------------------------
REM 2️⃣ START BACKEND (FASTAPI)
REM -----------------------------------------
start "Backend API" cmd /k ^
"cd /d C:\Users\rishi\OneDrive\Desktop\AI MUSIC PLAYER\backend && ^
call venv\Scripts\activate && ^
uvicorn app.main:app --reload"

REM -----------------------------------------
REM 3️⃣ START FRONTEND (REACT)
REM -----------------------------------------
start "Frontend" cmd /k ^
"cd /d C:\Users\rishi\OneDrive\Desktop\AI MUSIC PLAYER\frontend && ^
npm start"

echo =========================================
echo ✅ All services started successfully
echo =========================================
pause