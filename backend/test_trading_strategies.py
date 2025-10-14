"""
Test trading strategies with budget
"""
import requests

def test_with_budget():
    """Test analyze endpoint with budget parameter"""
    base_url = "http://localhost:8000"
    
    test_cases = [
        {
            "query": "Should I buy Apple stock?",
            "strategy": "aggressive",
            "budget": 10000,
            "desc": "Intraday/Aggressive with $10k budget"
        },
        {
            "query": "Is Tesla a good long-term investment?",
            "strategy": "long_term",
            "budget": 25000,
            "desc": "Long-term investment with $25k budget"
        }
    ]
    
    print("=" * 80)
    print("TESTING TRADING STRATEGIES WITH BUDGET")
    print("=" * 80)
    
    for test in test_cases:
        print(f"\n{'='*80}")
        print(f"Test: {test['desc']}")
        print(f"Query: '{test['query']}'")
        print(f"Strategy: {test['strategy'].upper()}")
        print(f"Budget: ${test['budget']:,}")
        print("-" * 80)
        
        try:
            response = requests.get(
                f"{base_url}/analyze",
                params={
                    "query": test['query'],
                    "portfolio_type": test['strategy'],
                    "budget": test['budget']
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print(f"✅ Success!")
                    print(f"   Symbol: {data.get('symbol')}")
                    print(f"   Current Price: ${data.get('quote', {}).get('price'):.2f}")
                    
                    # Trading Plan
                    plan = data.get('trading_plan')
                    if plan:
                        print(f"\n   📋 TRADING PLAN: {plan['strategy']}")
                        print(f"   Risk Level: {plan['risk_level']}")
                        print(f"   Recommended Shares: {plan['recommended_shares']}")
                        print(f"   Capital Needed: ${plan['budget_required']:,.2f} ({plan['capital_used_pct']}% of budget)")
                        print(f"   Entry Price: ${plan['entry_price']}")
                        print(f"   Stop Loss: ${plan['stop_loss']}")
                        print(f"   Target Price: ${plan['target_price']}")
                        print(f"   Potential Profit: ${plan['potential_profit']:,.2f}")
                        print(f"   Potential Loss: ${plan['potential_loss']:,.2f}")
                        print(f"   Entry Timing: {plan['entry_timing']}")
                        print(f"   Exit Timing: {plan['exit_timing']}")
                        print(f"   Holding Period: {plan['holding_period']}")
                    else:
                        print("   ⚠️ No trading plan generated")
                        
                else:
                    print(f"❌ Error: {data.get('error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to {base_url}")
            print(f"   Make sure the backend server is running!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("Test complete!")
    print("=" * 80)

if __name__ == "__main__":
    test_with_budget()
