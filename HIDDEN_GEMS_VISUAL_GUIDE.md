# 🎨 Hidden Gems Feature - Visual Guide

## Feature Location
**Page**: Long-Term Investment Section (`/long-term`)

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  📈 Long-Term Investment                      [← Back to Home]  │
│  Wealth building · 3-6 month holds · Growth focused             │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  8% Stop Loss │ 20% Target │ 3-6 Months │ 25% Max Position     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  🔍 Search Bar - "Ask about any stock..."                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  💎 Hidden Gems - Quality Stocks          [Found: 10]           │
│  ─────────────────────────────────────────────────────────────  │
│  High-quality stocks with strong fundamentals at attractive     │
│  valuations for long-term wealth creation                       │
│                                                                  │
│  🎯 Screening Criteria Applied:                                 │
│  ┌──────┬──────┬────────────┬────────────┬──────┬──────┬──────┐│
│  │ROCE  │ ROE  │Sales Growth│EPS Growth  │ P/E  │Debt/E│ OPM  ││
│  │≥ 40% │≥ 15% │   ≥ 15%    │   ≥ 15%    │≤ 50  │≤ 0.5 │≥ 15% ││
│  └──────┴──────┴────────────┴────────────┴──────┴──────┴──────┘│
│                                                                  │
│  📊 Stock Table:                                                │
│  ┌────┬─────────────────┬───────┬──────┬──────┬────┬─────┬────┐│
│  │Rnk │Company          │Price  │ P/E  │Score │ROCE│ ROE │Rec ││
│  ├────┼─────────────────┼───────┼──────┼──────┼────┼─────┼────┤│
│  │🥇 1│IMEC Services    │229.65 │ 1.77 │100/100│177%│91% │⭐⭐││
│  │    │Services         │       │      │      │    │     │[Analyze]│
│  ├────┼─────────────────┼───────┼──────┼──────┼────┼─────┼────┤│
│  │🥈 2│Stellant Security│368.20 │ 4.37 │89.3  │107%│95% │⭐⭐││
│  │    │Security Services│       │      │      │    │     │[Analyze]│
│  ├────┼─────────────────┼───────┼──────┼──────┼────┼─────┼────┤│
│  │🥉 3│Tips Music       │495.20 │36.42 │85.0  │109%│65% │⭐  ││
│  │    │Media & Ent.     │       │      │      │    │     │[Analyze]│
│  └────┴─────────────────┴───────┴──────┴──────┴────┴─────┴────┘│
│                                                                  │
│  📊 Quality Score Methodology: Composite score based on         │
│  ROCE (25%), ROE (20%), Growth Metrics (30%), Valuation (25%)   │
└─────────────────────────────────────────────────────────────────┘
```

## Color Coding

### Quality Score Colors
- **100-75**: 🟢 Bold Green (Excellent Quality)
- **74-65**: 🟢 Emerald (Very Good Quality)
- **64-55**: 🔵 Blue (Good Quality)
- **54-0**: ⚪ Gray (Fair Quality)

### Recommendation Badges
- **STRONG BUY**: Green background, green border
- **BUY**: Emerald background, emerald border
- **ACCUMULATE**: Blue background, blue border
- **HOLD & WATCH**: Yellow background, yellow border
- **RESEARCH MORE**: Gray background, gray border

## User Interaction Flow

```
1. User visits Long-Term Page
        ↓
2. Hidden Gems auto-loads (loading spinner shown)
        ↓
3. Table displays with top 10 stocks
        ↓
4. User reviews metrics (Quality Score, ROCE, ROE, Growth, etc.)
        ↓
5. User clicks "Analyze" button on interesting stock
        ↓
6. Full stock analysis loads below (same as search)
        ↓
7. User gets complete trading strategy & recommendation
```

## Sample Stock Card

```
┌─────────────────────────────────────────────────────────────────┐
│ 🥇 #1                                                            │
├─────────────────────────────────────────────────────────────────┤
│ IMEC Services                                  ₹229.65          │
│ Services                                                         │
│                                                                  │
│ P/E: 1.77          Quality Score: 100/100 (Excellent)          │
│ ROCE: 177.1%       ROE: 91.0%                                   │
│ Sales Growth 5Y: 57.5%     EPS Growth 5Y: 822.7%               │
│                                                                  │
│ [STRONG BUY]                              [Analyze Stock]       │
└─────────────────────────────────────────────────────────────────┘
```

## Responsive Design

### Desktop View (>1024px)
- Full table with all columns visible
- Horizontal layout for criteria badges
- Large, readable fonts

### Tablet View (768px - 1024px)
- Slightly compressed table
- All data still visible
- Smaller fonts but still readable

### Mobile View (<768px)
- Horizontal scroll for table
- Criteria badges stack in 2-3 columns
- Tap to analyze stocks
- Pinch to zoom table

## Animation Effects

### On Load
- Fade-in animation for entire card
- Skeleton loading state for table

### On Hover
- Row highlights with light green background
- Analyze button scales slightly larger
- Cursor changes to pointer

### On Click
- Analyze button shows loading state
- Smooth scroll to analysis results
- Hidden Gems card stays visible for reference

## Data Display Format

### Numbers
- **Price**: ₹XXX.XX (2 decimal places)
- **P/E Ratio**: X.XX (2 decimal places)
- **Quality Score**: XX.X/100 (1 decimal place)
- **Percentages**: XX.X% (1 decimal place)

### Text
- **Company Name**: Bold, larger font
- **Sector**: Smaller, gray text below name
- **Recommendation**: All caps, badge format

## Empty States

### Loading State
```
┌─────────────────────────────────────────────────────────────────┐
│                        🔄 Loading...                             │
│          Loading investment opportunities...                     │
└─────────────────────────────────────────────────────────────────┘
```

### Error State (if API fails)
```
┌─────────────────────────────────────────────────────────────────┐
│                          ⚠️ Error                               │
│          Unable to load stock data. Please try again.           │
└─────────────────────────────────────────────────────────────────┘
```

### No Results State (if no stocks match criteria)
```
┌─────────────────────────────────────────────────────────────────┐
│                      🔍 No Stocks Found                         │
│     No stocks currently match the screening criteria.           │
│              Try adjusting your filters.                         │
└─────────────────────────────────────────────────────────────────┘
```

## Integration with Existing Features

### Works With
✅ Existing search functionality
✅ Budget-based analysis
✅ Trading strategy recommendations
✅ Technical indicators
✅ News sentiment analysis (if enabled)

### Enhances
✅ Long-term investment decisions
✅ Portfolio diversification
✅ Stock discovery process
✅ Fundamental analysis workflow

---

## Quick Reference Card

**Purpose**: Find high-quality stocks for long-term investment
**Location**: Long-Term Investment page, below search bar
**Updates**: Loads fresh data on each page visit
**Stocks Shown**: Top 10 by quality score
**Click Action**: "Analyze" button → Full stock analysis
**Mobile**: Swipe table horizontally to see all data

