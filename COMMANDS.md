# 📋 Command Reference - Stock Market Predictor

Quick reference for all commands to run the application.

---

## 🚀 Initial Setup (One Time Only)

### Option 1: Automated Setup (Recommended)
```powershell
# PowerShell
.\setup.ps1
```

```cmd
# Command Prompt
setup.bat
```

### Option 2: Manual Setup

#### Backend Setup
```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# OR Activate (Command Prompt)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env and add your API key (use notepad or any editor)
notepad .env

# Create models directory
mkdir models
```

#### Frontend Setup
```powershell
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env
```

---

## 🏃 Running the Application

### Start Backend (Terminal 1)
```powershell
# From project root
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start server
python main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Start Frontend (Terminal 2)
```powershell
# From project root (open NEW terminal)
cd frontend

# Start development server
npm run dev
```

Expected output:
```
  VITE v5.0.8  ready in XXX ms
  ➜  Local:   http://localhost:3000/
```

### Open Browser
Navigate to: **http://localhost:3000**

---

## 🧪 Testing Commands

### Test Backend Setup
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python test_setup.py
```

### Test API Endpoints Manually
```powershell
# Get quote
curl "http://localhost:8000/quote?symbol=AAPL"

# Get prediction
curl "http://localhost:8000/predict?symbol=AAPL"

# Get signal
curl "http://localhost:8000/signal?symbol=AAPL"

# Get chart data
curl "http://localhost:8000/chart?symbol=AAPL"

# Get portfolio signal
curl "http://localhost:8000/portfolio?symbol=AAPL&type=aggressive"

# Train model
curl -X POST "http://localhost:8000/train?symbol=AAPL"
```

### View API Documentation
Open in browser: **http://localhost:8000/docs**

---

## 📦 Package Management

### Update Backend Dependencies
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
```

### Update Frontend Dependencies
```powershell
cd frontend
npm update
```

### Add New Python Package
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install package-name
pip freeze > requirements.txt
```

### Add New Node Package
```powershell
cd frontend
npm install package-name
```

---

## 🐳 Docker Commands

### Build and Run with Docker Compose
```powershell
# From project root
docker-compose up --build
```

### Build Backend Only
```powershell
cd backend
docker build -t stock-predictor-backend .
docker run -p 8000:8000 --env-file .env stock-predictor-backend
```

### Build Frontend Only
```powershell
cd frontend
docker build -t stock-predictor-frontend .
docker run -p 3000:80 stock-predictor-frontend
```

### Stop Docker Containers
```powershell
docker-compose down
```

---

## 🏗️ Build Commands

### Build Frontend for Production
```powershell
cd frontend
npm run build
```

Output directory: `frontend/dist/`

### Preview Production Build
```powershell
cd frontend
npm run preview
```

---

## 🧹 Cleanup Commands

### Clean Python Cache
```powershell
cd backend
# Remove cache files
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force .pytest_cache
Remove-Item -Force *.pyc
```

### Clean Node Modules
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Clean All Generated Files
```powershell
# From project root

# Backend cleanup
cd backend
Remove-Item -Recurse -Force __pycache__
Remove-Item -Force cache.db
Remove-Item -Recurse -Force models/*.pkl
Remove-Item -Force .env

# Frontend cleanup
cd ../frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Recurse -Force dist
Remove-Item -Force .env

# Return to root
cd ..
```

---

## 🔧 Development Commands

### Run Backend with Auto-Reload
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Frontend with Custom Port
```powershell
cd frontend
npm run dev -- --port 3001
```

### Check Python Version
```powershell
python --version
```

### Check Node Version
```powershell
node --version
npm --version
```

### List Installed Python Packages
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip list
```

### List Installed Node Packages
```powershell
cd frontend
npm list --depth=0
```

---

## 🚢 Deployment Commands

### Deploy to Railway
```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy backend
cd backend
railway up

# Deploy frontend
cd ../frontend
railway up
```

### Deploy to Render
1. Connect GitHub repository
2. Create Web Service for backend
3. Create Static Site for frontend
4. Add environment variables
5. Deploy automatically on push

---

## 🔍 Debugging Commands

### Check Backend Logs
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
# Logs will appear in terminal
```

### Check if Port is in Use
```powershell
# Check port 8000 (backend)
netstat -ano | findstr :8000

# Check port 3000 (frontend)
netstat -ano | findstr :3000
```

### Kill Process on Port
```powershell
# Find PID from netstat output
taskkill /PID <PID> /F
```

### Test Database Connection
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -c "import sqlite3; conn = sqlite3.connect('cache.db'); print('✓ Database OK')"
```

### Verify API Key
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -c "from config import settings; print(f'API Key: {settings.ALPHA_VANTAGE_API_KEY[:10]}...')"
```

---

## 📊 Database Commands

### View Cache Database
```powershell
cd backend
sqlite3 cache.db
```

SQLite commands:
```sql
-- List all tables
.tables

-- View cache contents
SELECT symbol, timestamp FROM cache;

-- Clear cache
DELETE FROM cache;

-- Exit
.quit
```

### Reset Cache
```powershell
cd backend
Remove-Item cache.db
# Cache will be recreated on next run
```

---

## 🎯 Quick Commands Summary

| Task | Command |
|------|---------|
| **Setup** | `.\setup.ps1` |
| **Start Backend** | `cd backend; .\venv\Scripts\Activate.ps1; python main.py` |
| **Start Frontend** | `cd frontend; npm run dev` |
| **Test Backend** | `cd backend; python test_setup.py` |
| **API Docs** | Open `http://localhost:8000/docs` |
| **Build Frontend** | `cd frontend; npm run build` |
| **Docker Run** | `docker-compose up --build` |
| **Clean All** | See "🧹 Cleanup Commands" section |

---

## ⌨️ Keyboard Shortcuts (in App)

- **Enter** in search box → Submit search
- **F5** → Refresh page
- **Ctrl + C** in terminal → Stop server

---

## 🆘 Emergency Reset

If everything breaks, start fresh:

```powershell
# 1. Stop all running servers (Ctrl+C in terminals)

# 2. Clean everything
cd backend
Remove-Item -Recurse -Force venv
Remove-Item -Recurse -Force __pycache__
Remove-Item -Force cache.db
Remove-Item -Force .env

cd ../frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Force .env

# 3. Run setup again
cd ..
.\setup.ps1

# 4. Add API key to backend\.env

# 5. Start fresh
```

---

## 💡 Tips

### Keep Both Terminals Open
- Terminal 1: Backend (stays running)
- Terminal 2: Frontend (stays running)

### Don't Forget to Activate venv
Backend commands require:
```powershell
.\venv\Scripts\Activate.ps1
```

You'll see `(venv)` in your prompt when activated.

### Check Logs for Errors
Both terminals show real-time logs. Watch for:
- `ERROR` messages
- `Exception` traces
- HTTP error codes (400, 500, etc.)

---

**Need more help?** Check QUICKSTART.md or README.md
