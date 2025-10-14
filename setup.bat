@echo off
echo ================================
echo Stock Market Predictor - Setup
echo ================================
echo.

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    exit /b 1
)

echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 16+
    exit /b 1
)

echo.
echo Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo [WARNING] Please edit backend\.env and add your Alpha Vantage API key
)

echo Creating models directory...
if not exist models mkdir models

cd ..

echo.
echo Setting up Frontend...
cd frontend

echo Installing dependencies...
call npm install

echo Creating .env file...
if not exist .env (
    copy .env.example .env
)

cd ..

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next Steps:
echo 1. Get API key from: https://www.alphavantage.co/support/#api-key
echo 2. Edit backend\.env and add your API key
echo 3. Run in two separate terminals:
echo    Terminal 1: cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo    Terminal 2: cd frontend ^&^& npm run dev
echo 4. Open http://localhost:3000
echo.
pause
