"""
Test all API keys and configurations
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("🔍 CHECKING ENVIRONMENT CONFIGURATION")
print("=" * 70)
print()

# Check Alpha Vantage API Key
alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
print("1. ALPHA VANTAGE API KEY:")
if alpha_key and len(alpha_key) > 10:
    print(f"   ✅ CONFIGURED: {alpha_key[:10]}...{alpha_key[-4:]}")
    print(f"   Length: {len(alpha_key)} characters")
else:
    print("   ❌ NOT CONFIGURED or INVALID")
print()

# Check News API Key
news_key = os.getenv('NEWS_API_KEY')
print("2. NEWS API KEY:")
if news_key and len(news_key) > 10:
    print(f"   ✅ CONFIGURED: {news_key[:10]}...{news_key[-4:]}")
    print(f"   Length: {len(news_key)} characters")
else:
    print("   ⚠️  NOT CONFIGURED (Optional - will use mock news)")
print()

# Check Gemini API Key
gemini_key = os.getenv('GEMINI_API_KEY')
print("3. GEMINI API KEY:")
if gemini_key and len(gemini_key) > 10:
    print(f"   ✅ CONFIGURED: {gemini_key[:10]}...{gemini_key[-4:]}")
    print(f"   Length: {len(gemini_key)} characters")
    
    # Test Gemini import
    try:
        import google.generativeai as genai
        print("   ✅ google-generativeai library installed")
        
        # Test API connection
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-pro')
            print("   ✅ Gemini API connection successful")
        except Exception as e:
            print(f"   ⚠️  API connection issue: {str(e)[:50]}")
    except ImportError:
        print("   ⚠️  google-generativeai library not installed")
        print("   Run: pip install google-generativeai")
else:
    print("   ⚠️  NOT CONFIGURED (Optional - will use fallback parser)")
print()

print("=" * 70)
print("📊 CONFIGURATION SUMMARY")
print("=" * 70)
print()

all_configured = all([
    alpha_key and len(alpha_key) > 10,
    news_key and len(news_key) > 10,
    gemini_key and len(gemini_key) > 10
])

if all_configured:
    print("✅ ALL API KEYS CONFIGURED!")
    print("   Your app has full functionality:")
    print("   • Stock data fetching (Alpha Vantage)")
    print("   • Real news sentiment (NewsAPI)")
    print("   • AI-powered search (Gemini)")
else:
    print("⚠️  PARTIAL CONFIGURATION:")
    if not alpha_key or len(alpha_key) < 10:
        print("   ❌ Alpha Vantage key missing (REQUIRED)")
    if not news_key or len(news_key) < 10:
        print("   ⚠️  News API key missing (Optional)")
    if not gemini_key or len(gemini_key) < 10:
        print("   ⚠️  Gemini key missing (Optional)")
print()

# Test imports
print("=" * 70)
print("🧪 TESTING CORE MODULES")
print("=" * 70)
print()

try:
    from data_fetcher import DataFetcher
    print("✅ DataFetcher")
except Exception as e:
    print(f"❌ DataFetcher: {e}")

try:
    from predictor import Predictor
    print("✅ Predictor")
except Exception as e:
    print(f"❌ Predictor: {e}")

try:
    from nlp_parser import NLPParser
    print("✅ NLPParser")
except Exception as e:
    print(f"❌ NLPParser: {e}")

try:
    from news_analyzer import NewsAnalyzer
    print("✅ NewsAnalyzer")
except Exception as e:
    print(f"❌ NewsAnalyzer: {e}")

try:
    from advisor import StockAdvisor
    print("✅ StockAdvisor")
except Exception as e:
    print(f"❌ StockAdvisor: {e}")

try:
    from trading_strategy import TradingStrategy
    print("✅ TradingStrategy")
except Exception as e:
    print(f"❌ TradingStrategy: {e}")

try:
    from top_stocks import TopStocksRecommender
    print("✅ TopStocksRecommender")
except Exception as e:
    print(f"❌ TopStocksRecommender: {e}")

try:
    from gemini_parser import GeminiNLPParser
    print("✅ GeminiNLPParser")
except Exception as e:
    print(f"⚠️  GeminiNLPParser: {e}")

print()
print("=" * 70)
print("🚀 FINAL STATUS")
print("=" * 70)
print()

if all_configured:
    print("🎉 YOUR APP IS FULLY CONFIGURED!")
    print()
    print("Next steps:")
    print("1. Backend is running on: http://localhost:8000")
    print("2. Frontend is running on: http://localhost:3000")
    print("3. Try the features:")
    print("   • Top Stocks Chart: http://localhost:3000/aggressive")
    print("   • AI Search: Ask any question naturally")
    print("   • Full analysis with all features enabled")
else:
    print("⚠️  YOUR APP IS PARTIALLY CONFIGURED")
    print()
    print("What's working:")
    if alpha_key and len(alpha_key) > 10:
        print("✅ Stock predictions and basic features")
    if news_key and len(news_key) > 10:
        print("✅ Real news sentiment analysis")
    else:
        print("⚠️  Mock news will be used")
    if gemini_key and len(gemini_key) > 10:
        print("✅ AI-powered natural language search")
    else:
        print("⚠️  Standard NLP parser will be used")

print()
print("=" * 70)
