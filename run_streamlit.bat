@echo off
echo.
echo 🌾 Smart Farming AI - Streamlit Deployment
echo ===========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo Install from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% detected
echo.

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements_streamlit.txt

echo.
echo ✅ Setup complete!
echo.

REM Check backend
echo 🔍 Checking backend API...
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is running at http://localhost:5000
) else (
    echo ⚠️  Backend is NOT running at http://localhost:5000
    echo    Make sure to start the backend first:
    echo    cd backend ^&^& npm start
)

echo.
echo 🚀 Starting Streamlit app...
echo 📱 Your app will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start Streamlit
streamlit run streamlit_app.py --server.port=8501 --server.address=localhost

pause
