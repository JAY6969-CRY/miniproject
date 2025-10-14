# Natural Language Investment Advisor - Feature Documentation

## Overview
The Stock Predictor now supports **natural language queries**! Instead of just typing stock symbols, you can ask questions in plain English like a conversation with a financial advisor.

## 🎯 What's New?

### Natural Language Understanding
Ask questions naturally:
- ✅ "Can I invest in Apple today?"
- ✅ "Should I buy Tesla stock?"
- ✅ "Is Reliance a good investment?"
- ✅ "How many TCS shares should I buy?"
- ✅ "Is Microsoft worth buying?"

### Intelligent Analysis Components

#### 1. **NLP Query Parser** (`nlp_parser.py`)
- Extracts stock symbols from company names
- Supports 80+ popular stocks (US & Indian markets)
- Detects user intent (buy/sell/hold/analyze)
- Extracts quantity if mentioned
- Examples:
  - "invest in apple" → AAPL
  - "buy reliance" → RELIANCE.NS
  - "buy 10 shares of TCS" → TCS.NS, quantity: 10

#### 2. **News & Sentiment Analyzer** (`news_analyzer.py`)
- Fetches recent news from NewsAPI (optional)
- Analyzes sentiment using TextBlob
- Provides overall sentiment score
- Shows positive/negative/neutral article counts
- Falls back to mock news if API key not provided

#### 3. **Intelligent Advisor** (`advisor.py`)
- Combines technical analysis + news sentiment
- Generates comprehensive recommendations
- Identifies growth factors
- Highlights risk factors
- Calculates investment metrics
- Provides human-readable reasoning

## 📊 Analysis Output

### What You Get:
1. **Recommendation**: STRONG BUY / BUY / HOLD / SELL / STRONG SELL
2. **Confidence Score**: 0.0 to 1.0 with label (VERY HIGH to VERY LOW)
3. **Technical Score**: Based on ML predictions and indicators
4. **Sentiment Score**: Based on recent news analysis
5. **Growth Factors**: What's making the stock grow
   - Technical buy signals
   - Predicted price increases
   - Positive news sentiment
   - RSI indicators
6. **Risk Factors**: Potential concerns
   - Technical sell signals
   - High volatility
   - Negative news
7. **News Summary**: Recent headlines with sentiment
8. **Investment Metrics** (if quantity specified):
   - Total investment amount
   - Predicted value
   - Expected profit/loss
   - Return percentage

## 🚀 How to Use

### Frontend (User Interface)

**Option 1: Natural Language**
```
Type: "Can I invest in Apple today?"
Result: Comprehensive analysis with reasoning
```

**Option 2: Traditional Symbol**
```
Type: "AAPL"
Result: Traditional price prediction view
```

**Option 3: Use Quick Try Buttons**
Click pre-filled example queries in the search bar

### Backend API

**New Endpoint: `/analyze`**

```bash
# Natural language query
GET /analyze?query=Can%20I%20invest%20in%20Apple%20today&portfolio_type=balanced

# Response structure
{
  "success": true,
  "symbol": "AAPL",
  "company_name": "Apple",
  "parsed_query": {
    "original": "Can I invest in Apple today",
    "detected_symbol": "AAPL",
    "detected_company": "Apple",
    "detected_intent": "buy",
    "confidence": 0.85
  },
  "quote": { /* current price data */ },
  "prediction": { /* price prediction */ },
  "signal": { /* trading signal */ },
  "news_sentiment": {
    "label": "positive",
    "score": 0.45,
    "emoji": "📈",
    "article_count": 5,
    "positive_count": 3,
    "negative_count": 1,
    "neutral_count": 1
  },
  "news_articles": [ /* top 3 articles */ ],
  "analysis": {
    "recommendation": "BUY",
    "confidence": "HIGH",
    "confidence_score": 0.72,
    "technical_score": 0.75,
    "sentiment_score": 0.65,
    "growth_factors": [
      "📊 Technical indicators show BUY signal",
      "📈 Predicted price increase of 2.5%",
      "📰 Positive news sentiment (3 positive articles)"
    ],
    "risk_factors": [
      "✅ No major risk factors identified"
    ],
    "reasoning": "✅ This stock shows positive signals...",
    "should_invest": true,
    "portfolio_alignment": "Fits balanced portfolio approach"
  }
}
```

## 🎨 Frontend Components

### New Component: `AnalysisCard.jsx`
Displays comprehensive analysis with:
- Query understanding section
- Recommendation card with confidence
- Current price information
- Investment calculator (if quantity specified)
- Score breakdowns (technical + sentiment)
- Growth factors list
- Risk factors list
- News sentiment summary
- Recent headlines with sentiment indicators
- Portfolio alignment message

### Updated Component: `SearchBar.jsx`
- Enhanced placeholder text
- Example query buttons
- Better UX for natural language input
- Visual loading state

### Updated Component: `App.jsx`
- Auto-detects natural language vs symbol
- Switches between "simple" and "advanced" view modes
- Handles both query types seamlessly

## 📦 Dependencies

### New Python Packages:
```txt
textblob>=0.17.1          # Sentiment analysis
newsapi-python>=0.2.7     # News fetching (optional)
```

### Installation:
```bash
cd backend
pip install -r requirements.txt
```

## 🔧 Configuration

### Environment Variables (`.env`):
```bash
# Required
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key

# Optional - for real news data
NEWS_API_KEY=your_newsapi_key
# Get from: https://newsapi.org/register
# If not provided, mock news will be used
```

## 🧪 Testing

### Test Queries:

**US Stocks:**
```
Can I invest in Apple today?
Should I buy Tesla stock?
Is Microsoft worth it?
Buy 5 shares of Google
What about Amazon?
```

**Indian Stocks:**
```
Should I invest in Reliance?
Is TCS a good buy?
Can I buy HDFC Bank stock?
Is Infosys worth buying?
Buy 10 shares of Wipro
```

**Different Intents:**
```
Should I sell my Apple stocks?
Can I hold Reliance?
Is Tesla a bad investment?
```

### Test via API:
```bash
# PowerShell
curl "http://localhost:8000/analyze?query=can%20i%20invest%20in%20apple%20today"

# Browser
http://localhost:8000/analyze?query=can i invest in apple today
```

## 🎯 Scoring Algorithm

### Overall Confidence Score:
```python
confidence_score = (technical_score * 0.6) + (sentiment_score * 0.4)
```

**Technical Score (60% weight):**
- Base signal (BUY=0.8, HOLD=0.5, SELL=0.2)
- Confidence multiplier (HIGH=1.0, MEDIUM=0.85, LOW=0.7)
- Price change adjustment (±20% max)

**Sentiment Score (40% weight):**
- News sentiment polarity (-1 to +1)
- Normalized to 0-1 scale

### Recommendation Thresholds:
- **STRONG BUY**: Score ≥ 0.70
- **BUY**: Score ≥ 0.55
- **HOLD**: Score 0.45-0.54
- **SELL**: Score 0.30-0.44
- **STRONG SELL**: Score < 0.30

## 🌟 Example Use Cases

### Use Case 1: Quick Investment Check
**Query:** "Can I invest in Apple today?"
**Result:** Instant analysis with buy/hold/sell recommendation

### Use Case 2: Quantity Planning
**Query:** "Should I buy 100 shares of Tesla?"
**Result:** Full analysis + investment calculator showing total cost and expected P&L

### Use Case 3: News-Driven Decision
**Query:** "Is Reliance a good investment?"
**Result:** Technical + news sentiment analysis to make informed decision

### Use Case 4: Risk Assessment
**Query:** "Should I sell my Microsoft stocks?"
**Result:** Identifies current risks and growth factors

## 🔮 Future Enhancements

Potential improvements:
1. More advanced NLP using spaCy or transformers
2. Multi-stock comparison ("Apple vs Microsoft")
3. Time-based queries ("Is Apple good for long-term?")
4. Portfolio analysis ("Analyze my portfolio: AAPL, TSLA, GOOGL")
5. Real-time news streaming
6. Sentiment from social media (Twitter, Reddit)
7. Voice input support
8. Multi-language support (Hindi, Spanish, etc.)

## 📚 Code Architecture

```
backend/
├── nlp_parser.py       # Query understanding & symbol extraction
├── news_analyzer.py    # News fetching & sentiment analysis
├── advisor.py          # Comprehensive analysis & recommendations
└── main.py             # New /analyze endpoint

frontend/
├── src/
│   ├── components/
│   │   ├── AnalysisCard.jsx   # New comprehensive results UI
│   │   └── SearchBar.jsx      # Enhanced with NL support
│   ├── App.jsx                # View mode switching
│   └── api.js                 # New analyzeQuery function
```

## 🐛 Troubleshooting

### Issue: "Could not understand the query"
**Solution:** Make sure to mention a stock name or symbol
**Example:** ✅ "invest in Apple" ❌ "invest in stocks"

### Issue: Mock news showing instead of real news
**Solution:** Add NEWS_API_KEY to your .env file
**Get key from:** https://newsapi.org/register

### Issue: Sentiment shows neutral for everything
**Solution:** TextBlob may need more context. This is normal for short headlines.

## 📝 Notes

- News API has rate limits (100 requests/day on free tier)
- Mock news is automatically used if NEWS_API_KEY is not set
- TextBlob sentiment analysis is lightweight and fast
- Stock symbol mapping includes 80+ popular stocks
- Unknown company names will return an error with suggestions

## 🎉 Success Metrics

After implementing this feature:
- ✅ Users can ask questions in natural language
- ✅ Get comprehensive analysis combining 3 data sources
- ✅ See growth and risk factors clearly
- ✅ Make informed investment decisions
- ✅ Understand reasoning behind recommendations
- ✅ Calculate investment returns before buying

---

**Built with:** FastAPI, TextBlob, NewsAPI, React, and ❤️
