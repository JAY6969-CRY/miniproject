# 🚀 Deploy Stock Predictor - Vercel + Render

## Your Deployment Plan: Option 2
- **Frontend:** Vercel (React + Vite) - Super fast CDN
- **Backend:** Render (FastAPI + Python) - Free API hosting
- **Total Cost:** $0.00/month
- **Time:** 10-15 minutes

---

## Part 1: Deploy Backend on Render (5-7 minutes)

### Step 1: Sign Up for Render

1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

### Step 2: Create Backend Web Service

1. **From Render Dashboard:**
   - Click **"New +"** (top right)
   - Select **"Web Service"**

2. **Connect Repository:**
   - Click **"Build and deploy from a Git repository"**
   - Click **"Connect"** next to: `JAY6969-CRY/miniproject`
   - If repo not visible, click **"Configure account"** and grant access

3. **Configure Service Settings:**

| Setting | Value |
|---------|-------|
| **Name** | `stock-predictor-api` |
| **Region** | Choose closest (e.g., Oregon) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |

4. **Build & Start Commands:**

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

5. **Instance Type:**
   - Select **"Free"** (512 MB RAM)

### Step 3: Add Environment Variables

Click **"Advanced"** → Scroll to **"Environment Variables"**

Add these **3 variables** (click "+ Add Environment Variable" for each):

**Variable 1:**
- Key: `ALPHA_VANTAGE_API_KEY`
- Value: `B6285XQINCRH073P`

**Variable 2:**
- Key: `NEWS_API_KEY`
- Value: `5b78003e86864acda172f59dccee91ca`

**Variable 3:**
- Key: `GEMINI_API_KEY`
- Value: `AIzaSyCI22SJFVeUAeHBpywp6JcsSwVJ9QMwB8Q`

### Step 4: Deploy Backend!

1. Click **"Create Web Service"** (bottom)
2. Render will start building (watch the logs)
3. Build takes ~2-3 minutes
4. Wait for: **"Your service is live 🎉"**

### Step 5: Get Backend URL

Once deployed:
1. Copy your backend URL (looks like):
   ```
   https://stock-predictor-api.onrender.com
   ```
2. **Save this URL!** You'll need it for frontend
3. Test it: Visit `https://your-backend-url.onrender.com/`
   - Should see: `{"message": "Stock Predictor API", ...}`

✅ **Backend deployed successfully!**

---

## Part 2: Update Frontend Configuration (2 minutes)

Before deploying frontend, we need to update the API URL.

### Option A: Update via GitHub Web Interface

1. Go to: https://github.com/JAY6969-CRY/miniproject
2. Navigate to: `frontend/.env.production`
3. Click **"Edit this file"** (pencil icon)
4. Change line 2 to your actual backend URL:
   ```env
   VITE_API_URL=https://stock-predictor-api.onrender.com
   ```
   *(Replace with YOUR actual Render URL from Step 5)*
5. Click **"Commit changes"**
6. Add commit message: `Update API URL for production`
7. Click **"Commit changes"**

### Option B: Update Locally

```powershell
cd d:\miniproject
# Edit frontend/.env.production
# Change VITE_API_URL to your Render backend URL
git add frontend/.env.production
git commit -m "Update API URL for production"
git push origin main
```

✅ **Frontend configuration updated!**

---

## Part 3: Deploy Frontend on Vercel (3-5 minutes)

### Step 1: Sign Up for Vercel

1. Go to **https://vercel.com**
2. Click **"Start Deploying"** or **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your repositories

### Step 2: Import Project

1. **From Vercel Dashboard:**
   - Click **"Add New..."** (top right)
   - Select **"Project"**

2. **Import Git Repository:**
   - Find: `JAY6969-CRY/miniproject`
   - Click **"Import"**
   - If not visible, click **"Adjust GitHub App Permissions"**

### Step 3: Configure Project

**Configure Project Settings:**

| Setting | Value |
|---------|-------|
| **Project Name** | `stock-predictor` (or any name) |
| **Framework Preset** | `Vite` |
| **Root Directory** | `frontend` (click Edit, select folder) |
| **Build Command** | `npm run build` (auto-detected) |
| **Output Directory** | `dist` (auto-detected) |

### Step 4: Environment Variables (Optional)

Vercel will use the `.env.production` file automatically, but you can also set it in dashboard:

Click **"Environment Variables"** (optional):
- Key: `VITE_API_URL`
- Value: `https://stock-predictor-api.onrender.com`
- Select: **Production** ✅

### Step 5: Deploy Frontend!

1. Click **"Deploy"** (bottom)
2. Vercel starts building (watch progress)
3. Build takes ~1-2 minutes
4. Wait for: **"Congratulations! 🎉"**

### Step 6: Get Frontend URL

Once deployed:
1. Vercel shows your live URL:
   ```
   https://stock-predictor.vercel.app
   ```
   or custom subdomain like:
   ```
   https://stock-predictor-jay6969.vercel.app
   ```
2. Click **"Visit"** to see your live app!

✅ **Frontend deployed successfully!**

---

## Part 4: Final Configuration (2-3 minutes)

### Update Backend CORS

Your backend needs to allow requests from the Vercel domain.

**Option A: Via GitHub**

1. Go to: https://github.com/JAY6969-CRY/miniproject
2. Edit: `backend/main.py`
3. Find the CORS section (around line 30)
4. Add your Vercel URL:
   ```python
   allow_origins=[
       # ... existing origins ...
       "https://stock-predictor.vercel.app",  # Add your Vercel URL
       "https://*.vercel.app",  # Already included (all Vercel apps)
   ],
   ```
5. Commit: `Add Vercel frontend URL to CORS`

**Option B: Locally**

```powershell
cd d:\miniproject\backend
# Edit main.py and add your Vercel URL to CORS origins
git add main.py
git commit -m "Add Vercel frontend URL to CORS"
git push origin main
```

Render will auto-deploy the changes!

✅ **CORS configured!**

---

## Part 5: Test Your Deployed App! 🎉

### 1. Test Backend API

Visit: `https://stock-predictor-api.onrender.com/`

**Expected:** JSON response with API info

**Test endpoints:**
- `/` - API info
- `/quote?symbol=AAPL` - Stock quote
- `/analyze?query=Should I buy Apple?&portfolio_type=aggressive` - Analysis

### 2. Test Frontend App

Visit: `https://stock-predictor.vercel.app`

**Test these features:**

✅ **Homepage loads**
- Search bar visible
- Navigation menu works

✅ **Search functionality**
- Search: "Should I invest in Apple?"
- Results appear
- Analysis shows

✅ **Budget feature**
- Click "+ Add Budget"
- Enter: $5000
- Get position sizing

✅ **Aggressive page**
- Navigate to "Aggressive Trading"
- Top stocks chart loads
- Click "Trade" on a stock

✅ **Long-term page**
- Navigate to "Long-term Investment"
- Search for a stock
- Get long-term analysis

✅ **Currency display**
- Search for: "TCS" (Indian stock)
- Should show: ₹ symbol
- Search for: "AAPL" (US stock)
- Should show: $ symbol

### 3. Check Performance

**First visit:**
- Backend might take 30 seconds to wake up (Render free tier sleeps)
- After that, responses should be fast

**Subsequent visits:**
- Frontend: <1 second load time (Vercel CDN)
- Backend: 200-500ms response time

---

## 🎊 Deployment Complete!

### Your Live URLs:

**Frontend (Vercel):**
```
https://stock-predictor.vercel.app
```

**Backend (Render):**
```
https://stock-predictor-api.onrender.com
```

---

## 📊 What You Now Have

### ✅ Features Live:
- AI-powered stock search (Gemini)
- Natural language understanding
- Top intraday stocks scanner
- Budget-based position sizing
- Currency localization (₹/$ )
- Separate strategy pages
- Real-time news sentiment
- Technical analysis (SMA, RSI)

### ✅ Infrastructure:
- Global CDN (Vercel)
- SSL certificates (auto)
- Auto-deploy on git push
- Unlimited bandwidth (Vercel)
- 750 hours/month backend (Render)

### ✅ Cost:
- **$0.00/month** 🎉

---

## 🔧 Post-Deployment

### Auto-Deploy Setup

**Already configured!** Every time you push to GitHub:

```powershell
git add .
git commit -m "Your changes"
git push origin main
```

- Vercel auto-deploys frontend (~1 min)
- Render auto-deploys backend (~2 min)

### Custom Domain (Optional)

**Vercel:**
1. Buy domain (e.g., from Namecheap - $10/year)
2. Go to Vercel → Project Settings → Domains
3. Add domain: `stockpredictor.com`
4. Update DNS (Vercel provides instructions)
5. SSL certificate auto-configured

**Render:**
1. Render Dashboard → Service → Settings
2. Custom Domain → Add
3. Update DNS CNAME record
4. SSL auto-configured

### Monitoring

**Vercel Dashboard:**
- Analytics (page views, performance)
- Deployment history
- Logs and errors

**Render Dashboard:**
- Logs (view API requests)
- Metrics (CPU, memory usage)
- Deploy history

---

## 🐛 Troubleshooting

### Issue: Backend takes 30 seconds to respond

**Why:** Render free tier sleeps after 15 min inactivity  
**Solution:** 
- Normal behavior on first request
- Upgrade to Starter ($7/month) for always-on
- Or: Use a service like UptimeRobot to ping every 10 min

### Issue: CORS errors in browser console

**Check:**
1. Vercel URL added to backend CORS?
2. Backend deployed with latest CORS changes?
3. Using HTTPS (not HTTP)?

**Fix:**
```python
# In backend/main.py, add your Vercel URL:
allow_origins=[
    "https://stock-predictor.vercel.app",
    "https://*.vercel.app",
]
```

### Issue: API calls return 404

**Check:**
1. Backend URL correct in `.env.production`?
2. Backend deployed successfully?
3. Environment variable set in Vercel?

**Test backend directly:**
```
https://stock-predictor-api.onrender.com/
```

### Issue: Vercel build fails

**Common causes:**
- Node modules error → Clear cache and redeploy
- Build command wrong → Should be `npm run build`
- Root directory wrong → Should be `frontend`

**Fix:**
1. Go to Vercel Project Settings
2. Update build settings
3. Redeploy

---

## 📈 Performance Optimization

### Speed Up Backend Wake Time

**Option 1: Keep-Alive Service (FREE)**
- Use UptimeRobot (free)
- Ping backend every 10 minutes
- Prevents sleeping

**Option 2: Upgrade Render ($7/month)**
- No sleep time
- Always-on instance
- Better performance

### Improve Frontend Performance

**Already optimized:**
- ✅ Vite for fast builds
- ✅ Vercel global CDN
- ✅ Automatic code splitting
- ✅ Image optimization

**Additional tips:**
- Use lazy loading for routes
- Minimize bundle size
- Enable Vercel Analytics

---

## 🎯 Next Steps

### Immediate:
- ✅ Share your live URL!
- ✅ Test all features thoroughly
- ✅ Add to your portfolio
- ✅ Share on LinkedIn/Twitter

### This Week:
- ⬜ Set up custom domain
- ⬜ Enable Vercel Analytics
- ⬜ Add error monitoring (Sentry)
- ⬜ Create documentation page
- ⬜ Add FAQ/Help section

### This Month:
- ⬜ User authentication
- ⬜ Save favorites/watchlist
- ⬜ Email notifications
- ⬜ Mobile app (React Native)
- ⬜ API rate limiting

---

## 📱 Share Your Project

### URLs to Share:

**Live App:**
```
https://stock-predictor.vercel.app
```

**GitHub:**
```
https://github.com/JAY6969-CRY/miniproject
```

### Social Media Templates:

**Twitter/LinkedIn:**
```
🚀 Just deployed my AI-powered Stock Predictor!

Features:
✅ Natural language search with Gemini AI
✅ Real-time stock analysis
✅ Intraday trading recommendations
✅ Budget-based position sizing
✅ Multi-currency support (₹/$)

Try it: https://stock-predictor.vercel.app
Code: https://github.com/JAY6969-CRY/miniproject

#WebDev #Python #React #FastAPI #AI #StockMarket
```

**Portfolio Description:**
```
Stock Predictor - AI-Powered Investment Analysis Platform

Full-stack web application using FastAPI, React, and Google's Gemini AI for intelligent stock market analysis and trading recommendations.

Tech Stack: Python, FastAPI, React, Vite, TailwindCSS, Gemini AI
Deployed on: Vercel + Render

Live Demo: https://stock-predictor.vercel.app
```

---

## 🎉 Congratulations!

You've successfully deployed your Stock Predictor app!

### What You Achieved:
- ✅ Built a full-stack ML application
- ✅ Integrated AI (Gemini) for NLP
- ✅ Deployed to production (FREE)
- ✅ Global CDN distribution
- ✅ SSL certificates
- ✅ Auto-deploy pipeline

### Deployment Stats:
- **Time Taken:** ~15 minutes
- **Cost:** $0.00/month
- **Platforms:** Vercel + Render
- **Features:** All working!

---

## 📞 Need Help?

**Resources:**
- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)

**Community:**
- Vercel Discord
- Render Community
- Reddit: r/webdev

---

**Enjoy your live app! 🚀**

Share your URL - I'd love to see it in action! 🎉
