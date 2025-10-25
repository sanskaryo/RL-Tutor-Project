# Free Deployment Guide for JEE RL Tutor

## 🚀 Recommended Free Deployment Stack

### Best Option: Vercel (Frontend) + Render (Backend)

This is the easiest and most reliable free deployment:

---

## Option 1: Vercel + Render (Recommended)

### Part 1: Deploy Backend to Render.com

**Why Render?**
- Free tier with 750 hours/month
- Auto-deploys from Git
- Built-in PostgreSQL (or keep SQLite)
- Easy environment variables

**Steps:**

1. **Prepare Backend for Deployment**
   
   Create `render.yaml` in project root (already created below)

2. **Sign up at Render.com**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `jee-rl-tutor-backend`
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan**: Free

4. **Set Environment Variables** (in Render dashboard):
   ```
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DATABASE_URL=sqlite:///./rl_tutor.db
   FRONTEND_URL=https://your-vercel-app.vercel.app
   ```

5. **Deploy**: Click "Create Web Service"
   - Your backend URL will be: `https://jee-rl-tutor-backend.onrender.com`

### Part 2: Deploy Frontend to Vercel

**Why Vercel?**
- Built by Next.js creators
- Zero-config deployment
- Auto HTTPS
- Global CDN

**Steps:**

1. **Sign up at Vercel.com**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Next.js
     - **Root Directory**: `./` (leave as root)
     - **Build Command**: `npm run build`
     - **Output Directory**: `.next`

3. **Set Environment Variable**:
   ```
   NEXT_PUBLIC_API_URL=https://jee-rl-tutor-backend.onrender.com/api/v1
   ```

4. **Deploy**: Click "Deploy"
   - Your frontend URL will be: `https://jee-rl-tutor.vercel.app`

5. **Update Backend CORS**:
   - Go back to Render dashboard
   - Update `FRONTEND_URL` env variable to your Vercel URL
   - Redeploy backend

---

## Option 2: Railway.app (Full Stack)

**Why Railway?**
- Deploy both frontend + backend together
- Free $5 credit/month
- Very simple setup

**Steps:**

1. **Sign up at Railway.app**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Deploy Backend**:
   - Railway auto-detects Python
   - Set environment variables:
     ```
     SECRET_KEY=your-secret-key
     DATABASE_URL=sqlite:///./rl_tutor.db
     PORT=8002
     ```
   - Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

4. **Deploy Frontend**:
   - Add new service from same repo
   - Railway auto-detects Next.js
   - Set environment variable:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api/v1
     ```

---

## Option 3: Fly.io (Full Stack)

**Why Fly.io?**
- Free tier: 3 shared VMs
- Global deployment
- Good for full-stack apps

**Setup files already created below**

**Steps:**

1. **Install Fly CLI**:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up**:
   ```bash
   fly auth signup
   ```

3. **Deploy Backend**:
   ```bash
   cd backend
   fly launch --name jee-rl-tutor-backend
   fly deploy
   ```

4. **Deploy Frontend**:
   ```bash
   cd ..
   fly launch --name jee-rl-tutor-frontend
   fly deploy
   ```

---

## Option 4: Heroku (Classic)

**Note**: Heroku removed free tier, but has $5/month Eco plan

---

## Database Considerations

### Current: SQLite (File-based)
- ✅ Works on Render/Railway/Fly
- ⚠️ Data lost on redeploy (ephemeral storage)
- ⚠️ Not suitable for production

### Better: PostgreSQL (Free tiers available)

**Free PostgreSQL Options:**
1. **Neon.tech** (Best for free tier)
   - 3GB storage free
   - Auto-scaling
   - https://neon.tech

2. **Supabase**
   - 500MB free
   - Includes auth & storage
   - https://supabase.com

3. **Railway PostgreSQL**
   - Built-in with Railway
   - 1GB free

**To migrate to PostgreSQL:**

1. Install adapter:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `backend/requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```

3. Update `DATABASE_URL` environment variable:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

---

## 📋 Pre-Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create `.gitignore` (exclude `node_modules`, `venv`, `.env`, `rl_tutor.db`)
- [ ] Update `SECRET_KEY` to secure random value
- [ ] Test locally with `start.bat`
- [ ] Prepare environment variables
- [ ] Choose deployment platform
- [ ] Deploy backend first
- [ ] Note backend URL
- [ ] Deploy frontend with backend URL
- [ ] Test deployed app

---

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` to random secure value (use password generator)
- [ ] Update CORS origins to your actual domain
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (automatic on Vercel/Render)
- [ ] Set `ACCESS_TOKEN_EXPIRE_MINUTES` appropriately
- [ ] Review API rate limits

---

## 💰 Cost Comparison (Free Tiers)

| Platform | Frontend | Backend | Database | Limits |
|----------|----------|---------|----------|--------|
| **Vercel + Render** | ✅ Free | ✅ 750hrs/mo | SQLite included | Best combo |
| **Railway** | ✅ Free | ✅ Free | ✅ 1GB free | $5 credit/mo |
| **Fly.io** | ✅ Free | ✅ Free | Shared VM | 3 VMs free |
| **Netlify + Render** | ✅ Free | ✅ 750hrs/mo | SQLite included | Alternative |

---

## 🎯 Recommended for You

**Start with: Vercel (Frontend) + Render (Backend)**

**Why?**
- ✅ Easiest setup
- ✅ Most generous free tier
- ✅ Auto-deployments from Git
- ✅ Great documentation
- ✅ No credit card required initially
- ✅ Perfect for student projects/portfolio

**Later upgrade to:**
- PostgreSQL database (Neon.tech free tier)
- Custom domain (free with Vercel)
- More dynos if traffic grows

---

## 📦 What Gets Deployed

**Backend (Render/Railway/Fly):**
- FastAPI application
- RL agent & student model
- SQLite database (or PostgreSQL)
- 39 JEE questions pre-loaded
- API endpoints for frontend

**Frontend (Vercel):**
- Next.js application
- All React components
- Sidebar navigation
- Dashboard, Analytics, Learn pages
- Static assets

---

## 🚨 Common Issues & Solutions

### Issue: Backend takes 30s to wake up
**Solution**: Free tier servers sleep after inactivity. First request wakes them up.
- Render/Railway/Fly all have this
- Use UptimeRobot.com to ping every 5 minutes (keeps alive)

### Issue: Database resets on redeploy
**Solution**: 
- Migrate to PostgreSQL (persistent storage)
- Or accept for demo purposes

### Issue: CORS errors
**Solution**: Update backend `FRONTEND_URL` to exact Vercel URL (no trailing slash)

### Issue: Environment variables not working
**Solution**: 
- Vercel: Prefix with `NEXT_PUBLIC_` for browser access
- Render: Set in dashboard under "Environment"
- Redeploy after changing env vars

---

## 📞 Support

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Fly.io Docs**: https://fly.io/docs

---

## 🎓 Next Steps After Deployment

1. Test all features on deployed site
2. Add custom domain (free on Vercel)
3. Set up monitoring (Vercel Analytics free)
4. Add more JEE questions
5. Share with friends/teachers
6. Add to portfolio/resume

---

Good luck with your deployment! 🚀
