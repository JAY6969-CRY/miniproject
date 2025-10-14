# 🤖 Gemini AI Integration - Setup Guide

## ✨ New Features Added

### 1. **Top Intraday Stocks Chart** 🔥
- Real-time scanning of high-volume, volatile stocks
- Perfect for aggressive/intraday trading
- Shows top 10 stocks by trading score
- Metrics: Price, Change, Volume, Volatility, Signal
- Click any stock to analyze instantly
- Switch between US 🇺🇸 and India 🇮🇳 markets

### 2. **Gemini AI-Powered NLP** 🧠
- Understands ANY natural language query
- No need to remember exact stock symbols
- Context-aware responses
- Intelligent intent detection
- Better than regex-based parsing

---

## 🚀 Setup Instructions

### Step 1: Get Your Gemini API Key (FREE)

1. Go to **Google AI Studio**: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy your API key (starts with `AIza...`)

### Step 2: Add API Key to Backend

1. Open `d:\miniproject\backend\.env` file
2. Add this line:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```
3. Replace `your_api_key_here` with your actual key

Example:
```bash
ALPHA_VANTAGE_API_KEY=B6285XQINCRH073P
NEWS_API_KEY=your_news_api_key
GEMINI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 3: Install Gemini Python Library

Open PowerShell in the backend directory and run:

```powershell
cd D:\miniproject\backend
pip install google-generativeai
```

### Step 4: Restart Backend Server

Stop the current backend (Ctrl+C) and restart:

```powershell
cd D:\miniproject\backend
python main.py
```

You should see:
```
✅ Gemini AI parser initialized successfully
```

---

## 🎯 How It Works

### Without Gemini (Current - Regex Parser)
```
User: "Tell me about Tesla's growth potential"
❌ Parser: Can't understand - needs exact phrases
```

### With Gemini (NEW - AI Parser)
```
User: "Tell me about Tesla's growth potential"
✅ Gemini: Understands intent, identifies TSLA, provides analysis
```

### Example Queries Gemini Can Handle:

1. **Vague Queries**:
   - "Which tech stock should I buy?"
   - "Best Indian stock for retirement?"
   - "I want quick profits, what should I trade?"

2. **Complex Questions**:
   - "Compare Apple and Microsoft for day trading"
   - "Is Tesla overvalued right now?"
   - "Should I invest $10,000 in Amazon or Google?"

3. **Natural Language**:
   - "Tell me about Reliance Industries prospects"
   - "What's happening with TCS stock?"
   - "Give me a good stock under $100"

4. **Contextual**:
   - "I have 50k rupees, which Indian stock?"
   - "Looking for dividend stocks in tech sector"
   - "High growth potential stocks for 2025"

---

## 📊 Top Stocks Feature

### How It Works:

The system scans pre-defined watchlists and calculates a **Trading Score** for each stock:

```
Trading Score = 
  Today's Movement × 30% +
  Volume Surge × 20% +
  Volatility × 30% +
  3-Day Momentum × 20%
```

### Metrics Displayed:

1. **Price**: Current trading price
2. **Change**: Today's percentage change
3. **Volume**: Trading volume in millions
4. **Volatility**: Average daily price range
5. **Signal**: BUY, SELL, STRONG BUY, etc.
6. **Score**: Overall trading suitability (0-100)

### Stock Selection Criteria:

**US Stocks**: AAPL, TSLA, NVDA, AMD, COIN, etc.
- High liquidity (>1M daily volume)
- Good volatility (1-5% daily range)
- Popular among day traders

**Indian Stocks**: RELIANCE.NS, TCS.NS, TATAMOTORS.NS, etc.
- High NSE volume
- Intraday-friendly
- Strong momentum

---

## 🎨 UI Features

### Aggressive Page Updates:

1. **Top Stocks Table** (NEW):
   - Ranking with gradient badges
   - Color-coded signals
   - Click any stock to analyze
   - Region switcher (US/India)
   - Auto-refresh capability

2. **Enhanced Search**:
   - Now uses Gemini AI automatically
   - Falls back to regex if Gemini unavailable
   - Better error handling

### Long-Term Page Updates:

1. **Gemini Integration**:
   - Same AI-powered understanding
   - Optimized for investment queries
   - Context-aware recommendations

---

## 🔧 Technical Details

### New Backend Files:

1. **`gemini_parser.py`** (240 lines):
   - GeminiNLPParser class
   - JSON response parsing
   - Fallback to regex parser
   - Stock symbol validation

2. **`top_stocks.py`** (200 lines):
   - TopStocksRecommender class
   - Real-time stock scanning
   - Metric calculations
   - Caching (1 hour)

### New Frontend Components:

1. **`TopStocksChart.jsx`** (280 lines):
   - Interactive stock table
   - Region selector
   - Click-to-analyze
   - Refresh button

### New API Endpoints:

1. **`GET /top-stocks`**:
   - Query params: `limit`, `region`
   - Returns: Top stocks with metrics
   - Cache: 1 hour

2. **`GET /analyze-gemini`**:
   - Query params: `query`, `portfolio_type`, `budget`
   - Returns: AI-powered analysis
   - Falls back to `/analyze` if Gemini unavailable

---

## 🎯 Testing the Features

### Test 1: Top Stocks Chart

1. Go to: http://localhost:3001/aggressive
2. See the "🔥 Top Intraday Stocks" table
3. Click US/India switcher
4. Click any stock's "Trade" button
5. Get instant analysis!

### Test 2: Gemini AI Parser

1. On aggressive page, type:
   ```
   "What's a volatile tech stock I can day trade?"
   ```
2. Gemini will understand and suggest stocks
3. Try:
   ```
   "Give me a high-growth Indian stock under ₹500"
   ```

### Test 3: Complex Queries

```
✅ "Compare Tesla and Rivian for short-term trading"
✅ "I have $5000, which stock has best momentum?"
✅ "Tell me about Microsoft's AI business impact on stock"
✅ "Which Indian bank stock is oversold right now?"
```

---

## 📝 Configuration Options

### Customize Watchlists:

Edit `backend/top_stocks.py`:

```python
INTRADAY_WATCHLIST = {
    'US': [
        'AAPL', 'TSLA', 'NVDA',  # Add your stocks here
    ],
    'INDIA': [
        'RELIANCE.NS', 'TCS.NS',  # Add your stocks here
    ]
}
```

### Adjust Trading Score Weights:

```python
trading_score = (
    abs(change_pct) * 0.3 +      # ← Adjust weight
    volume_surge * 0.2 +         # ← Adjust weight
    avg_volatility * 0.3 +       # ← Adjust weight
    abs(momentum) * 0.2          # ← Adjust weight
)
```

### Cache Duration:

```python
self.cache_duration = 3600  # 1 hour (in seconds)
```

---

## 🚨 Troubleshooting

### Issue 1: "Gemini API error"
**Solution**: Check your API key in `.env` file

### Issue 2: Top stocks not loading
**Solution**: 
- Check internet connection
- Some stocks might have trading halted
- Try refreshing after market hours

### Issue 3: "Module not found: google.generativeai"
**Solution**: 
```powershell
pip install google-generativeai
```

### Issue 4: Fallback to regex parser
**Solution**: 
- This is normal if Gemini is not configured
- App still works with standard NLP parser
- Set GEMINI_API_KEY to enable AI features

---

## 💰 Pricing

### Gemini API:
- **FREE Tier**: 60 requests per minute
- **Cost**: $0 for normal usage
- More info: https://ai.google.dev/pricing

### Top Stocks Feature:
- **FREE**: Uses yfinance (no API key needed)
- Real-time data from Yahoo Finance

---

## 🎉 What You Get

### Before:
- ❌ Limited stock symbol recognition
- ❌ Rigid query patterns
- ❌ No stock discovery
- ❌ Manual stock selection

### After:
- ✅ Understands ANY query
- ✅ Context-aware AI
- ✅ Top stocks automatically identified
- ✅ Click-to-analyze from chart
- ✅ US + India markets
- ✅ Real-time volatility tracking

---

## 📚 Example Use Cases

### Day Trader Workflow:
1. Open aggressive page
2. Check top stocks chart
3. See TSLA has high score (volatility + volume)
4. Click "Trade" button
5. Add budget: $5000
6. Get position size, entry/exit prices
7. Execute trade!

### AI Query Workflow:
1. Ask: "Which stock will give me 5% in 2 days?"
2. Gemini identifies volatile stocks
3. Analyzes NVDA (high momentum)
4. Provides trading plan
5. Shows stop loss and target
6. Ready to trade!

---

**Your stock predictor now has AI superpowers! 🤖🚀**

*No more rigid patterns - just ask naturally and get intelligent answers!*
