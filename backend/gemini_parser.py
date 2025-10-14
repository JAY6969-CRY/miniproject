"""
Gemini AI-Powered Natural Language Query Parser
Uses Google's Gemini API for intelligent stock query understanding
"""
import os
import json
import re
from typing import Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiNLPParser:
    """Parse natural language queries using Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        # Use gemini-1.5-flash for faster, cost-effective parsing
        # Alternative: 'gemini-1.5-pro' for more complex reasoning
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Fallback stock mapping for validation
        self.KNOWN_STOCKS = {
            # US Stocks
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'TSLA': 'Tesla Inc.',
            'META': 'Meta Platforms Inc.',
            'NVDA': 'NVIDIA Corporation',
            'NFLX': 'Netflix Inc.',
            'DIS': 'The Walt Disney Company',
            'BA': 'Boeing Company',
            'INTC': 'Intel Corporation',
            'AMD': 'Advanced Micro Devices',
            'WMT': 'Walmart Inc.',
            'KO': 'Coca-Cola Company',
            'PEP': 'PepsiCo Inc.',
            'MCD': "McDonald's Corporation",
            'NKE': 'Nike Inc.',
            'V': 'Visa Inc.',
            'MA': 'Mastercard Inc.',
            'PYPL': 'PayPal Holdings',
            'IBM': 'IBM',
            'ORCL': 'Oracle Corporation',
            'CSCO': 'Cisco Systems',
            'CRM': 'Salesforce Inc.',
            'ADBE': 'Adobe Inc.',
            'UBER': 'Uber Technologies',
            'ABNB': 'Airbnb Inc.',
            'SNAP': 'Snap Inc.',
            'ZM': 'Zoom Video Communications',
            'SPOT': 'Spotify Technology',
            'SQ': 'Block Inc.',
            
            # Indian Stocks (NSE)
            'RELIANCE.NS': 'Reliance Industries',
            'TCS.NS': 'Tata Consultancy Services',
            'INFY.NS': 'Infosys Limited',
            'HDFCBANK.NS': 'HDFC Bank',
            'ICICIBANK.NS': 'ICICI Bank',
            'HINDUNILVR.NS': 'Hindustan Unilever',
            'ITC.NS': 'ITC Limited',
            'SBIN.NS': 'State Bank of India',
            'BHARTIARTL.NS': 'Bharti Airtel',
            'BAJFINANCE.NS': 'Bajaj Finance',
            'KOTAKBANK.NS': 'Kotak Mahindra Bank',
            'LT.NS': 'Larsen & Toubro',
            'ASIANPAINT.NS': 'Asian Paints',
            'WIPRO.NS': 'Wipro Limited',
            'MARUTI.NS': 'Maruti Suzuki',
            'TATAMOTORS.NS': 'Tata Motors',
            'TATASTEEL.NS': 'Tata Steel',
            'SUNPHARMA.NS': 'Sun Pharmaceutical',
            'TITAN.NS': 'Titan Company',
            'AXISBANK.NS': 'Axis Bank',
            'ADANIENT.NS': 'Adani Enterprises',
            'ADANIPORTS.NS': 'Adani Ports',
            
            # Indian Stocks (BSE)
            'RELIANCE.BO': 'Reliance Industries',
            'TCS.BO': 'Tata Consultancy Services',
            'INFY.BO': 'Infosys Limited',
        }
    
    def parse(self, query: str) -> Dict:
        """
        Parse natural language query using Gemini AI
        
        Args:
            query: User's natural language question about stocks
            
        Returns:
            Dictionary with symbol, intent, company_name, and confidence
        """
        try:
            # Create a detailed prompt for Gemini
            prompt = f"""You are a stock market query parser. Analyze this user query and extract structured information.

User Query: "{query}"

Known Stock Symbols (US): AAPL (Apple), MSFT (Microsoft), GOOGL (Google), AMZN (Amazon), TSLA (Tesla), META (Facebook), NVDA (Nvidia), NFLX (Netflix), DIS (Disney), BA (Boeing), IBM, ORCL (Oracle), CSCO (Cisco), CRM (Salesforce), ADBE (Adobe), UBER, ABNB (Airbnb), SNAP (Snapchat), ZM (Zoom), SPOT (Spotify), SQ (Block/Square)

Known Stock Symbols (India): RELIANCE.NS, TCS.NS, INFY.NS (Infosys), HDFCBANK.NS, ICICIBANK.NS, HINDUNILVR.NS, ITC.NS, SBIN.NS (SBI), BHARTIARTL.NS (Airtel), BAJFINANCE.NS, KOTAKBANK.NS, LT.NS (Larsen & Toubro), ASIANPAINT.NS, WIPRO.NS, MARUTI.NS, TATAMOTORS.NS, TATASTEEL.NS, SUNPHARMA.NS, TITAN.NS, AXISBANK.NS, ADANIENT.NS, ADANIPORTS.NS

Extract the following information and respond ONLY with valid JSON (no markdown, no explanations):

{{
    "symbol": "STOCK_SYMBOL",
    "company_name": "Company Name",
    "intent": "buy|sell|hold|analyze|price|news",
    "sentiment": "bullish|bearish|neutral",
    "timeframe": "short_term|medium_term|long_term|intraday",
    "confidence": 0.0-1.0
}}

Rules:
1. IMPORTANT: Try hard to identify a stock. Use context clues:
   - "tech stock" → suggest AAPL or MSFT
   - "electric car" → TSLA
   - "Indian stock" → RELIANCE.NS or TCS.NS
   - "streaming" → NFLX or SPOT
   - "e-commerce" → AMZN
   - "AI" → NVDA or GOOGL
   - "bank" → HDFCBANK.NS or ICICIBANK.NS
   - "social media" → META or SNAP
2. For Indian companies, ALWAYS add .NS suffix (NSE listing)
3. If query is vague but has sector hint, suggest most popular stock in that sector
4. Only return "UNKNOWN" if absolutely no stock can be inferred
5. Intent should be one of: buy, sell, hold, analyze, price, news
6. Sentiment: bullish (positive), bearish (negative), neutral
7. Timeframe: intraday (<1 day), short_term (days-weeks), medium_term (weeks-months), long_term (months-years)
8. Confidence: Higher if stock explicitly mentioned, lower if inferred from context

Respond with JSON only:"""

            # Call Gemini API
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = re.sub(r'^```json?\s*', '', response_text)
                response_text = re.sub(r'\s*```$', '', response_text)
            
            # Parse JSON response
            result = json.loads(response_text)
            
            # Validate and enhance result
            symbol = result.get('symbol', '').upper()
            
            # Check if symbol exists in our known stocks
            if symbol not in self.KNOWN_STOCKS and symbol != 'UNKNOWN':
                # Try to find similar symbol
                symbol = self._find_similar_symbol(symbol)
            
            # Get company name from our database if not provided
            if symbol in self.KNOWN_STOCKS:
                result['company_name'] = self.KNOWN_STOCKS[symbol]
                result['symbol'] = symbol
            
            # Ensure all required fields exist
            result.setdefault('intent', 'analyze')
            result.setdefault('sentiment', 'neutral')
            result.setdefault('timeframe', 'medium_term')
            result.setdefault('confidence', 0.7)
            
            # Add original query
            result['original_query'] = query
            result['parsed_by'] = 'gemini'
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Response text: {response_text}")
            # Fallback to regex parser
            return self._fallback_parse(query)
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback to regex parser
            return self._fallback_parse(query)
    
    def _find_similar_symbol(self, symbol: str) -> str:
        """Find similar stock symbol from known stocks"""
        symbol_upper = symbol.upper()
        
        # Direct match
        if symbol_upper in self.KNOWN_STOCKS:
            return symbol_upper
        
        # Check if it's a partial match
        for known_symbol in self.KNOWN_STOCKS.keys():
            if symbol_upper in known_symbol or known_symbol.startswith(symbol_upper):
                return known_symbol
        
        return symbol_upper
    
    def _fallback_parse(self, query: str) -> Dict:
        """Fallback regex-based parser if Gemini fails"""
        query_lower = query.lower()
        
        # Try to extract symbol from query
        symbol = None
        company_name = None
        
        # Check for explicit symbols (all caps words)
        symbol_match = re.search(r'\b([A-Z]{2,5})\b', query)
        if symbol_match:
            symbol = symbol_match.group(1)
            if symbol in self.KNOWN_STOCKS:
                company_name = self.KNOWN_STOCKS[symbol]
        
        # Check for company names (partial matches too)
        if not symbol:
            for sym, name in self.KNOWN_STOCKS.items():
                name_lower = name.lower()
                # Check full name or key words from name
                name_words = name_lower.split()
                if (name_lower in query_lower or 
                    any(word in query_lower and len(word) > 3 for word in name_words)):
                    symbol = sym
                    company_name = name
                    break
        
        # Sector-based suggestions if still no match
        if not symbol:
            sector_map = {
                'tech': 'AAPL',
                'technology': 'AAPL',
                'apple': 'AAPL',
                'microsoft': 'MSFT',
                'google': 'GOOGL',
                'amazon': 'AMZN',
                'tesla': 'TSLA',
                'electric': 'TSLA',
                'ev': 'TSLA',
                'facebook': 'META',
                'meta': 'META',
                'social': 'META',
                'nvidia': 'NVDA',
                'ai': 'NVDA',
                'streaming': 'NFLX',
                'netflix': 'NFLX',
                'disney': 'DIS',
                'boeing': 'BA',
                'reliance': 'RELIANCE.NS',
                'tcs': 'TCS.NS',
                'tata': 'TCS.NS',
                'infosys': 'INFY.NS',
                'hdfc': 'HDFCBANK.NS',
                'icici': 'ICICIBANK.NS',
                'bank': 'HDFCBANK.NS',
                'indian': 'RELIANCE.NS',
                'india': 'RELIANCE.NS',
            }
            
            for keyword, sym in sector_map.items():
                if keyword in query_lower:
                    symbol = sym
                    company_name = self.KNOWN_STOCKS.get(sym, sym)
                    break
        
        # Determine intent
        intent = 'analyze'
        if any(word in query_lower for word in ['buy', 'purchase', 'invest', 'long']):
            intent = 'buy'
        elif any(word in query_lower for word in ['sell', 'exit', 'dump']):
            intent = 'sell'
        elif any(word in query_lower for word in ['hold', 'keep', 'wait']):
            intent = 'hold'
        elif any(word in query_lower for word in ['price', 'cost', 'trading at']):
            intent = 'price'
        elif any(word in query_lower for word in ['news', 'update', 'latest']):
            intent = 'news'
        
        # Determine timeframe
        timeframe = 'medium_term'
        if any(word in query_lower for word in ['intraday', 'day trade', 'today', 'scalp']):
            timeframe = 'intraday'
        elif any(word in query_lower for word in ['short', 'quick', 'swing']):
            timeframe = 'short_term'
        elif any(word in query_lower for word in ['long', 'invest', 'hold', 'years', 'retirement']):
            timeframe = 'long_term'
        
        return {
            'symbol': symbol or 'UNKNOWN',
            'company_name': company_name or 'Unknown',
            'intent': intent,
            'sentiment': 'neutral',
            'timeframe': timeframe,
            'confidence': 0.5,
            'original_query': query,
            'parsed_by': 'fallback'
        }
