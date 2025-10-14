# 📊 Stock Market Predictor - Technical Documentation

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌─────────────┬──────────────┬─────────────┬─────────────┐ │
│  │ SearchBar   │  PriceCard   │ SignalCard  │ StockChart  │ │
│  └─────────────┴──────────────┴─────────────┴─────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         │
┌────────────────────────┴────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints                                       │   │
│  │  /quote │ /predict │ /signal │ /chart │ /portfolio  │   │
│  └────┬────────────┬─────────────┬────────────┬─────────┘   │
│       │            │             │            │              │
│  ┌────▼────┐  ┌────▼─────┐  ┌───▼──────┐ ┌───▼──────┐      │
│  │  Data   │  │  Model   │  │Predictor │ │  Cache   │      │
│  │ Fetcher │  │ Trainer  │  │          │ │ (SQLite) │      │
│  └────┬────┘  └────┬─────┘  └───┬──────┘ └──────────┘      │
└───────┼────────────┼────────────┼─────────────────────────┐
        │            │            │                           │
   ┌────▼────┐  ┌────▼─────┐ ┌───▼──────┐                   │
   │ Alpha   │  │  Pickle  │ │ yfinance │                   │
   │Vantage  │  │  Models  │ │          │                   │
   └─────────┘  └──────────┘ └──────────┘                   │
```

## Backend Components

### 1. main.py - FastAPI Application
**Purpose**: Core API server with REST endpoints

**Endpoints**:
- `GET /` - Health check and API documentation
- `GET /quote?symbol=X` - Current stock price
- `GET /predict?symbol=X` - Next-day price prediction
- `GET /signal?symbol=X` - Buy/sell/hold recommendation
- `GET /chart?symbol=X` - Historical + prediction data
- `GET /portfolio?symbol=X&type=Y` - Portfolio-adjusted signal
- `POST /train?symbol=X` - Train/retrain model

**Technologies**: FastAPI, Uvicorn, CORS middleware

### 2. data_fetcher.py - Data Retrieval Layer
**Purpose**: Fetch and cache stock data from multiple sources

**Features**:
- **Primary Source**: Alpha Vantage API
- **Fallback**: yfinance library
- **Caching**: SQLite database (15 min for quotes, 24h for historical)
- **Rate Limiting**: Automatic fallback when API limits reached

**Key Methods**:
- `get_quote(symbol)` - Real-time quote
- `get_historical_data(symbol, days)` - Historical OHLCV data
- `_get_cached_data()` / `_save_to_cache()` - Cache management

### 3. model_trainer.py - ML Pipeline
**Purpose**: Feature engineering and model training

**Features Engineered**:
1. **SMA (5)** - 5-day Simple Moving Average
2. **SMA (10)** - 10-day Simple Moving Average
3. **RSI (14)** - 14-day Relative Strength Index
4. **Current Close** - Latest closing price

**Model**: LinearRegression (scikit-learn)
- **Training Data**: 90 days historical
- **Train/Val Split**: 80/20
- **Feature Scaling**: StandardScaler
- **Persistence**: Pickle files in `./models/`

**Key Methods**:
- `calculate_sma(prices, window)` - Moving average
- `calculate_rsi(prices, period)` - RSI indicator
- `prepare_features()` - Feature matrix creation
- `train_model()` - Model training pipeline
- `load_model()` - Load saved model

### 4. predictor.py - Prediction Engine
**Purpose**: Generate predictions and trading signals

**Prediction Logic**:
1. Load/train model for symbol
2. Calculate technical indicators
3. Scale features
4. Predict next-day price
5. Generate trading signal

**Signal Generation**:
```python
if predicted_change >= threshold:
    signal = "BUY"
elif predicted_change <= -threshold:
    signal = "SELL"
else:
    signal = "HOLD"
```

**Portfolio Thresholds**:
- Aggressive: ±1%
- Balanced: ±2% (default)
- Long Term: ±3%

**Key Methods**:
- `predict_next_day()` - Price forecast
- `generate_signal()` - Trading recommendation
- `get_chart_data()` - Visualization data

### 5. config.py - Configuration Management
**Purpose**: Centralized settings using Pydantic

**Settings**:
- `ALPHA_VANTAGE_API_KEY` - API authentication
- `CACHE_DB_PATH` - SQLite database path
- `MODEL_DIR` - Model storage directory

## Frontend Components

### 1. App.jsx - Main Application
**Purpose**: Application state and orchestration

**State Management**:
- `symbol` - Current stock symbol
- `loading` - Loading indicator
- `error` - Error messages
- `portfolioType` - Strategy selection
- `quoteData`, `predictionData`, `signalData`, `chartData` - API responses

**Key Functions**:
- `handleSearch()` - Fetch all data in parallel
- `handlePortfolioTypeChange()` - Update strategy

### 2. SearchBar.jsx
**Purpose**: Stock symbol input

**Features**:
- Auto-uppercase input
- Submit on Enter key
- Loading state disabled input
- Example hints

### 3. PriceCard.jsx
**Purpose**: Display current and predicted prices

**Features**:
- Price with 2 decimal precision
- Change % with color coding (green/red)
- Volume and last update info
- Special styling for predictions

### 4. SignalCard.jsx
**Purpose**: Trading recommendation display

**Features**:
- Signal icon (📈/📉/⏸️)
- Color-coded backgrounds (green/red/yellow)
- Confidence badge (HIGH/MEDIUM/LOW)
- Reasoning explanation
- Timing recommendation
- Technical indicators display

### 5. StockChart.jsx
**Purpose**: Interactive price visualization

**Technologies**: Chart.js + react-chartjs-2

**Features**:
- Historical price line (solid blue)
- Prediction line (dashed green)
- Hover tooltips
- Responsive design
- Auto-scaling Y-axis
- Date formatting on X-axis

### 6. Footer.jsx
**Purpose**: Legal disclaimer and information

**Sections**:
- About section
- Features list
- Data sources
- Important disclaimer
- Copyright notice

## Data Flow

### Quote Request Flow
```
User Input → SearchBar → App.handleSearch() → api.getQuote()
    ↓
FastAPI /quote → DataFetcher.get_quote()
    ↓
Check Cache → [Hit: Return] [Miss: ↓]
    ↓
Try Alpha Vantage → [Success: Cache & Return]
    ↓
Try yfinance → [Success: Cache & Return]
    ↓
Error Response
```

### Prediction Flow
```
User Input → App.handleSearch() → api.getPrediction()
    ↓
FastAPI /predict → Predictor.predict_next_day()
    ↓
[Model Exists?] → [No: Train Model] → [Yes: ↓]
    ↓
Load Model & Scaler
    ↓
Fetch Recent Data → Calculate Features → Scale → Predict
    ↓
Return Prediction
```

### Signal Generation Flow
```
Prediction → Predictor.generate_signal()
    ↓
Compare predicted vs current price
    ↓
Apply portfolio threshold
    ↓
Check RSI for confirmation
    ↓
Generate signal + reasoning + timing
    ↓
Return to frontend
```

## Technical Indicators

### Simple Moving Average (SMA)
```python
SMA(n) = (P1 + P2 + ... + Pn) / n
```
**Purpose**: Smooth price fluctuations, identify trends

### Relative Strength Index (RSI)
```python
RS = Average Gain / Average Loss
RSI = 100 - (100 / (1 + RS))
```
**Interpretation**:
- RSI > 70: Overbought (potential sell)
- RSI < 30: Oversold (potential buy)
- RSI = 50: Neutral

## Model Details

### Linear Regression
**Formula**: y = β₀ + β₁x₁ + β₂x₂ + β₃x₃ + β₄x₄

**Features (X)**:
- x₁: Current close price
- x₂: SMA(5)
- x₃: SMA(10)
- x₄: RSI(14)

**Target (y)**: Next-day close price

**Advantages**:
- Fast training/prediction
- Interpretable coefficients
- Low computational requirements
- Good for MVP

**Limitations**:
- Linear relationships only
- May not capture complex patterns
- Sensitive to outliers

## Caching Strategy

### Cache Keys
- Quotes: `{symbol}` (15 min TTL)
- Historical: `{symbol}_historical_{days}` (24 hour TTL)

### Cache Structure (SQLite)
```sql
CREATE TABLE cache (
    symbol TEXT PRIMARY KEY,
    data TEXT,           -- JSON serialized
    timestamp REAL       -- Unix timestamp
)
```

## API Rate Limits

### Alpha Vantage (Free Tier)
- 5 API calls per minute
- 500 API calls per day

### Handling Strategy
1. Check cache first
2. If cache miss, try Alpha Vantage
3. If rate limited, fallback to yfinance
4. Cache successful results

## Security Considerations

### API Keys
- Stored in `.env` file (not committed)
- Loaded via environment variables
- Never exposed to frontend

### CORS
- Configured for development (`allow_origins=["*"]`)
- Should be restricted in production

### Input Validation
- FastAPI automatic validation via Pydantic
- Symbol format checked by data sources

## Performance Optimizations

1. **Parallel API Calls**: Frontend fetches all data simultaneously
2. **Aggressive Caching**: Reduces API calls by 90%+
3. **Model Persistence**: No retraining on each request
4. **Lazy Training**: Models trained on-demand, not upfront
5. **SQLite WAL Mode**: Better concurrent read performance

## Deployment Considerations

### Environment Variables (Production)
- `ALPHA_VANTAGE_API_KEY` - Required
- `PORT` - Auto-set by platforms
- `VITE_API_URL` - Frontend API endpoint

### Scaling
- **Horizontal**: Multiple backend instances with shared cache (Redis)
- **Vertical**: Increase memory for more cached models
- **CDN**: Serve frontend static files

### Monitoring
- Health checks: `/health` endpoint
- Logs: Uvicorn access logs
- Metrics: Request counts, latency, cache hit rate

## Future Enhancements

### Short Term
- [ ] Background job for daily model retraining
- [ ] More technical indicators (MACD, Bollinger Bands)
- [ ] Historical prediction accuracy tracking
- [ ] User favorites/watchlist

### Long Term
- [ ] LSTM/GRU models for better predictions
- [ ] Multiple timeframe predictions (1d, 1w, 1m)
- [ ] News sentiment analysis integration
- [ ] Portfolio tracking and P&L calculation
- [ ] Email/SMS alerts for signals

## Testing

### Backend Tests
```bash
cd backend
python test_setup.py
```

### Manual API Testing
Visit http://localhost:8000/docs for Swagger UI

### Frontend Testing
```bash
cd frontend
npm run dev
# Manual testing in browser
```

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "API key not configured"
Edit `backend/.env` and add your Alpha Vantage key

### "Unable to fetch quote"
- Check API key validity
- Verify symbol format (e.g., AAPL, RELIANCE.NS)
- Check API rate limits

### Models not training
- Ensure 90+ days of historical data available
- Check internet connection
- Verify API quotas not exceeded

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify `VITE_API_URL` in `.env`

## Contributing

See README.md for contribution guidelines.

---

**Last Updated**: October 2025
**Version**: 1.0.0
