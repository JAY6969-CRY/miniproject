# 🚀 Quick Start - Hidden Gems Feature

## Testing the Feature (Local Development)

### Step 1: Start Backend Server
```bash
cd "d:\Projects\Personal Projects\miniproject\backend"
python main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
✅ Gemini AI parser initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test Backend Endpoint (Optional)
Open a new terminal:
```bash
curl http://localhost:8000/screener/hidden-gems
```

Or open in browser:
```
http://localhost:8000/screener/hidden-gems
```

You should see JSON response with 10 stocks.

### Step 3: Start Frontend Development Server
```bash
cd "d:\Projects\Personal Projects\miniproject\frontend"
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 4: View the Feature
1. Open browser: `http://localhost:5173`
2. Click "Long-Term Investment" button
3. Scroll down to see "💎 Hidden Gems - Quality Stocks" section
4. Click "Analyze" on any stock to test integration

## What You Should See

### ✅ Success Indicators
- Green header with "📈 Long-Term Investment"
- Search bar at the top
- Hidden Gems section loads automatically
- Table shows 10 stocks with metrics
- "Analyze" buttons are clickable
- Clicking Analyze shows full stock analysis below

### ❌ Troubleshooting

#### Backend Not Starting
**Issue**: Import errors
```bash
# Install missing dependencies
pip install fastapi uvicorn pydantic
```

#### Frontend Build Errors
**Issue**: Module not found
```bash
# Reinstall dependencies
npm install
```

#### Hidden Gems Not Showing
**Check**:
1. Backend is running on port 8000
2. No console errors in browser (F12)
3. API URL is correct in `.env` file
4. CORS is properly configured

#### API Connection Failed
**Fix**: Update frontend `.env` file:
```
VITE_API_URL=http://localhost:8000
```

## Feature Verification Checklist

- [ ] Backend server starts without errors
- [ ] `/screener/hidden-gems` endpoint returns data
- [ ] Frontend builds successfully
- [ ] Long-Term page loads
- [ ] Hidden Gems section appears
- [ ] Table shows 10 stocks
- [ ] Quality scores are calculated
- [ ] Recommendations are color-coded
- [ ] "Analyze" buttons work
- [ ] Clicking Analyze loads stock details
- [ ] No console errors

## Sample Stock Data

The feature comes preloaded with 15 high-quality Indian stocks:

1. **IMEC Services** - Services (Score: 100/100)
2. **Stellant Security** - Security Services (Score: 89.3/100)
3. **Tips Music** - Media & Entertainment (Score: 85/100)
4. **Websol Energy** - Solar Energy (Score: 77.4/100)
5. **Shilchar Technologies** - Technology (Score: 75.1/100)
6. **Waaree Renewable** - Renewable Energy
7. **Esab India** - Manufacturing
8. **Shakti Pumps** - Industrial
9. **CAMS Services** - Financial Services
10. **Indian Energy Exchange** - Power Exchange

And 5 more: IRCTC, HDFC AMC, Mazagon Dock, Premier Energies, Infosys

## Next Steps

### Add More Stocks
Edit: `backend/stock_screener.py`
```python
QUALITY_STOCKS = [
    # Add your stocks here
    {
        'name': 'New Company',
        'symbol': 'NEWCO.NS',
        'price': 500.0,
        # ... other fields
    }
]
```

### Customize Filters
Edit: `backend/stock_screener.py` → `get_hidden_gems()` function
```python
gems = self.screen_stocks(
    min_roce=50.0,  # Change from 40%
    min_roe=20.0,   # Change from 15%
    # ... adjust other criteria
)
```

### Change Number of Results
```python
gems = self.screen_stocks(
    # ... filters ...
    top_n=20  # Show top 20 instead of 10
)
```

## Production Deployment

### Backend (Render/Railway)
The endpoint is automatically available at:
```
https://your-backend-url.com/screener/hidden-gems
```

### Frontend (Vercel)
No changes needed - API URL is from environment variable.

### Environment Variables
Ensure `VITE_API_URL` points to production backend.

## Support

### Documentation Files Created
- `HIDDEN_GEMS_FEATURE.md` - Complete implementation guide
- `HIDDEN_GEMS_VISUAL_GUIDE.md` - UI/UX documentation
- This file - Quick start guide

### Test Script
Run comprehensive test:
```bash
cd backend
python test_screener.py
```

---

## 🎉 You're All Set!

The Hidden Gems feature is now ready to help users discover quality long-term investment opportunities!

**Key Points**:
- ✅ Fully functional stock screener
- ✅ Beautiful, responsive UI
- ✅ Integrated with existing analysis
- ✅ Quality scoring algorithm
- ✅ No external API dependencies (uses sample data)

**Future Enhancement**: Connect to live stock data APIs for real-time information.

