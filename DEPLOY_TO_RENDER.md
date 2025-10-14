# 🚀 Quick Deploy - Stock Predictor to Render (FREE)

## ⚡ 5-Minute Deployment

Follow these steps to deploy your stock predictor completely FREE on Render.

---

## Prerequisites
- [x] GitHub account with repo: `JAY6969-CRY/miniproject`
- [x] Render account (sign up at render.com - FREE)
- [x] API Keys ready (Alpha Vantage, NewsAPI, Gemini)

---

## Step 1: Deploy Backend (FastAPI)

### 1.1 Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Click **"Build and deploy from a Git repository"**
4. Connect your GitHub account (if not already connected)
5. Select repository: **`JAY6969-CRY/miniproject`**
6. Click **"Connect"**

### 1.2 Configure Service

Fill in the following:

**Basic Settings:**
- **Name:** `stock-predictor-backend` (or any name you like)
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:**
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **"Free"** (512 MB RAM, shared CPU)

### 1.3 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these three variables:

| Key | Value |
|-----|-------|
| `ALPHA_VANTAGE_API_KEY` | `B6285XQINCRH073P` |
| `NEWS_API_KEY` | `5b78003e86864acda172f59dccee91ca` |
| `GEMINI_API_KEY` | `AIzaSyCI22SJFVeUAeHBpywp6JcsSwVJ9QMwB8Q` |

### 1.4 Deploy!

1. Click **"Create Web Service"**
2. Render will start building (takes 2-3 minutes)
3. Once deployed, you'll get a URL like:
   ```
   https://stock-predictor-backend.onrender.com
   ```
4. **Save this URL!** You'll need it for frontend

### 1.5 Test Backend

Visit: `https://your-backend-url.onrender.com/`

You should see:
```json
{
  "message": "Stock Predictor API",
  "version": "1.0.0",
  "endpoints": [...]
}
```

✅ Backend deployed successfully!

---

## Step 2: Deploy Frontend (React + Vite)

### 2.1 Update Frontend Environment Variable

**Before deploying frontend, update the API URL:**

1. Go to your GitHub repo
2. Edit `frontend/.env.production`
3. Change:
   ```env
   VITE_API_URL=https://your-actual-backend-url.onrender.com
   ```
4. Replace with your actual backend URL from Step 1.4
5. Commit and push

### 2.2 Create Static Site

1. Go back to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Static Site"**
3. Select repository: **`JAY6969-CRY/miniproject`**
4. Click **"Connect"**

### 2.3 Configure Static Site

Fill in the following:

**Basic Settings:**
- **Name:** `stock-predictor-frontend`
- **Branch:** `main`
- **Root Directory:** `frontend`

**Build Settings:**
- **Build Command:**
  ```bash
  npm install && npm run build
  ```

- **Publish Directory:**
  ```
  dist
  ```

**Advanced (Optional):**
- **Auto-Deploy:** Yes
- **Pull Request Previews:** Enabled (optional)

### 2.4 Add Rewrite Rule (SPA Support)

In **"Redirects/Rewrites"** section:

- **Source:** `/*`
- **Destination:** `/index.html`
- **Action:** `Rewrite`

This ensures React Router works correctly.

### 2.5 Deploy Frontend!

1. Click **"Create Static Site"**
2. Render builds (takes 1-2 minutes)
3. Once deployed, you'll get a URL like:
   ```
   https://stock-predictor-frontend.onrender.com
   ```

### 2.6 Test Frontend

Visit your frontend URL and test:
- ✅ Homepage loads
- ✅ Search for "Apple" or "AAPL"
- ✅ Get analysis results
- ✅ Navigate to Aggressive/Long-term pages
- ✅ Top stocks chart loads

---

## Step 3: Update Backend CORS (Important!)

Your backend needs to allow requests from the frontend domain.

### 3.1 Update main.py CORS

Edit `backend/main.py` and update CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://stock-predictor-frontend.onrender.com",  # Add your frontend URL
        "https://your-custom-domain.com"  # If you have custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3.2 Push Changes

```bash
cd d:\miniproject
git add backend/main.py
git commit -m "chore: Update CORS for production deployment"
git push origin main
```

Render will auto-deploy the changes!

---

## 🎉 Deployment Complete!

Your app is now live!

### Your URLs:
- **Backend API:** `https://stock-predictor-backend.onrender.com`
- **Frontend App:** `https://stock-predictor-frontend.onrender.com`

### Test Everything:
1. Visit frontend URL
2. Search: "Should I invest in Apple?"
3. Add budget: $5000
4. Check aggressive page for top stocks
5. Test long-term page

---

## 📊 Post-Deployment

### Monitor Your App
- **Render Dashboard:** View logs, metrics, deploy history
- **Free Tier Limits:**
  - 750 hours/month (plenty for hobby projects)
  - Sleeps after 15 min inactivity
  - Takes ~30 seconds to wake up

### Auto-Deploy
- Every git push to `main` auto-deploys
- Check deploy logs in Render dashboard

### Custom Domain (Optional)
1. Buy domain (e.g., from Namecheap)
2. In Render: Settings → Custom Domain
3. Add CNAME record pointing to Render
4. SSL certificate added automatically

---

## 🔧 Troubleshooting

### Backend won't start:
- Check logs in Render dashboard
- Verify environment variables are set
- Ensure requirements.txt is correct

### Frontend shows errors:
- Check browser console (F12)
- Verify VITE_API_URL is correct
- Check backend CORS settings

### API calls fail:
- Backend might be sleeping (wait 30 sec)
- Check CORS configuration
- Verify API keys are valid

### "Module not found" errors:
- Ensure all dependencies in requirements.txt
- Check Python version compatibility
- Re-deploy with fresh build

---

## 💰 Cost: $0.00/month!

Render free tier includes:
- ✅ 750 hours/month
- ✅ Auto-deploy from Git
- ✅ SSL certificates
- ✅ Custom domains
- ✅ Preview deployments

Perfect for portfolios, demos, and hobby projects!

---

## 🚀 What's Next?

### Upgrade Options:
- **Render Starter ($7/month):**
  - No sleep
  - Always-on
  - Better performance
  
- **Add Database:**
  - Render free PostgreSQL
  - Store user preferences
  - Historical analysis

### Enhancements:
- Add user authentication
- Save favorite stocks
- Email alerts for price targets
- Mobile app (React Native)

---

## 📝 Maintenance

### Keep It Running:
- Monitor usage in Render dashboard
- Update dependencies regularly
- Check API key usage limits
- Review logs for errors

### Stay Updated:
```bash
git pull origin main  # Get latest code
# Make changes
git push origin main  # Auto-deploys
```

---

## Need Help?

- **Render Docs:** https://render.com/docs
- **GitHub Issues:** Create issue in your repo
- **Community:** Render Community Forums

---

**Congratulations!** 🎉 Your Stock Predictor is LIVE!

Share your deployment URL and show off your project! 🚀
