@echo off
REM Smart Farming Ecosystem - Windows Startup Script
REM This script sets up and starts all services

echo.
echo ========================================
echo 🌾 Smart Farming Ecosystem Startup
echo ========================================
echo.

REM Check if Docker is installed
echo Checking for Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Docker is not installed or not in PATH
    echo Please install Docker Desktop from: https://www.docker.com/
    exit /b 1
)

echo ✓ Docker found
echo.

REM Navigate to script directory
cd /d "%~dp0"

REM Create environment files
echo Setting up environment files...
if not exist "backend\.env" (
    echo Creating backend\.env
    copy backend\.env.example backend\.env
    echo ✓ Created backend\.env
) else (
    echo ✓ backend\.env already exists
)

if not exist "frontend\.env" (
    echo Creating frontend\.env
    copy frontend\.env.example frontend\.env
    echo ✓ Created frontend\.env
) else (
    echo ✓ frontend\.env already exists
)

REM Start services
echo.
echo Starting all services...
echo This may take 1-2 minutes on first run...
echo.

cd docker
docker-compose up -d

echo.
echo ========================================
echo 🚀 Smart Farming is Starting Up!
echo ========================================
echo.
echo Access the application:
echo   🌐 Frontend:    http://localhost:3000
echo   🔌 Backend API: http://localhost:5000
echo   📚 API Docs:    http://localhost:5000/api
echo.
echo Useful Commands:
echo   View logs:      docker-compose logs -f
echo   Stop services:  docker-compose down
echo   Stop and clean: docker-compose down -v
echo.
echo ⏳ Services may take 30-60 seconds to fully start
echo    If you see errors, wait a moment and refresh
echo.
echo ========================================
echo Happy Farming! 🌾👨‍🌾👩‍🌾
echo ========================================
echo.

pause
