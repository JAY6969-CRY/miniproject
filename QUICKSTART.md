# 🚀 Quick Start Guide

## Get Up and Running in 5 Minutes

### Step 1: Get Your API Key (30 seconds)
Visit https://www.alphavantage.co/support/#api-key and get a free API key.

### Step 2: Run Setup Script (2 minutes)

**Option A - PowerShell (Recommended for Windows):**
```powershell
.\setup.ps1
```

**Option B - Command Prompt:**
```cmd
setup.bat
```

**Option C - Manual Setup:**
See detailed instructions in README.md

### Step 3: Add Your API Key (30 seconds)
1. Open `backend\.env` in a text editor
2. Replace `your_alpha_vantage_api_key_here` with your actual API key
3. Save the file

### Step 4: Start Backend (1 minute)
Open a terminal and run:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Start Frontend (1 minute)
Open a **NEW** terminal and run:
```powershell
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:3000/
```

### Step 6: Use the App! 🎉
1. Open http://localhost:3000 in your browser
2. Try searching for: **AAPL** (Apple stock)
3. See the magic happen! ✨

## 💡 Example Stock Symbols

### 🇮🇳 Indian Stocks (NSE/BSE)
- **RELIANCE.NS** - Reliance Industries (NSE)
- **TCS.NS** - Tata Consultancy Services (NSE)
- **INFY.NS** - Infosys (NSE)
- **RELIANCE.BO** - Reliance Industries (BSE)

### 🇺🇸 US Stocks (NASDAQ)
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet (Google)
- **MSFT** - Microsoft
- **TSLA** - Tesla
- **NVDA** - NVIDIA

## 🎯 Portfolio Types

Try different strategies:
- **Aggressive**: Short-term trades (1% threshold)
- **Balanced**: Medium-term holds (2% threshold) - Default
- **Long Term**: Long-term investments (3% threshold)

## 🔥 Features to Try

1. **Search** for any stock symbol
2. **View** current price vs predicted price
3. **Check** buy/sell/hold recommendation
4. **Analyze** the interactive price chart
5. **Switch** between portfolio strategies
6. **Read** the reasoning behind each signal

## ⚠️ Troubleshooting

### Backend won't start?
- Make sure you activated the virtual environment
- Check if Python 3.8+ is installed: `python --version`
- Verify dependencies installed: `pip list`

### Frontend won't start?
- Check if Node.js 16+ is installed: `node --version`
- Try deleting `node_modules` and run `npm install` again

### "Unable to fetch quote" error?
- Verify your API key is correct in `backend\.env`
- Check if the stock symbol is valid
- Alpha Vantage free tier has rate limits (5 calls/minute, 500 calls/day)

### API Rate Limits?
The app uses yfinance as a fallback when Alpha Vantage limits are reached!

## 📚 What's Next?

- Read the full [README.md](README.md) for deployment options
- Explore the API at http://localhost:8000/docs
- Customize the frontend styling in `frontend/src/index.css`
- Train models for your favorite stocks using the `/train` endpoint

## 🤝 Need Help?

Check out the detailed README.md or open an issue on GitHub!

---

**Remember**: This is for educational purposes only. Not financial advice!
