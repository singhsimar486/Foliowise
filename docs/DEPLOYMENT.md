# Foliowise Deployment Guide

## Stack (All Free)
- **Backend:** Render (Free tier)
- **Database:** Render PostgreSQL (Free tier)
- **Frontend:** Vercel (Free tier)
- **Market Data:** Alpha Vantage (Free tier - 25 req/day)

---

## Step 1: Deploy Backend on Render

1. Go to [render.com](https://render.com) and sign up (use GitHub)
2. Click **New → Blueprint**
3. Connect your `foliowise` repository
4. Render will detect `render.yaml` and create:
   - Web service (foliowise-api)
   - PostgreSQL database (foliowise-db)
5. Click **Apply** and wait for deployment (~5 min)
6. Copy your backend URL: `https://foliowise-api.onrender.com`

### Set Environment Variables
In Render dashboard → foliowise-api → Environment:
- `FRONTEND_URL` → (set after Vercel deploy)
- `ALPHA_VANTAGE_API_KEY` → Get free at [alphavantage.co](https://www.alphavantage.co/support/#api-key)

---

## Step 2: Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) and sign up (use GitHub)
2. Click **Add New → Project**
3. Import your `foliowise` repository
4. Configure:
   - **Framework Preset:** Angular
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist/frontend/browser`
5. Click **Deploy**

---

## Step 3: Connect Frontend to Backend

1. Update `frontend/src/environments/environment.prod.ts` with your Render URL
2. Commit and push - Vercel will auto-redeploy
3. Go to Render dashboard and set `FRONTEND_URL` to your Vercel URL

---

## Verify Deployment

1. Visit your Vercel URL
2. Try registering a new account
3. Check Render logs if issues: Dashboard → foliowise-api → Logs

---

## Free Tier Limits

| Service | Limit |
|---------|-------|
| Render Web | Sleeps after 15 min inactivity |
| Render PostgreSQL | 256 MB storage, expires after 90 days |
| Vercel | 100 GB bandwidth/month |
| Alpha Vantage | 25 API calls/day |

---

## Upgrading Later

When you have paying users:
- Render Starter: $7/mo (no cold starts)
- Render PostgreSQL: $7/mo (persistent, no expiry)
