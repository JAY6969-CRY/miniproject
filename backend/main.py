from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

from data_fetcher import DataFetcher
from model_trainer import ModelTrainer
from predictor import Predictor
from nlp_parser import NLPParser
from advisor import StockAdvisor
from top_stocks import TopStocksRecommender
from stock_screener import StockScreener

# Try to import Gemini parser, fall back to NLP parser if not available
try:
    from gemini_parser import GeminiNLPParser
    USE_GEMINI = True
except ImportError:
    USE_GEMINI = False
    print("Gemini parser not available, using fallback NLP parser")

app = FastAPI(
    title="Stock Market Forecast API",
    description="Next-day stock price prediction for NSE, BSE, and NASDAQ tickers",
    version="1.0.0"
)

# Configure CORS
# Allow requests from local development and common deployment platforms
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://miniproject-biahc05cq-jayasimhareddy872-8873s-projects.vercel.app",
        "https://miniproject-gold-beta.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_fetcher = DataFetcher()
model_trainer = ModelTrainer()
predictor = Predictor()
nlp_parser = NLPParser()
advisor = StockAdvisor()
top_stocks = TopStocksRecommender()
stock_screener = StockScreener()

# Initialize Gemini parser if available
gemini_parser = None
if USE_GEMINI:
    try:
        gemini_parser = GeminiNLPParser()
        print("✅ Gemini AI parser initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Gemini parser: {e}")
        USE_GEMINI = False

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

class AnalyzeRequest(BaseModel):
    query: str
    portfolio_type: Optional[str] = "balanced"

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
            "/train?symbol=RELIANCE.NS",
            "/analyze?query=can I invest in apple today"
        ],
        "example_queries": nlp_parser.get_example_queries()
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

@app.get("/analyze")
async def analyze_query(
    query: str = Query(..., description="Natural language query about stock investment"),
    portfolio_type: str = Query("balanced", description="Portfolio type: aggressive, balanced, or long_term"),
    budget: float = Query(None, description="Available budget for trading (optional)")
):
    """
    Analyze stock investment using natural language query
    
    Examples:
    - "Can I invest in Apple today?"
    - "Should I buy Tesla stock?"
    - "Is Reliance a good investment?"
    - "How many TCS shares should I buy?"
    
    Returns comprehensive analysis including:
    - Technical indicators and prediction
    - Recent news and sentiment analysis
    - Growth and risk factors
    - Investment recommendation with reasoning
    """
    try:
        # Parse the natural language query
        parsed = nlp_parser.parse_query(query)
        
        if not parsed.get('parsed') or not parsed.get('symbol'):
            return {
                "success": False,
                "error": "Could not understand the query. Please mention a stock name or symbol.",
                "parsed": parsed,
                "examples": nlp_parser.get_example_queries()
            }
        
        # Get comprehensive analysis
        analysis = advisor.analyze_investment(
            symbol=parsed['symbol'],
            company_name=parsed.get('company_name', parsed['symbol']),
            user_intent=parsed.get('intent', 'analyze'),
            quantity=parsed.get('quantity'),
            portfolio_type=portfolio_type,
            budget=budget
        )
        
        # Add parsed query info
        analysis['parsed_query'] = {
            'original': query,
            'detected_symbol': parsed['symbol'],
            'detected_company': parsed.get('company_name'),
            'detected_intent': parsed.get('intent'),
            'detected_quantity': parsed.get('quantity'),
            'confidence': parsed.get('confidence')
        }
        
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/top-stocks")
async def get_top_stocks(
    limit: int = Query(10, description="Number of stocks to return"),
    region: str = Query("US", description="Region: US or INDIA")
):
    """
    Get top recommended stocks for aggressive/intraday trading
    
    Returns stocks sorted by trading score (volatility + volume + momentum)
    Perfect for the aggressive trading page!
    
    Args:
        limit: Number of stocks to return (default: 10)
        region: US or INDIA (default: US)
    """
    try:
        stocks = top_stocks.get_top_aggressive_stocks(limit=limit, region=region)
        return {
            "success": True,
            "region": region,
            "count": len(stocks),
            "stocks": stocks,
            "last_updated": stocks[0]['last_updated'] if stocks else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze-gemini")
async def analyze_query_gemini(
    query: str = Query(..., description="Natural language question about stocks"),
    portfolio_type: str = Query("balanced", description="Portfolio type: aggressive, balanced, or long_term"),
    budget: float = Query(None, description="Available budget for trading (optional)")
):
    """
    🤖 AI-Powered Stock Analysis using Google Gemini
    
    This endpoint uses Google's Gemini AI to understand ANY natural language query
    about stocks and provides intelligent, contextual responses.
    
    Examples:
    - "What's a good tech stock to buy right now?"
    - "I have $10000, which Indian stock should I invest in for long term?"
    - "Tell me about Tesla's future prospects"
    - "Compare Apple and Microsoft for day trading"
    - "Which stock will give me quick profits?"
    
    The AI will:
    - Understand context and intent
    - Identify the stock(s) mentioned
    - Provide comprehensive analysis
    - Give actionable recommendations
    """
    if not USE_GEMINI or not gemini_parser:
        return {
            "success": False,
            "error": "Gemini AI is not configured. Please set GEMINI_API_KEY environment variable.",
            "fallback": "Using standard NLP parser instead"
        }
    
    try:
        # Parse with Gemini AI
        parsed = gemini_parser.parse(query)
        
        if parsed.get('symbol') == 'UNKNOWN' or not parsed.get('symbol'):
            # Provide helpful suggestions
            popular_stocks = [
                "AAPL (Apple)", "MSFT (Microsoft)", "GOOGL (Google)", 
                "TSLA (Tesla)", "AMZN (Amazon)", "NVDA (Nvidia)",
                "RELIANCE.NS (Reliance)", "TCS.NS (TCS)", "INFY.NS (Infosys)"
            ]
            return {
                "success": False,
                "error": "Could not identify a specific stock from your query.",
                "parsed": parsed,
                "suggestion": "Try asking about a specific stock. Examples:",
                "examples": [
                    "What's a good tech stock to buy?",
                    "Should I invest in Apple?",
                    "Tell me about Tesla",
                    "Is Reliance a good buy?"
                ],
                "popular_stocks": popular_stocks
            }
        
        # Get comprehensive analysis
        analysis = advisor.analyze_investment(
            symbol=parsed['symbol'],
            company_name=parsed.get('company_name', parsed['symbol']),
            user_intent=parsed.get('intent', 'analyze'),
            quantity=None,
            portfolio_type=portfolio_type,
            budget=budget
        )
        
        # Add Gemini parsed info
        analysis['gemini_insights'] = {
            'original_query': query,
            'detected_symbol': parsed['symbol'],
            'detected_company': parsed.get('company_name'),
            'detected_intent': parsed.get('intent'),
            'sentiment': parsed.get('sentiment'),
            'timeframe': parsed.get('timeframe'),
            'confidence': parsed.get('confidence'),
            'parsed_by': parsed.get('parsed_by', 'gemini')
        }
        
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/screener/hidden-gems")
async def get_hidden_gems():
    """
    Get hidden gems - high-quality stocks with strong fundamentals at attractive valuations
    Perfect for long-term investment opportunities
    """
    try:
        result = stock_screener.get_hidden_gems()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to screen stocks: {str(e)}")

@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "stock-predictor",
        "gemini_enabled": USE_GEMINI,
        "features": {
            "gemini_ai": USE_GEMINI,
            "top_stocks": True,
            "trading_strategies": True,
            "news_sentiment": True
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
