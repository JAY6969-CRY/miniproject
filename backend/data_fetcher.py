import sqlite3
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import yfinance as yf
import requests
from config import settings

class DataFetcher:
    def __init__(self):
        self.alpha_vantage_key = settings.ALPHA_VANTAGE_API_KEY
        self.cache_db = settings.CACHE_DB_PATH
        self._init_cache_db()
    
    def _init_cache_db(self):
        """Initialize SQLite cache database"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                symbol TEXT PRIMARY KEY,
                data TEXT,
                timestamp REAL
            )
        """)
        conn.commit()
        conn.close()
    
    def _get_cached_data(self, symbol: str, max_age_hours: int = 1) -> Optional[Dict]:
        """Retrieve cached data if fresh"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        cursor.execute("SELECT data, timestamp FROM cache WHERE symbol = ?", (symbol,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            data, timestamp = row
            age_hours = (time.time() - timestamp) / 3600
            if age_hours < max_age_hours:
                return json.loads(data)
        return None
    
    def _save_to_cache(self, symbol: str, data: Dict):
        """Save data to cache"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO cache (symbol, data, timestamp) VALUES (?, ?, ?)",
            (symbol, json.dumps(data), time.time())
        )
        conn.commit()
        conn.close()
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get current stock quote - try Alpha Vantage first, fallback to yfinance"""
        # Check cache first
        cached = self._get_cached_data(symbol, max_age_hours=0.25)  # 15 min cache for quotes
        if cached:
            return cached
        
        # Try Alpha Vantage first
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.alpha_vantage_key
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                result = {
                    "symbol": symbol,
                    "price": float(quote.get("05. price", 0)),
                    "change": float(quote.get("09. change", 0)),
                    "change_percent": quote.get("10. change percent", "0%"),
                    "volume": int(quote.get("06. volume", 0)),
                    "latest_trading_day": quote.get("07. latest trading day", ""),
                    "source": "alphavantage"
                }
                self._save_to_cache(symbol, result)
                return result
        except Exception as e:
            print(f"Alpha Vantage error: {e}")
        
        # Fallback to yfinance
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if len(hist) > 0:
                current_price = hist['Close'].iloc[-1]
                prev_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
                change = current_price - prev_close
                change_percent = (change / prev_close * 100) if prev_close else 0
                
                result = {
                    "symbol": symbol,
                    "price": float(current_price),
                    "change": float(change),
                    "change_percent": f"{change_percent:.2f}%",
                    "volume": int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                    "latest_trading_day": hist.index[-1].strftime("%Y-%m-%d"),
                    "source": "yfinance"
                }
                self._save_to_cache(symbol, result)
                return result
        except Exception as e:
            print(f"yfinance error: {e}")
        
        raise ValueError(f"Unable to fetch quote for {symbol}")
    
    def get_historical_data(self, symbol: str, days: int = 90) -> Dict[str, Any]:
        """Get historical stock data for model training"""
        cache_key = f"{symbol}_historical_{days}"
        cached = self._get_cached_data(cache_key, max_age_hours=24)  # 24 hour cache
        if cached:
            return cached
        
        # Try yfinance first for historical data (more reliable)
        try:
            ticker = yf.Ticker(symbol)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            hist = ticker.history(start=start_date, end=end_date)
            
            if len(hist) > 0:
                result = {
                    "symbol": symbol,
                    "dates": hist.index.strftime("%Y-%m-%d").tolist(),
                    "open": hist['Open'].tolist(),
                    "high": hist['High'].tolist(),
                    "low": hist['Low'].tolist(),
                    "close": hist['Close'].tolist(),
                    "volume": hist['Volume'].tolist(),
                    "source": "yfinance"
                }
                self._save_to_cache(cache_key, result)
                return result
        except Exception as e:
            print(f"yfinance historical error: {e}")
        
        # Fallback to Alpha Vantage
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "outputsize": "full",
                "apikey": self.alpha_vantage_key
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "Time Series (Daily)" in data:
                time_series = data["Time Series (Daily)"]
                dates = sorted(list(time_series.keys()))[-days:]
                
                result = {
                    "symbol": symbol,
                    "dates": dates,
                    "open": [float(time_series[d]["1. open"]) for d in dates],
                    "high": [float(time_series[d]["2. high"]) for d in dates],
                    "low": [float(time_series[d]["3. low"]) for d in dates],
                    "close": [float(time_series[d]["4. close"]) for d in dates],
                    "volume": [int(time_series[d]["5. volume"]) for d in dates],
                    "source": "alphavantage"
                }
                self._save_to_cache(cache_key, result)
                return result
        except Exception as e:
            print(f"Alpha Vantage historical error: {e}")
        
        raise ValueError(f"Unable to fetch historical data for {symbol}")
