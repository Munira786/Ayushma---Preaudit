@echo off
REM Ayushma AI Audit System - Startup Script

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo  Ayushma AI Pre-Audit System
echo ====================================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

echo Starting Ayushma Backend Server...
echo.

REM Start backend in a new window
start "Ayushma Backend Server" /D "%SCRIPT_DIR%" python run_backend.py

echo [OK] Backend server started
echo      Waiting for backend to initialize (3 seconds)...
timeout /t 3 /nobreak

echo.
echo Starting Ayushma Frontend...
echo.

REM Start streamlit in the same window
cd /d "%SCRIPT_DIR%"
streamlit run app.py --server.port=8501

echo.
echo Ayushma system shutting down.
pause
