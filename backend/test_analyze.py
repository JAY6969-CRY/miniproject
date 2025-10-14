"""
Test script for the natural language analysis endpoint
"""
import requests
import json

def test_analyze_endpoint():
    """Test the /analyze endpoint"""
    base_url = "http://localhost:8000"
    
    # Test queries
    test_queries = [
        "Can I invest in Apple today?",
        "Should I buy Tesla stock?",
        "Is Reliance a good investment?",
        "AAPL"  # Traditional symbol
    ]
    
    print("=" * 70)
    print("TESTING NATURAL LANGUAGE INVESTMENT ADVISOR")
    print("=" * 70)
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 70)
        
        try:
            response = requests.get(
                f"{base_url}/analyze",
                params={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print(f"✅ Success!")
                    print(f"   Symbol: {data.get('symbol')}")
                    print(f"   Company: {data.get('company_name')}")
                    
                    analysis = data.get('analysis', {})
                    print(f"   Recommendation: {analysis.get('recommendation')}")
                    print(f"   Confidence: {analysis.get('confidence')} ({analysis.get('confidence_score')})")
                    print(f"   Should Invest: {analysis.get('should_invest')}")
                    
                    # Show growth factors
                    growth_factors = analysis.get('growth_factors', [])
                    if growth_factors:
                        print(f"   Growth Factors:")
                        for factor in growth_factors[:2]:
                            print(f"      • {factor}")
                    
                else:
                    print(f"❌ Error: {data.get('error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to {base_url}")
            print(f"   Make sure the backend server is running!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 70)
    print("Test complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_analyze_endpoint()
