# Stock Market Predictor - Quick Setup Script
# Run this in PowerShell to set up the entire project

Write-Host "🚀 Setting up Stock Market Predictor..." -ForegroundColor Green

# Check Python
Write-Host "`n📦 Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3") {
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python 3.8+ is required. Please install from python.org" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "`n📦 Checking Node.js installation..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($nodeVersion -match "v") {
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js 16+ is required. Please install from nodejs.org" -ForegroundColor Red
    exit 1
}

# Setup Backend
Write-Host "`n🔧 Setting up Backend..." -ForegroundColor Cyan
Set-Location backend

Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Creating .env file..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "⚠ Please edit backend\.env and add your Alpha Vantage API key" -ForegroundColor Yellow
}

Write-Host "Creating models directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path models | Out-Null

Set-Location ..

# Setup Frontend
Write-Host "`n🎨 Setting up Frontend..." -ForegroundColor Cyan
Set-Location frontend

Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

Write-Host "Creating .env file..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}

Set-Location ..

# Final instructions
Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host "`n📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Get a free API key from: https://www.alphavantage.co/support/#api-key" -ForegroundColor White
Write-Host "2. Edit backend\.env and add your API key" -ForegroundColor White
Write-Host "3. Open TWO terminal windows:" -ForegroundColor White
Write-Host "   Terminal 1 (Backend):" -ForegroundColor Yellow
Write-Host "     cd backend" -ForegroundColor Gray
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "     python main.py" -ForegroundColor Gray
Write-Host "   Terminal 2 (Frontend):" -ForegroundColor Yellow
Write-Host "     cd frontend" -ForegroundColor Gray
Write-Host "     npm run dev" -ForegroundColor Gray
Write-Host "`n4. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "`n🎯 Try these example symbols:" -ForegroundColor Cyan
Write-Host "   NSE: RELIANCE.NS, TCS.NS, INFY.NS" -ForegroundColor Gray
Write-Host "   BSE: RELIANCE.BO, TCS.BO" -ForegroundColor Gray
Write-Host "   NASDAQ: AAPL, GOOGL, MSFT" -ForegroundColor Gray
