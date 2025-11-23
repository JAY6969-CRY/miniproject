"""
Test script for the stock screener functionality
"""
from stock_screener import StockScreener

def test_screener():
    print("🧪 Testing Stock Screener...\n")
    
    screener = StockScreener()
    
    # Test get_hidden_gems
    print("📊 Fetching Hidden Gems...")
    result = screener.get_hidden_gems()
    
    print(f"\n✅ Success: {result['success']}")
    print(f"📈 Total Found: {result['total_found']}")
    print(f"📋 Description: {result['description']}\n")
    
    print("🎯 Screening Criteria:")
    for key, value in result['screening_criteria'].items():
        print(f"  - {key}: {value}")
    
    print(f"\n💎 Top {len(result['stocks'])} Hidden Gems:\n")
    
    for i, stock in enumerate(result['stocks'][:5], 1):
        print(f"{i}. {stock['name']} ({stock['symbol']})")
        print(f"   Price: ₹{stock['price']:.2f} | P/E: {stock['pe_ratio']:.2f}")
        print(f"   Quality Score: {stock['quality_score']}/100")
        print(f"   ROCE: {stock['roce']:.1f}% | ROE: {stock['roe']:.1f}%")
        print(f"   Sales Growth 5Y: {stock['sales_growth_5y']:.1f}%")
        print(f"   EPS Growth 5Y: {stock['eps_growth_5y']:.1f}%")
        print(f"   Recommendation: {stock['recommendation']}")
        print(f"   Sector: {stock['sector']}\n")

if __name__ == "__main__":
    test_screener()
