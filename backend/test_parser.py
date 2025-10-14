"""
Test Gemini Parser with various queries
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Load environment
load_dotenv()

from gemini_parser import GeminiNLPParser

def test_queries():
    parser = GeminiNLPParser()
    
    test_cases = [
        "What's a good tech stock?",
        "Should I invest in Apple?",
        "Tell me about Tesla",
        "Is Reliance a good buy?",
        "Give me a stock recommendation",
        "What about Microsoft?",
        "Any good Indian stocks?",
        "Is AAPL a buy?",
        "What's the best AI stock?",
        "Should I buy Netflix?",
        "Tell me about TSLA",
        "Random query with no stock info"
    ]
    
    print("=" * 70)
    print("TESTING GEMINI PARSER")
    print("=" * 70)
    print()
    
    for i, query in enumerate(test_cases, 1):
        print(f"{i}. Query: \"{query}\"")
        try:
            result = parser.parse(query)
            print(f"   Symbol: {result.get('symbol')}")
            print(f"   Company: {result.get('company_name')}")
            print(f"   Intent: {result.get('intent')}")
            print(f"   Confidence: {result.get('confidence')}")
            print(f"   Parsed by: {result.get('parsed_by')}")
            
            if result.get('symbol') == 'UNKNOWN':
                print("   ⚠️  No stock identified")
            else:
                print("   ✅ Stock identified successfully")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()

if __name__ == "__main__":
    test_queries()
