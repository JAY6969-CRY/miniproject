from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from data_fetcher import DataFetcher
from model_trainer import ModelTrainer
from predictor import Predictor

app = FastAPI(
    title="Stock Market Forecast API",
    description="Next-day stock price prediction for NSE, BSE, and NASDAQ tickers",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_fetcher = DataFetcher()
model_trainer = ModelTrainer()
predictor = Predictor()

# Response models
class QuoteResponse(BaseModel):
    symbol: str
    price: float
    change: float
    change_percent: str
    volume: int
    latest_trading_day: str
    source: str

class PredictionResponse(BaseModel):
    symbol: str
    current_price: float
    predicted_price: float
    prediction_change: float
    prediction_change_percent: float

class SignalResponse(BaseModel):
    symbol: str
    signal: str
    confidence: str
    reason: str
    timing: str
    current_price: float
    predicted_price: float
    change_percent: float
    portfolio_type: str

@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Stock Market Forecast API",
        "status": "active",
        "endpoints": [
            "/quote?symbol=RELIANCE.NS",
            "/predict?symbol=RELIANCE.NS",
            "/signal?symbol=RELIANCE.NS",
            "/chart?symbol=RELIANCE.NS",
            "/portfolio?symbol=RELIANCE.NS&type=aggressive",
            "/train?symbol=RELIANCE.NS"
        ]
    }

@app.get("/quote", response_model=QuoteResponse)
async def get_quote(symbol: str = Query(..., description="Stock symbol (e.g., RELIANCE.NS, AAPL)")):
    """
    Get current stock quote
    
    Examples:
    - NSE: RELIANCE.NS, TCS.NS, INFY.NS
    - BSE: RELIANCE.BO, TCS.BO
    - NASDAQ: AAPL, GOOGL, MSFT
    """
    try:
        quote = data_fetcher.get_quote(symbol)
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predict", response_model=PredictionResponse)
async def get_prediction(symbol: str = Query(..., description="Stock symbol")):
    """
    Predict next-day closing price
    
    Uses historical data and technical indicators (SMA, RSI) to forecast.
    Model trains automatically if not available for the symbol.
    """
    try:
        prediction = predictor.predict_next_day(symbol)
        return {
            "symbol": prediction['symbol'],
            "current_price": prediction['current_price'],
            "predicted_price": prediction['predicted_price'],
            "prediction_change": prediction['prediction_change'],
            "prediction_change_percent": prediction['prediction_change_percent']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/signal", response_model=SignalResponse)
async def get_signal(symbol: str = Query(..., description="Stock symbol")):
    """
    Get buy/sell/hold recommendation
    
    Returns trading signal with reasoning and optimal timing based on technical analysis.
    """
    try:
        signal = predictor.generate_signal(symbol)
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chart")
async def get_chart_data(symbol: str = Query(..., description="Stock symbol")):
    """
    Get historical prices + prediction for charting
    
    Returns 30 days of historical data plus next-day prediction.
    """
    try:
        chart_data = predictor.get_chart_data(symbol)
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio")
async def get_portfolio_signal(
    symbol: str = Query(..., description="Stock symbol"),
    type: str = Query("balanced", description="Portfolio type: aggressive, balanced, or long_term")
):
    """
    Get personalized trading signal based on portfolio type
    
    Portfolio types:
    - aggressive: 1% threshold, short-term trades
    - balanced: 2% threshold, medium-term holds (default)
    - long_term: 3% threshold, long-term investments
    """
    if type not in ["aggressive", "balanced", "long_term"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid portfolio type. Choose: aggressive, balanced, or long_term"
        )
    
    try:
        signal = predictor.generate_signal(symbol, portfolio_type=type)
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
async def train_model(symbol: str = Query(..., description="Stock symbol")):
    """
    Manually train or retrain model for a symbol
    
    Fetches 90 days of historical data and trains a new prediction model.
    Useful for updating models with latest market data.
    """
    try:
        historical_data = data_fetcher.get_historical_data(symbol, days=90)
        result = model_trainer.train_model(symbol, historical_data)
        return {
            "message": f"Model trained successfully for {symbol}",
            "details": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Service health check"""
    return {"status": "healthy", "service": "stock-predictor"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
