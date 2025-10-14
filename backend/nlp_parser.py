"""
Natural Language Query Parser
Extracts stock symbols, intent, and investment amount from conversational queries
"""
import re
from typing import Dict, Optional

class NLPParser:
    """Parse natural language queries about stocks"""
    
    # Stock name to symbol mapping
    STOCK_MAPPING = {
        # US Stocks
        'apple': 'AAPL',
        'microsoft': 'MSFT',
        'google': 'GOOGL',
        'alphabet': 'GOOGL',
        'amazon': 'AMZN',
        'tesla': 'TSLA',
        'meta': 'META',
        'facebook': 'META',
        'nvidia': 'NVDA',
        'netflix': 'NFLX',
        'disney': 'DIS',
        'boeing': 'BA',
        'intel': 'INTC',
        'amd': 'AMD',
        'walmart': 'WMT',
        'coca cola': 'KO',
        'pepsi': 'PEP',
        'mcdonalds': 'MCD',
        'nike': 'NKE',
        'visa': 'V',
        'mastercard': 'MA',
        'paypal': 'PYPL',
        'ibm': 'IBM',
        'oracle': 'ORCL',
        'cisco': 'CSCO',
        'salesforce': 'CRM',
        'adobe': 'ADBE',
        'uber': 'UBER',
        'lyft': 'LYFT',
        'airbnb': 'ABNB',
        'twitter': 'TWTR',
        'x': 'TWTR',
        'snapchat': 'SNAP',
        'zoom': 'ZM',
        'spotify': 'SPOT',
        'square': 'SQ',
        'block': 'SQ',
        'robinhood': 'HOOD',
        'coinbase': 'COIN',
        'palantir': 'PLTR',
        'snowflake': 'SNOW',
        
        # Indian Stocks (NSE)
        'reliance': 'RELIANCE.NS',
        'tcs': 'TCS.NS',
        'tata consultancy': 'TCS.NS',
        'infosys': 'INFY.NS',
        'hdfc': 'HDFCBANK.NS',
        'hdfc bank': 'HDFCBANK.NS',
        'icici': 'ICICIBANK.NS',
        'icici bank': 'ICICIBANK.NS',
        'bharti': 'BHARTIARTL.NS',
        'bharti airtel': 'BHARTIARTL.NS',
        'airtel': 'BHARTIARTL.NS',
        'itc': 'ITC.NS',
        'sbi': 'SBIN.NS',
        'state bank': 'SBIN.NS',
        'wipro': 'WIPRO.NS',
        'larsen': 'LT.NS',
        'l&t': 'LT.NS',
        'larsen toubro': 'LT.NS',
        'hcl tech': 'HCLTECH.NS',
        'hcltech': 'HCLTECH.NS',
        'axis bank': 'AXISBANK.NS',
        'axis': 'AXISBANK.NS',
        'bajaj finance': 'BAJFINANCE.NS',
        'maruti': 'MARUTI.NS',
        'maruti suzuki': 'MARUTI.NS',
        'asian paints': 'ASIANPAINT.NS',
        'titan': 'TITAN.NS',
        'ultratech': 'ULTRACEMCO.NS',
        'nestle': 'NESTLEIND.NS',
        'hul': 'HINDUNILVR.NS',
        'hindustan unilever': 'HINDUNILVR.NS',
        'adani': 'ADANIENT.NS',
        'adani enterprises': 'ADANIENT.NS',
        'adani ports': 'ADANIPORTS.NS',
        'jsw steel': 'JSWSTEEL.NS',
        'tata steel': 'TATASTEEL.NS',
        'tata motors': 'TATAMOTORS.NS',
        'mahindra': 'M&M.NS',
        'kotak': 'KOTAKBANK.NS',
        'kotak bank': 'KOTAKBANK.NS',
        'power grid': 'POWERGRID.NS',
        'ongc': 'ONGC.NS',
        'ntpc': 'NTPC.NS',
        'coal india': 'COALINDIA.NS',
        'sun pharma': 'SUNPHARMA.NS',
        'dr reddy': 'DRREDDY.NS',
        'cipla': 'CIPLA.NS',
        'divis lab': 'DIVISLAB.NS',
    }
    
    # Intent keywords
    BUY_KEYWORDS = ['buy', 'invest', 'purchase', 'get', 'acquire', 'long', 'bullish', 'good investment']
    SELL_KEYWORDS = ['sell', 'exit', 'dump', 'short', 'bearish', 'bad investment']
    HOLD_KEYWORDS = ['hold', 'keep', 'maintain', 'stay']
    ANALYZE_KEYWORDS = ['analyze', 'analysis', 'check', 'look at', 'review', 'worth', 'should i']
    
    def parse_query(self, query: str) -> Dict:
        """
        Parse natural language query and extract structured information
        
        Args:
            query: Natural language query like "can i invest in apple today"
            
        Returns:
            Dictionary with symbol, intent, quantity, and parsed query info
        """
        query_lower = query.lower().strip()
        
        result = {
            'original_query': query,
            'symbol': None,
            'company_name': None,
            'intent': 'analyze',  # Default intent
            'quantity': None,
            'confidence': 0.0,
            'parsed': False
        }
        
        # Extract stock symbol
        symbol_info = self._extract_symbol(query_lower)
        if symbol_info:
            result['symbol'] = symbol_info['symbol']
            result['company_name'] = symbol_info['name']
            result['confidence'] = symbol_info['confidence']
            result['parsed'] = True
        
        # Extract intent
        result['intent'] = self._extract_intent(query_lower)
        
        # Extract quantity
        result['quantity'] = self._extract_quantity(query_lower)
        
        return result
    
    def _extract_symbol(self, query: str) -> Optional[Dict]:
        """Extract stock symbol from query"""
        # First, try to match company names (more reliable for natural language)
        best_match = None
        best_confidence = 0.0
        
        for name, symbol in self.STOCK_MAPPING.items():
            if name in query:
                # Calculate confidence based on match quality
                confidence = len(name) / len(query)
                confidence = min(confidence * 2, 0.9)  # Normalize
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = {
                        'symbol': symbol,
                        'name': name.title(),
                        'confidence': confidence
                    }
        
        # If no company name found, try ticker symbols (for direct symbol queries)
        if not best_match:
            # Only match if query is short and looks like a ticker (2-5 chars, uppercase)
            ticker_pattern = r'\b([A-Z]{2,5}(?:\.[A-Z]{2})?)\b'
            ticker_matches = re.findall(ticker_pattern, query.upper())
            
            if ticker_matches and len(query.strip()) <= 10:  # Short queries only
                return {
                    'symbol': ticker_matches[0],
                    'name': ticker_matches[0],
                    'confidence': 0.95
                }
        
        return best_match
    
    def _extract_intent(self, query: str) -> str:
        """Extract user intent from query"""
        # Check for buy intent
        for keyword in self.BUY_KEYWORDS:
            if keyword in query:
                return 'buy'
        
        # Check for sell intent
        for keyword in self.SELL_KEYWORDS:
            if keyword in query:
                return 'sell'
        
        # Check for hold intent
        for keyword in self.HOLD_KEYWORDS:
            if keyword in query:
                return 'hold'
        
        # Default to analyze
        return 'analyze'
    
    def _extract_quantity(self, query: str) -> Optional[int]:
        """Extract stock quantity from query"""
        # Look for patterns like "buy 10 stocks", "100 shares", etc.
        patterns = [
            r'(\d+)\s*(?:stocks?|shares?|units?)',
            r'(?:buy|purchase|get)\s*(\d+)',
            r'(\d+)\s*(?:of|in)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                try:
                    quantity = int(match.group(1))
                    if 1 <= quantity <= 10000:  # Reasonable range
                        return quantity
                except ValueError:
                    continue
        
        return None
    
    def get_example_queries(self) -> list:
        """Get example queries for user guidance"""
        return [
            "Can I invest in Apple today?",
            "Should I buy Tesla stock?",
            "Is Reliance a good investment?",
            "How many TCS shares should I buy?",
            "Should I sell my Amazon stocks?",
            "Is it worth investing in Microsoft?",
            "What about Google stock?",
            "Should I buy 10 shares of Infosys?",
            "Is HDFC Bank a good buy?",
            "Can I hold my Nvidia stocks?",
        ]
