# Port Configuration Guide

## Quick Start (Default Ports)

### Backend (Port 8002)
```bash
cd backend
source venv/Scripts/activate  # or venv\Scripts\activate on Windows CMD
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### Frontend (Port 3000)
```bash
cd mini_project
npm run dev
```

---

## What if Port 8002 is Blocked?

### Option 1: Find and Kill Process on Port 8002
```bash
# Windows (Git Bash)
netstat -ano | grep :8002
taskkill /PID <PID> /F

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8002).OwningProcess | Stop-Process -Force
```

### Option 2: Use a Different Port

If port 8002 is truly blocked, follow these steps:

#### Step 1: Start Backend on Different Port
```bash
cd backend
source venv/Scripts/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```
*(Change 8003 to any available port)*

#### Step 2: Update `.env.local`
Edit `mini_project/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8003/api/v1
NEXT_PUBLIC_API_BASE=http://localhost:8003
```
*(Change 8003 to match your backend port)*

#### Step 3: Restart Frontend
```bash
# Press Ctrl+C to stop frontend
npm run dev
```

---

## Common Port Issues

### Backend Port Conflicts
**Symptom**: `Error: Address already in use`
**Solution**: 
- Use a different port (8003, 8004, etc.)
- Update `.env.local` to match
- Restart frontend

### Frontend Port Conflicts
**Symptom**: Next.js says "Port 3000 is already in use"
**Solution**: 
- Next.js will automatically try 3001, 3002, etc.
- Just press `Y` when prompted
- Frontend will work on any port - backend URL is what matters

---

## Checking What's Running

### Check if Backend is Running
```bash
curl http://localhost:8002/health
# Should return: {"status":"healthy"}
```

### Check Current Ports in Use
```bash
# Windows
netstat -ano | grep LISTENING

# Check specific port
netstat -ano | grep :8002
```

---

## Production Deployment

For production, use environment variables:
```bash
# Backend
export PORT=8002
uvicorn main:app --host 0.0.0.0 --port $PORT

# Frontend .env.production
NEXT_PUBLIC_API_URL=https://your-domain.com/api/v1
NEXT_PUBLIC_API_BASE=https://your-domain.com
```

---

## Troubleshooting

### "Failed to fetch" errors in browser
1. Check backend is running: `curl http://localhost:8002/health`
2. Check `.env.local` has correct port
3. Restart frontend after changing `.env.local`
4. Check browser console for actual URL being called

### Database errors
If you see database column errors, delete and recreate:
```bash
cd backend
rm -f rl_tutor.db
# Restart backend - it will recreate the database
```

### "CORS" errors
Backend CORS is configured for all origins in development. If you see CORS errors:
1. Make sure backend is running
2. Check you're using the correct URL in `.env.local`
