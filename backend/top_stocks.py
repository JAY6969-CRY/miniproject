"""
Top Stocks Recommender for Aggressive Trading
Identifies high-volume, volatile stocks suitable for intraday trading
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
import json
import os

class TopStocksRecommender:
    """Recommend top stocks for aggressive/intraday trading"""
    
    # Pre-defined list of liquid stocks for intraday trading
    INTRADAY_WATCHLIST = {
        # High volume US tech stocks
        'US': [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
            'NVDA', 'META', 'NFLX', 'AMD', 'INTC',
            'UBER', 'LYFT', 'SNAP', 'COIN', 'PLTR',
            'RIVN', 'LCID', 'NIO', 'BABA', 'JD'
        ],
        # High volume Indian stocks
        'INDIA': [
            'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 
            'ICICIBANK.NS', 'SBIN.NS', 'BHARTIARTL.NS', 
            'TATAMOTORS.NS', 'TATASTEEL.NS', 'ADANIENT.NS',
            'WIPRO.NS', 'TECHM.NS', 'LTIM.NS', 'YESBANK.NS',
            'ITC.NS', 'HINDUNILVR.NS', 'AXISBANK.NS', 'KOTAKBANK.NS'
        ]
    }
    
    def __init__(self):
        self.cache_file = 'top_stocks_cache.json'
        self.cache_duration = 3600  # 1 hour cache
    
    def get_top_aggressive_stocks(self, limit: int = 10, region: str = 'US') -> List[Dict]:
        """
        Get top recommended stocks for aggressive trading
        
        Args:
            limit: Number of stocks to return
            region: 'US' or 'INDIA'
            
        Returns:
            List of stock dictionaries with metrics
        """
        # Check cache first
        cached_data = self._load_cache(region)
        if cached_data:
            return cached_data[:limit]
        
        # Fetch fresh data
        stocks_data = []
        watchlist = self.INTRADAY_WATCHLIST.get(region, self.INTRADAY_WATCHLIST['US'])
        
        for symbol in watchlist:
            try:
                stock_info = self._analyze_stock(symbol)
                if stock_info:
                    stocks_data.append(stock_info)
            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")
                continue
        
        # Sort by trading score (volatility + volume + momentum)
        stocks_data.sort(key=lambda x: x['trading_score'], reverse=True)
        
        # Cache the results
        self._save_cache(stocks_data, region)
        
        return stocks_data[:limit]
    
    def _analyze_stock(self, symbol: str) -> Dict:
        """Analyze a stock for intraday trading suitability"""
        try:
            # Fetch data
            stock = yf.Ticker(symbol)
            hist = stock.history(period='5d', interval='1d')
            
            if hist.empty or len(hist) < 3:
                return None
            
            # Calculate metrics
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            change_pct = ((current_price - prev_close) / prev_close) * 100
            
            # Volume analysis
            avg_volume = hist['Volume'].mean()
            today_volume = hist['Volume'].iloc[-1]
            volume_surge = ((today_volume - avg_volume) / avg_volume) * 100 if avg_volume > 0 else 0
            
            # Volatility (average daily range)
            hist['daily_range'] = ((hist['High'] - hist['Low']) / hist['Low']) * 100
            avg_volatility = hist['daily_range'].mean()
            
            # Momentum (3-day change)
            momentum = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
            
            # Trading score (weighted combination)
            trading_score = (
                abs(change_pct) * 0.3 +           # Today's movement
                min(volume_surge, 100) * 0.2 +     # Volume surge (capped)
                avg_volatility * 0.3 +             # Volatility
                abs(momentum) * 0.2                # Momentum
            )
            
            # Determine signal
            signal = 'NEUTRAL'
            if change_pct > 2 and momentum > 3:
                signal = 'STRONG BUY'
            elif change_pct > 1:
                signal = 'BUY'
            elif change_pct < -2 and momentum < -3:
                signal = 'STRONG SELL'
            elif change_pct < -1:
                signal = 'SELL'
            
            # Get company info
            info = stock.info
            company_name = info.get('longName', info.get('shortName', symbol))
            
            return {
                'symbol': symbol,
                'company_name': company_name,
                'current_price': round(current_price, 2),
                'change_percent': round(change_pct, 2),
                'volume': int(today_volume),
                'avg_volume': int(avg_volume),
                'volume_surge': round(volume_surge, 1),
                'volatility': round(avg_volatility, 2),
                'momentum': round(momentum, 2),
                'trading_score': round(trading_score, 2),
                'signal': signal,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            return None
    
    def _load_cache(self, region: str) -> List[Dict]:
        """Load cached stock data"""
        try:
            if not os.path.exists(self.cache_file):
                return None
            
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            
            region_cache = cache.get(region, {})
            timestamp = region_cache.get('timestamp', 0)
            
            # Check if cache is still valid
            if datetime.now().timestamp() - timestamp < self.cache_duration:
                return region_cache.get('data', [])
            
            return None
            
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None
    
    def _save_cache(self, data: List[Dict], region: str):
        """Save stock data to cache"""
        try:
            # Load existing cache
            cache = {}
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            
            # Update region cache
            cache[region] = {
                'timestamp': datetime.now().timestamp(),
                'data': data
            }
            
            # Save cache
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f)
                
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def get_stock_details(self, symbol: str) -> Dict:
        """Get detailed information for a specific stock"""
        return self._analyze_stock(symbol)
