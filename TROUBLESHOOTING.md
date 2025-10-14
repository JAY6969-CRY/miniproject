# 🔧 Troubleshooting Guide

Common issues and solutions for the Stock Market Predictor.

---

## 🐍 Python/Backend Issues

### ❌ "python: command not found"
**Problem**: Python is not installed or not in PATH

**Solution**:
1. Download Python 3.8+ from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart terminal
4. Verify: `python --version`

---

### ❌ "pip: command not found"
**Problem**: pip is not installed

**Solution**:
```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

---

### ❌ "Module not found" or Import Errors
**Problem**: Dependencies not installed

**Solution**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If still failing:
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

---

### ❌ Virtual Environment Won't Activate
**Problem**: Execution policy restrictions (Windows)

**Solution**:
```powershell
# Check current policy
Get-ExecutionPolicy

# If Restricted, temporarily allow scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try activating again
.\venv\Scripts\Activate.ps1
```

---

### ❌ "Address already in use" (Port 8000)
**Problem**: Another process is using port 8000

**Solution**:
```powershell
# Find the process
netstat -ano | findstr :8000

# Kill it (replace <PID> with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
uvicorn main:app --host 0.0.0.0 --port 8001
```

---

### ❌ "Unable to open database file"
**Problem**: Database permissions or corruption

**Solution**:
```powershell
cd backend
# Delete corrupted database
Remove-Item cache.db

# Restart backend (new database will be created)
python main.py
```

---

### ❌ "API key not configured"
**Problem**: .env file missing or incorrect

**Solution**:
```powershell
cd backend

# Check if .env exists
Get-Item .env

# If not, copy from example
copy .env.example .env

# Edit and add your API key
notepad .env
```

Make sure it looks like:
```
ALPHA_VANTAGE_API_KEY=YOUR_ACTUAL_KEY_HERE
```

---

### ❌ "Rate limit exceeded"
**Problem**: Alpha Vantage free tier limits (5/min, 500/day)

**Solution**:
- Wait 1 minute and try again
- App automatically falls back to yfinance
- Consider upgrading API plan for higher limits
- Cache helps reduce API calls

---

### ❌ "Insufficient data for training"
**Problem**: Stock has less than 30 days of history

**Solution**:
- Try a different, more established stock
- Some newly listed stocks won't work
- Use stocks with at least 90 days of trading history

---

## 📦 Node.js/Frontend Issues

### ❌ "node: command not found"
**Problem**: Node.js not installed

**Solution**:
1. Download Node.js 16+ from https://nodejs.org/
2. Install LTS version
3. Restart terminal
4. Verify: `node --version` and `npm --version`

---

### ❌ "npm install" fails
**Problem**: Network issues or corrupted cache

**Solution**:
```powershell
cd frontend

# Clear npm cache
npm cache clean --force

# Delete node_modules
Remove-Item -Recurse -Force node_modules

# Delete package-lock.json
Remove-Item package-lock.json

# Try again
npm install
```

---

### ❌ "EACCES: permission denied"
**Problem**: Permission issues on Windows

**Solution**:
```powershell
# Run PowerShell as Administrator
# Or change npm prefix
npm config set prefix "$env:APPDATA\npm"
```

---

### ❌ "Port 3000 already in use"
**Problem**: Another app using port 3000

**Solution**:
```powershell
# Find and kill process
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
npm run dev -- --port 3001
```

---

### ❌ "Failed to fetch" or CORS errors
**Problem**: Backend not running or CORS misconfigured

**Solution**:
1. Make sure backend is running on port 8000
2. Check backend terminal for errors
3. Verify `http://localhost:8000` in browser shows API info
4. Check `.env` file has correct API URL

---

### ❌ Blank page or "Cannot GET /"
**Problem**: Frontend build issues

**Solution**:
```powershell
cd frontend

# Clean build
Remove-Item -Recurse -Force dist

# Rebuild
npm run build

# Or just use dev mode
npm run dev
```

---

## 🔌 Connection Issues

### ❌ "Network Error" in browser
**Problem**: Backend not reachable

**Checklist**:
- [ ] Backend is running (`cd backend; python main.py`)
- [ ] Backend shows "Uvicorn running on http://0.0.0.0:8000"
- [ ] Can access http://localhost:8000 in browser
- [ ] Frontend .env has correct `VITE_API_URL`
- [ ] No firewall blocking ports 8000 or 3000

---

### ❌ API calls returning 404
**Problem**: Wrong URL or backend not running

**Solution**:
1. Check backend is running
2. Visit http://localhost:8000/docs to see available endpoints
3. Verify symbol format (e.g., AAPL not Apple)

---

## 🎨 UI/Display Issues

### ❌ Styles not loading (plain HTML)
**Problem**: Tailwind CSS not building

**Solution**:
```powershell
cd frontend

# Check if Tailwind is in package.json
npm list tailwindcss

# If not, install
npm install -D tailwindcss autoprefixer postcss

# Restart dev server
npm run dev
```

---

### ❌ Chart not displaying
**Problem**: Chart.js not loaded

**Solution**:
```powershell
cd frontend

# Install chart dependencies
npm install chart.js react-chartjs-2

# Restart
npm run dev
```

---

### ❌ Images/icons not showing
**Problem**: Missing assets or wrong paths

**Solution**:
- Check browser console for 404 errors
- Verify file paths in components
- Clear browser cache (Ctrl+Shift+R)

---

## 💾 Data Issues

### ❌ "Symbol not found" or invalid quote
**Problem**: Wrong symbol format

**Solution**:
Use correct format for each market:
- **NSE (India)**: `RELIANCE.NS`, `TCS.NS`, `INFY.NS`
- **BSE (India)**: `RELIANCE.BO`, `TCS.BO`, `INFY.BO`
- **NASDAQ (US)**: `AAPL`, `GOOGL`, `MSFT` (no suffix)

---

### ❌ Predictions seem wrong
**Problem**: Model needs training or insufficient data

**Solution**:
1. Visit http://localhost:8000/docs
2. Use `/train?symbol=AAPL` endpoint to retrain
3. Try different stock with more trading history
4. Remember: It's educational, not production-grade!

---

## 🐳 Docker Issues

### ❌ "docker: command not found"
**Problem**: Docker not installed

**Solution**:
1. Download Docker Desktop from https://www.docker.com/
2. Install and start Docker Desktop
3. Verify: `docker --version`

---

### ❌ "Cannot connect to Docker daemon"
**Problem**: Docker Desktop not running

**Solution**:
- Start Docker Desktop application
- Wait for it to fully start (whale icon in system tray)
- Try command again

---

### ❌ "Port is already allocated"
**Problem**: Port conflict with running container

**Solution**:
```powershell
# Stop all containers
docker-compose down

# Or stop specific container
docker stop <container-id>

# Remove stopped containers
docker container prune
```

---

## 🔐 Environment Issues

### ❌ .env file not found
**Problem**: Forgot to create .env

**Solution**:
```powershell
# Backend
cd backend
copy .env.example .env

# Frontend
cd ../frontend
copy .env.example .env
```

---

### ❌ Environment variables not loading
**Problem**: Wrong file location or format

**Solution**:
1. Make sure `.env` is in the correct directory:
   - `backend/.env` for backend
   - `frontend/.env` for frontend
2. No quotes needed: `KEY=value` not `KEY="value"`
3. No spaces: `KEY=value` not `KEY = value`
4. Restart servers after editing .env

---

## 🧪 Testing Issues

### ❌ test_setup.py fails
**Problem**: Dependencies or configuration issue

**Solution**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1

# Update all packages
pip install --upgrade -r requirements.txt

# Run test again
python test_setup.py
```

---

## 🚀 Deployment Issues

### ❌ Railway deployment fails
**Problem**: Missing environment variables

**Solution**:
1. Go to Railway dashboard
2. Select your service
3. Add `ALPHA_VANTAGE_API_KEY` in Variables tab
4. Redeploy

---

### ❌ Render deployment fails
**Problem**: Build configuration

**Solution**:
- Check `render.yaml` is in backend directory
- Verify Python version in settings
- Add environment variables in Render dashboard
- Check build logs for specific errors

---

## 🆘 Nuclear Option (Complete Reset)

If nothing works, start completely fresh:

```powershell
# 1. Stop all servers (Ctrl+C in both terminals)

# 2. Delete everything
cd backend
Remove-Item -Recurse -Force venv, __pycache__, models, cache.db, .env

cd ../frontend
Remove-Item -Recurse -Force node_modules, dist, .env

# 3. Run setup again
cd ..
.\setup.ps1

# 4. Add API key to backend\.env

# 5. Start fresh
cd backend
.\venv\Scripts\Activate.ps1
python main.py

# In another terminal
cd frontend
npm run dev
```

---

## 📞 Getting More Help

### Check Logs
Always check terminal output for error messages:
- Backend: Watch the terminal running `python main.py`
- Frontend: Watch the terminal running `npm run dev`
- Browser: Open Developer Tools (F12) → Console tab

### Verify Basics
```powershell
# Check Python
python --version  # Should be 3.8+

# Check Node
node --version   # Should be 16+

# Check pip
pip --version

# Check npm
npm --version

# Test internet connection
ping google.com
```

### Read Documentation
- **README.md** - Full project guide
- **QUICKSTART.md** - Setup steps
- **COMMANDS.md** - All commands
- **TECHNICAL.md** - Architecture details

### Still Stuck?
1. Read error messages carefully
2. Google the specific error
3. Check if backend runs: `http://localhost:8000/docs`
4. Check if frontend runs: `http://localhost:3000`
5. Try the nuclear reset option above

---

## 💡 Pro Tips

### Keep Terminals Open
Don't close terminal windows while servers are running.

### Check Activation
Always activate venv before backend commands:
```powershell
.\venv\Scripts\Activate.ps1
```
You should see `(venv)` in your prompt.

### Use Correct Directory
- Backend commands: run from `backend/` directory
- Frontend commands: run from `frontend/` directory
- Setup commands: run from project root

### Watch for Typos
Common mistakes:
- `python` vs `python3`
- `.\venv\Scripts\` vs `venv\Scripts\`
- `.NS` vs `.BO` for Indian stocks

### Clear Cache
Sometimes old data causes issues:
```powershell
# Backend cache
cd backend
Remove-Item cache.db

# Browser cache
Ctrl+Shift+Delete in browser
```

---

**Still having issues? Read the error message carefully - it usually tells you exactly what's wrong!**
