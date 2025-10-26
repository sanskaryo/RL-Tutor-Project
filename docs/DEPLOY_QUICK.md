# Quick Deployment Steps for JEE RL Tutor

## 🚀 Fastest Way to Deploy (5 minutes)

### Step 1: Push to GitHub (if not already done)

```bash
git init
git add .
git commit -m "Initial commit - JEE RL Tutor"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/jee-rl-tutor.git
git push -u origin main
```

### Step 2: Deploy Backend to Render

1. Go to https://render.com (sign up with GitHub)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Fill in:
   - **Name**: `jee-rl-tutor-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

5. Add Environment Variables:
   ```
   SECRET_KEY = your-random-secret-key-min-32-chars
   DATABASE_URL = sqlite:///./rl_tutor.db
   ```

6. Click **"Create Web Service"**
7. Copy your backend URL: `https://jee-rl-tutor-backend.onrender.com`

### Step 3: Deploy Frontend to Vercel

1. Go to https://vercel.com (sign up with GitHub)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Settings:
   - **Framework**: Next.js (auto-detected)
   - **Root Directory**: `./`
   - **Build Command**: `npm run build` (auto)
   - **Output Directory**: `.next` (auto)

5. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL = https://jee-rl-tutor-backend.onrender.com/api/v1
   ```

6. Click **"Deploy"**
7. Wait 2-3 minutes ⏳

### Step 4: Update Backend CORS

1. Go back to Render dashboard
2. Open your backend service
3. Add Environment Variable:
   ```
   FRONTEND_URL = https://your-app-name.vercel.app
   ```
4. Click **"Save Changes"** (auto-redeploys)

### ✅ Done! Your app is live at:
- **Frontend**: https://your-app-name.vercel.app
- **Backend**: https://jee-rl-tutor-backend.onrender.com
- **API Docs**: https://jee-rl-tutor-backend.onrender.com/docs

---

## 🎯 Important Notes

⚠️ **First Load**: Backend takes 30-60 seconds to wake up (free tier sleeps after inactivity)

⚠️ **Database**: SQLite data persists but may reset on redeploy. For production, use PostgreSQL.

✅ **Free Forever**: Both Vercel and Render have generous free tiers

✅ **Auto Deploy**: Push to GitHub = auto deploy to both platforms

---

## 🔧 Troubleshooting

### Frontend can't connect to backend
- Check `NEXT_PUBLIC_API_URL` is correct
- Ensure backend `FRONTEND_URL` matches Vercel URL
- Check browser console for CORS errors

### Backend shows errors
- Check Render logs: Dashboard → Service → Logs
- Verify environment variables are set
- Ensure `requirements.txt` has all dependencies

### Database is empty
- Backend needs to run `populate_jee_questions.py` once
- Or use Render Shell to populate manually

---

## 📱 Share Your App

Once deployed, share:
- Live URL: `https://your-app.vercel.app`
- GitHub repo: `https://github.com/username/jee-rl-tutor`
- Add to resume/portfolio!

---

## 💡 Want Better Performance?

**Upgrade Options:**
- Railway.app: $5/month (faster, no sleep)
- Render Starter: $7/month (no sleep, more resources)
- Add PostgreSQL: Neon.tech (free 3GB)
- Custom domain: Free with Vercel

---

Ready to deploy? Start with Step 1! 🚀
