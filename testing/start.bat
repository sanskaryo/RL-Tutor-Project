@echo off
REM JEE RL Tutor - Startup Script (Windows)
REM Starts both backend and frontend servers

echo.
echo ================================================
echo    JEE RL Tutor - Starting Services
echo ================================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found. Please install Node.js
    pause
    exit /b 1
)

echo.
echo [1/3] Installing Backend Dependencies...
cd backend
if not exist "requirements.txt" (
    echo [WARNING] requirements.txt not found in backend folder
) else (
    python -m pip install -q -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install backend dependencies
        pause
        exit /b 1
    )
)
cd ..

echo [2/3] Installing Frontend Dependencies...
if not exist "node_modules" (
    echo Installing npm packages (this may take a moment)...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
) else (
    echo npm packages already installed
)

echo [3/3] Starting Services...
echo.
echo Starting Backend (FastAPI on port 8002)...
cd backend
start "JEE RL Tutor - Backend" cmd /k "python -m uvicorn main:app --reload --port 8002"
cd ..
timeout /t 3 /nobreak >nul

echo Starting Frontend (Next.js on port 3000)...
start "JEE RL Tutor - Frontend" cmd /k "npm run dev"

echo.
echo ================================================
echo    Services Started Successfully!
echo ================================================
echo.
echo    Backend:  http://localhost:8002
echo    Frontend: http://localhost:3000
echo    API Docs: http://localhost:8002/docs
echo.
echo Press any key to exit this window...
echo (Services will continue running in separate windows)
pause >nul
echo ================================================
pause >nul

echo.
echo Stopping servers...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
echo Servers stopped.
