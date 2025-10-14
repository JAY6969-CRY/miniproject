# Budget Allocation & Currency Updates

## Issue Fixed
Previously, when users entered a budget (e.g., ₹50,000), the system was only using 25-30% of it, showing something like "29.7% of budget used". This was due to overly conservative risk management settings.

## Changes Made

### 1. Trading Strategy Budget Allocation

**Aggressive/Intraday Strategy:**
- **Before:** Used only 30% of budget (max_position_size = budget * 0.3)
- **After:** Uses up to 90% of budget (max_position_size = budget * 0.90)
- Keeps 10% buffer for price movements
- Max risk: 3% of total budget

**Long-Term Investment Strategy:**
- **Before:** Used only 25% of budget (max_position_size = budget * 0.25)
- **After:** Uses up to 85% of budget (max_position_size = budget * 0.85)
- Keeps 15% buffer (more conservative than intraday)
- Max risk: 7% of total budget

**Balanced/Swing Strategy:**
- **Before:** Used only 25% of budget
- **After:** Uses up to 80% of budget (max_position_size = budget * 0.80)
- Keeps 20% buffer
- Max risk: 5% of total budget

### 2. Currency Localization

**Backend (trading_strategy.py):**
- Added `_get_currency_info()` method that detects market based on symbol
- Indian stocks (NSE: .NS, BSE: .BO) → ₹ (INR)
- US stocks (NASDAQ, NYSE) → $ (USD)
- Currency info now included in every trading plan response

**Frontend (SearchBar.jsx):**
- Added real-time market detection based on user query
- Shows appropriate currency symbol (₹ or $) in budget input
- Displays market indicator (🇮🇳 Indian Market or 🇺🇸 US Market)
- Auto-adjusts placeholder amounts (₹50,000 for India, $5,000 for US)

**Frontend (AnalysisCard.jsx):**
- Uses currency from backend trading_plan.currency
- Falls back to symbol-based detection if not provided

## Example Budget Calculations

### Scenario 1: Intraday Trading with ₹50,000
- **Budget:** ₹50,000
- **Allocation:** 90% = ₹45,000
- **Stock Price:** ₹3,500
- **Shares:** 12 shares (₹42,000)
- **Capital Used:** ~84% of budget ✅

### Scenario 2: Long-Term Investment with $5,000
- **Budget:** $5,000
- **Allocation:** 85% = $4,250
- **Stock Price:** $170 (e.g., AAPL)
- **Shares:** 25 shares ($4,250)
- **Capital Used:** ~85% of budget ✅

### Scenario 3: Balanced Strategy with ₹100,000
- **Budget:** ₹100,000
- **Allocation:** 80% = ₹80,000
- **Stock Price:** ₹1,200
- **Shares:** 66 shares (₹79,200)
- **Capital Used:** ~79% of budget ✅

## Risk Management Preserved

While we now use more of the budget, risk management is still enforced:

1. **Stop Loss Protection:** 
   - Aggressive: 1.5% stop loss
   - Balanced: 5% stop loss
   - Long-term: 8% stop loss

2. **Maximum Risk Limits:**
   - Aggressive: Max 3% of total budget at risk
   - Balanced: Max 5% of total budget at risk
   - Long-term: Max 7% of total budget at risk

3. **Risk Validation:**
   - If calculated risk exceeds limits, shares are reduced
   - Formula: `max_shares_by_risk = max_risk_amount / risk_per_share`
   - Final shares = min(affordable, risk-allowed)

## Files Modified

1. **backend/trading_strategy.py**
   - Updated `_calculate_intraday_position()`
   - Updated `_calculate_longterm_position()`
   - Updated `_calculate_balanced_position()`
   - Added `_get_currency_info()` method

2. **frontend/src/components/SearchBar.jsx**
   - Added market detection logic
   - Dynamic currency symbol in budget input
   - Market indicator badge

3. **frontend/src/components/AnalysisCard.jsx**
   - Use currency from backend trading_plan
   - Fallback detection logic

## Testing

### Test with Indian Stock:
```
Query: "TCS stock"
Budget: ₹50,000
Expected: ~42,000-45,000 allocated (84-90%)
Currency: ₹ displayed
```

### Test with US Stock:
```
Query: "Apple stock"
Budget: $5,000
Expected: ~4,000-4,500 allocated (80-90%)
Currency: $ displayed
```

### Test Aggressive vs Long-term:
```
Same stock, same budget
Aggressive: 90% allocation (higher turnover)
Long-term: 85% allocation (more conservative)
```

## Benefits

✅ **Better Budget Utilization:** Users get recommendations that match their budget
✅ **Clear Currency Display:** No confusion between $ and ₹
✅ **Market-Aware:** Automatically detects Indian vs US stocks
✅ **Risk-Managed:** Still enforces strict risk limits
✅ **Realistic Calculations:** Matches real-world trading scenarios

## Note

The system keeps a small buffer (10-20%) to account for:
- Price volatility during order execution
- Brokerage fees and taxes
- Slippage in market orders
- Maintaining emergency reserves

This ensures users can actually execute the recommended trades!
