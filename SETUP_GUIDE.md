# Quick Setup & Troubleshooting Guide

## Current Configuration

**Backend**: Port 8001 (http://localhost:8001)  
**Frontend**: Port 3000 (http://localhost:3000)  
**Status**: CORS issues resolved, rate limiting disabled for development

---

## Quick Start

### Option 1: Use Startup Script (Windows)
```bash
# Double-click start.bat or run:
start.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

---

## Access Points

- **Landing Page**: http://localhost:3000
- **Register**: http://localhost:3000/register
- **Login**: http://localhost:3000/login
- **Demo**: http://localhost:3000/demo
- **RL Visualization**: http://localhost:3000/rl-viz
- **API Documentation**: http://localhost:8001/docs

---

## Known Issues & Solutions

### Issue 1: CORS Errors
**Symptom**: "Cross-Origin Request Blocked" in browser console

**Solution**:
- Backend configured with `allow_origins=["*"]` and `allow_credentials=False`
- Frontend uses `http://localhost:8001/api/v1` 
- Verify in `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1`

### Issue 2: Port 8000 Conflicts
**Symptom**: "Address already in use" error

**Solution**:
- Backend now uses port 8001 instead
- Update all references from 8000 → 8001
- Check `.env.local` has correct port

### Issue 3: Rate Limiting Blocks Registration
**Symptom**: "Rate limit exceeded: 5 per 1 hour"

**Solution**:
- Rate limiter temporarily disabled in `backend/app/api/auth.py`
- Line 25: `# @limiter.limit("100/hour")` (commented out)
- For production, re-enable with higher limits

### Issue 4: Cannot Create Account
**Symptom**: Registration fails silently or with network error

**Steps to Debug**:
1. Open browser console (F12)
2. Check for CORS errors
3. Verify backend is running: http://localhost:8001/health
4. Check API endpoint: http://localhost:8001/docs
5. Test direct registration:
   ```bash
   curl -X POST http://localhost:8001/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","username":"testuser","password":"pass123"}'
   ```

### Issue 5: Frontend Not Updating
**Symptom**: Changes to code don't appear

**Solution**:
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

---

## Environment Files

### `.env.local` (Frontend)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_API_BASE=http://localhost:8001
```

### `backend/.env` (Backend)
```bash
DATABASE_URL=sqlite:///./rl_tutor.db
SECRET_KEY=dev-secret-key-change-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:3000
PORT=8001
HOST=0.0.0.0
```

---

## Testing Registration

1. **Open Frontend**: http://localhost:3000/register
2. **Fill Form**:
   - Email: `test@example.com`
   - Username: `testuser123` (unique)
   - Password: `password123`
3. **Check Console**: Press F12 to see any errors
4. **Expected Behavior**: Redirect to `/dashboard` on success

---

## API Test (Direct)

Test backend directly with curl:

```bash
# Health check
curl http://localhost:8001/health

# Register
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"new@test.com","username":"newuser","password":"test123"}'

# Expected: {"access_token":"...","token_type":"bearer"}
```

---

## Reset Everything

If things are completely broken:

```bash
# Stop all processes
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# Clear caches
rm -rf .next
rm -rf backend/__pycache__
rm -rf backend/app/__pycache__

# Reset database (optional - loses all data)
rm backend/rl_tutor.db
cd backend && python seed_db.py && cd ..

# Restart
start.bat
```

---

## Still Having Issues?

1. Check that both servers are running:
   - Backend: http://localhost:8001/health should return `{"status":"healthy"}`
   - Frontend: http://localhost:3000 should show landing page

2. Check browser console (F12) for specific error messages

3. Check backend terminal for error logs

4. Verify file contents:
   - `app/api/client.ts` line 6: `'http://localhost:8001/api/v1'`
   - `backend/main.py` line 29: `allow_origins=["*"]`
   - `backend/main.py` line 30: `allow_credentials=False`

---

## Production Deployment

Before deploying:

1. **Re-enable rate limiting** in `backend/app/api/auth.py`
2. **Change SECRET_KEY** in `backend/.env`
3. **Update CORS origins** to specific domains
4. **Set `allow_credentials=True`** for production
5. **Use PostgreSQL** instead of SQLite
6. **Set environment variables** on hosting platform

See `DEPLOYMENT.md` for full instructions.

---

**Last Updated**: October 22, 2025  
**Backend Port**: 8001  
**Frontend Port**: 3000  
**Status**: Development Ready ⚠️ (CORS configured for testing)
