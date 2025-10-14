# Stock Predictor - Deployment Guide

## 🚀 Deployment Options

This guide covers multiple deployment platforms for your stock predictor app.

---

## Option 1: Render (Recommended - FREE)

### Why Render?
- ✅ Free tier available
- ✅ Automatic deploys from Git
- ✅ Supports Python + Node.js
- ✅ Free PostgreSQL database
- ✅ Custom domains
- ✅ SSL certificates

### Steps:

#### A. Backend Deployment (FastAPI)

1. **Sign up at [Render.com](https://render.com)**

2. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo: `JAY6969-CRY/miniproject`
   - Configure:
     - Name: `stock-predictor-backend`
     - Root Directory: `backend`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables:**
   Add in Render dashboard:
   ```
   ALPHA_VANTAGE_API_KEY=B6285XQINCRH073P
   NEWS_API_KEY=5b78003e86864acda172f59dccee91ca
   GEMINI_API_KEY=AIzaSyCI22SJFVeUAeHBpywp6JcsSwVJ9QMwB8Q
   ```

4. **Deploy!** Render auto-deploys on Git push

#### B. Frontend Deployment (React)

1. **Create Static Site:**
   - Click "New +" → "Static Site"
   - Connect same GitHub repo
   - Configure:
     - Name: `stock-predictor-frontend`
     - Root Directory: `frontend`
     - Build Command: `npm install && npm run build`
     - Publish Directory: `dist`

2. **Environment Variables:**
   ```
   VITE_API_URL=https://stock-predictor-backend.onrender.com
   ```

3. **Deploy!**

---

## Option 2: Vercel (Frontend) + Render (Backend)

### Frontend on Vercel (FREE)

1. **Sign up at [Vercel.com](https://vercel.com)**

2. **Import Project:**
   - Click "Add New" → "Project"
   - Import `JAY6969-CRY/miniproject`
   - Root Directory: `frontend`
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Environment Variables:**
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

4. **Deploy** - Auto-deploys on git push

---

## Option 3: Railway (Full-Stack - FREE $5/month credit)

### Why Railway?
- ✅ $5 free credit monthly
- ✅ Monorepo support
- ✅ Auto-deploy from Git
- ✅ Database included

### Steps:

1. **Sign up at [Railway.app](https://railway.app)**

2. **Deploy Backend:**
   - New Project → Deploy from GitHub
   - Select repository
   - Add service → Select `backend` folder
   - Add environment variables
   - Railway auto-detects Python

3. **Deploy Frontend:**
   - Add service → Select `frontend` folder
   - Railway auto-detects Node.js
   - Add VITE_API_URL env variable

---

## Option 4: Heroku (Paid - $7/month minimum)

### Backend:
```bash
heroku create stock-predictor-backend
heroku config:set ALPHA_VANTAGE_API_KEY=...
heroku config:set NEWS_API_KEY=...
heroku config:set GEMINI_API_KEY=...
git subtree push --prefix backend heroku main
```

### Frontend:
```bash
heroku create stock-predictor-frontend
heroku config:set VITE_API_URL=https://stock-predictor-backend.herokuapp.com
git subtree push --prefix frontend heroku main
```

---

## Option 5: AWS/GCP/Azure (Production Grade)

### AWS:
- EC2: Virtual machine
- S3 + CloudFront: Static frontend
- RDS: Database
- Elastic Beanstalk: Managed platform

### Google Cloud:
- Cloud Run: Containerized apps
- Cloud Storage: Static frontend
- Cloud SQL: Database

### Azure:
- App Service: Web apps
- Blob Storage: Static files
- SQL Database: Database

---

## 📋 Pre-Deployment Checklist

### Backend:
- [x] requirements.txt up to date
- [x] Environment variables documented
- [x] CORS configured for frontend domain
- [ ] Add Procfile (if needed)
- [ ] Configure production settings

### Frontend:
- [x] Environment variables for API URL
- [x] Build command tested locally
- [ ] Update CORS origin in backend
- [ ] Test production build

---

## 🔧 Configuration Files Needed

I'll create these next:
1. `backend/Procfile` - For Heroku/Render
2. `backend/render.yaml` - For Render
3. `frontend/.env.production` - Production env vars
4. `vercel.json` - For Vercel deployment
5. `railway.json` - For Railway deployment

---

## 🌐 Free Hosting Comparison

| Platform | Backend | Frontend | Database | SSL | Custom Domain |
|----------|---------|----------|----------|-----|---------------|
| **Render** | ✅ Free | ✅ Free | ✅ Free | ✅ | ✅ |
| **Vercel** | ❌ | ✅ Free | ❌ | ✅ | ✅ |
| **Railway** | ✅ $5 credit | ✅ $5 credit | ✅ | ✅ | ✅ |
| **Netlify** | ❌ | ✅ Free | ❌ | ✅ | ✅ |

**Recommendation:** **Render** for full-stack (100% free!)

---

## Next Steps

Choose your platform and I'll create the specific configuration files!

Which would you like to deploy to?
1. **Render** (recommended - completely free)
2. **Vercel** (frontend only)
3. **Railway** (full-stack with free credit)
4. **Other**
