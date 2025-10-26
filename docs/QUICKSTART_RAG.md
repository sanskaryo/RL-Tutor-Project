# Quick Start: RAG Doubt Solver

## TL;DR - Get Started in 10 Minutes

### What You Need (MUST HAVE):

1. **Google Gemini API Key** → [Get it here](https://aistudio.google.com/app/apikey) (FREE, takes 2 min)
2. **MongoDB Atlas Account** → [Sign up here](https://www.mongodb.com/cloud/atlas) (FREE forever)
3. **One JEE PDF** → Any NCERT chapter or notes (to test)

---

## Quick Setup (5 Steps)

### Step 1: Get API Keys (5 minutes)

**Gemini API:**
```
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with "AIza...")
```

**MongoDB Atlas:**
```
1. Go to: https://www.mongodb.com/cloud/atlas
2. Sign up (free account)
3. Create free cluster (M0)
4. Get connection string (Database → Connect → Connect your application)
   Format: mongodb+srv://username:password@cluster.mongodb.net/...
```

### Step 2: Configure Environment (1 minute)

Create `backend/.env`:
```env
GEMINI_API_KEY=AIzaSy...your_key_here
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
```

### Step 3: Create Vector Index in MongoDB (2 minutes)

1. Go to MongoDB Atlas → Your Cluster → Search tab
2. Click "Create Search Index" → Choose "JSON Editor"
3. Paste this:

```json
{
  "name": "vector_index",
  "type": "vectorSearch",
  "fields": [{
    "type": "vector",
    "path": "embedding",
    "numDimensions": 768,
    "similarity": "cosine"
  }]
}
```

4. Database: `jee_tutor`, Collection: `document_chunks`
5. Click "Create" → **Wait 5 minutes for index to build**

### Step 4: Install & Load Data (5 minutes)

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Create directory for PDFs
mkdir -p data/documents/physics

# Put ONE PDF in data/documents/physics/
# (e.g., NCERT Physics Chapter 5.pdf)

# Load it into database
python load_documents.py
```

Expected output:
```
✅ Completed: ncert_physics_ch5.pdf (45 chunks)
🎉 Processing complete!
```

### Step 5: Start & Test (2 minutes)

Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --reload --port 8001
```

Terminal 2 - Test:
```bash
curl -X POST "http://localhost:8001/api/v1/doubt/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is Newton's second law?\"}"
```

You should get a JSON response with the answer!

Terminal 3 - Frontend:
```bash
# In project root
npm install
npm run dev
```

Visit: **http://localhost:3000/doubt-solver**

---

## ✅ Checklist

- [ ] Got Gemini API key
- [ ] Got MongoDB URI
- [ ] Created `.env` file with both keys
- [ ] Created vector index in MongoDB Atlas
- [ ] Waited 5-10 min for index to build
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Put at least 1 PDF in `data/documents/physics/`
- [ ] Ran `python load_documents.py` successfully
- [ ] Backend starts without errors (`uvicorn main:app --reload`)
- [ ] Test API works (curl command)
- [ ] Frontend loads at `/doubt-solver`

---

## 🐛 Common Issues

**"GEMINI_API_KEY not configured"**
→ Check `.env` file exists in `backend/` folder

**"MongoDB connection failed"**
→ In MongoDB Atlas, go to Network Access → Add IP → Use `0.0.0.0/0` (allow all)

**"No relevant context found"**
→ Wait for vector index to finish building (check MongoDB Atlas UI)
→ Run: `curl http://localhost:8001/api/v1/doubt/stats` to verify data loaded

**"Import errors"**
→ Make sure you're in `backend/` directory when running commands

---

## 📝 What to Provide

Here's exactly what I've built and what YOU need to provide:

### ✅ Already Done (I Created):
- All backend code (RAG pipeline, API endpoints)
- All frontend code (chat interface)
- Configuration files
- Documentation

### 🔑 You Must Provide:
1. **Gemini API Key** - Get from Google AI Studio (free)
2. **MongoDB Atlas URI** - Create free cluster (free)
3. **PDF Study Materials** - NCERT books, notes, etc. (you have these)

### 📚 Recommended PDFs to Start With:
- NCERT Class 11 Physics (Chapters 1-8)
- NCERT Class 12 Physics (Chapters 1-8)
- NCERT Class 11 Chemistry (Chapters 1-7)
- NCERT Class 12 Chemistry (Chapters 1-6)
- NCERT Class 11 Math (Chapters 1-8)
- NCERT Class 12 Math (Chapters 1-6)

Download from: [NCERT Official](https://ncert.nic.in/textbook.php)

---

## 🚀 Next Actions

Once basic doubt solver works:

1. **Add more content**: Upload more PDFs (10-20 books recommended)
2. **Test quality**: Ask various JEE questions, verify answers
3. **Customize prompts**: Edit `backend/app/services/llm/prompts.py`
4. **Add to navigation**: Update sidebar to include "Doubt Solver" link

---

## 💡 Tips

- **Start small**: Load 1-2 PDFs first to test
- **Monitor costs**: Check Gemini API usage dashboard
- **Iterate**: Test questions → improve if needed → add more content
- **Backup**: Export MongoDB data periodically

---

## 📞 Support

If stuck, check:
1. Terminal logs (backend server)
2. Browser console (F12)
3. MongoDB Atlas logs

Most common fix: **Wait for vector index to finish building!**

---

**That's it! You now have an AI-powered doubt solver! 🎉**

Ask: "What is Newton's second law?" and see it answer with NCERT citations!
