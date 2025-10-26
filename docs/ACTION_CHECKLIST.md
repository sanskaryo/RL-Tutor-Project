# 🎯 WHAT YOU NEED TO DO - Action Checklist

## Overview
I've implemented a complete RAG-powered doubt solver for your JEE learning platform. Here's exactly what YOU need to provide and do to make it work.

---

## ✅ CHECKLIST - Complete These Steps

### 1. Get Google Gemini API Key (5 minutes)
- [ ] Go to https://aistudio.google.com/app/apikey
- [ ] Click "Create API Key" (might need to login with Google)
- [ ] Copy the API key (starts with `AIza...`)
- [ ] Save it somewhere safe (you'll add it to .env file)

**Cost**: FREE (60 requests/minute, 1500/day limit)

---

### 2. Setup MongoDB Atlas (10 minutes)
- [ ] Go to https://www.mongodb.com/cloud/atlas
- [ ] Sign up for free account
- [ ] Create new project (name it "JEE-Tutor")
- [ ] Click "Build a Database" → Choose **FREE M0** cluster
- [ ] Choose cloud provider and region (any is fine)
- [ ] Cluster name: "jee-cluster" (or anything you like)
- [ ] Click "Create" (takes 3-5 minutes to provision)

Once cluster is created:
- [ ] Click "Database Access" → Add Database User
  - Username: `jeeadmin` (or anything)
  - Password: Generate secure password (save this!)
  - Database User Privileges: "Atlas admin"
  - Click "Add User"

- [ ] Click "Network Access" → Add IP Address
  - Click "ALLOW ACCESS FROM ANYWHERE"
  - IP Address: `0.0.0.0/0` (auto-filled)
  - Click "Confirm"

- [ ] Go back to "Database" → Click "Connect"
  - Choose "Connect your application"
  - Driver: Python, Version: 3.12 or later
  - Copy the connection string (looks like: `mongodb+srv://jeeadmin:<password>@cluster.mongodb.net/?retryWrites=true&w=majority`)
  - **Replace `<password>` with your actual password**
  - Save this connection string

**Cost**: FREE forever (M0 tier, 512MB storage)

---

### 3. Create Vector Search Index in MongoDB (5 minutes) ⚠️ CRITICAL
- [ ] In MongoDB Atlas, go to your cluster
- [ ] Click "Search" tab (next to "Collections")
- [ ] Click "Create Search Index"
- [ ] Choose "Atlas Vector Search - JSON Editor"
- [ ] Database Name: `jee_tutor`
- [ ] Collection Name: `document_chunks`
- [ ] Index Name: `vector_index`
- [ ] Paste this JSON configuration:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 768,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "metadata.subject"
    },
    {
      "type": "filter",
      "path": "metadata.chapter"
    }
  ]
}
```

- [ ] Click "Next" → "Create Search Index"
- [ ] **IMPORTANT: Wait 5-10 minutes for "Status" to show "Active"**
  - Refresh the page to check status
  - Don't proceed until status is "Active"

---

### 4. Configure Environment Variables (2 minutes)
- [ ] Open `backend/.env.example` in a text editor
- [ ] Save it as `backend/.env` (remove `.example`)
- [ ] Fill in these values:

```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here
MONGODB_URI=mongodb+srv://jeeadmin:your_password@cluster.mongodb.net/?retryWrites=true&w=majority
```

- [ ] Save the file
- [ ] **Double-check**: Make sure `.env` is in `backend/` folder, not project root

---

### 5. Install Python Dependencies (3 minutes)
Open terminal/command prompt:

```bash
cd backend
pip install -r requirements.txt
```

Wait for all packages to install. You should see:
- `google-generativeai`
- `pymongo`
- `pymupdf`
- `tiktoken`
- and others...

If you get errors, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 6. Get JEE Study Material PDFs (10-30 minutes)

You need to download NCERT PDFs. Here's where:

**Option A: Official NCERT Website (Free)**
- [ ] Go to https://ncert.nic.in/textbook.php
- [ ] Download these (minimum):
  - Class 11 Physics (Part 1)
  - Class 11 Chemistry (Part 1)
  - Class 11 Mathematics

**Option B: Quick Links (if you have them)**
- [ ] Use any NCERT PDFs you already have
- [ ] Or get from your coaching materials

**Organize them**:
- [ ] Create folders:
  ```
  backend/data/documents/physics/
  backend/data/documents/chemistry/
  backend/data/documents/math/
  ```
- [ ] Put Physics PDFs in `physics/` folder
- [ ] Put Chemistry PDFs in `chemistry/` folder
- [ ] Put Math PDFs in `math/` folder

**Start with just 1-2 PDFs to test!**

---

### 7. Load Documents into Database (5-15 minutes)

Once you have at least 1 PDF:

```bash
cd backend
python load_documents.py
```

You should see output like:
```
Processing: ncert_class11_physics.pdf
Loaded 200 pages
Created 450 chunks
Embedding chunk 10/450...
...
✅ Completed: ncert_class11_physics.pdf (450 chunks)
🎉 Processing complete!
Total chunks inserted: 450
```

**Time**: ~2-3 minutes per PDF

If you get errors:
- Check `.env` file has correct API key and MongoDB URI
- Ensure MongoDB vector index status is "Active"
- Verify PDF is in correct folder

---

### 8. Start Backend Server (1 minute)

```bash
cd backend
uvicorn main:app --reload --port 8001
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**Keep this terminal open!** The server needs to keep running.

---

### 9. Test the API (2 minutes)

Open a NEW terminal and run:

```bash
curl -X POST "http://localhost:8001/api/v1/doubt/ask" -H "Content-Type: application/json" -d "{\"question\": \"What is Newton's second law?\"}"
```

You should get a JSON response with:
- `answer`: "Newton's second law states..."
- `sources`: Array of source chunks
- `confidence`: 0.85 or similar

If it works: **SUCCESS!** 🎉

If error:
- Check backend terminal for error messages
- Verify MongoDB index is "Active"
- Try: `curl http://localhost:8001/api/v1/doubt/stats` to check data loaded

---

### 10. Start Frontend (2 minutes)

Open ANOTHER terminal:

```bash
# In project root directory
npm install  # If not done already
npm run dev
```

You should see:
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
```

---

### 11. Test the UI (1 minute)

- [ ] Open browser: http://localhost:3000/doubt-solver
- [ ] You should see a chat interface
- [ ] Type: "What is Newton's second law?"
- [ ] Press Enter or click Send
- [ ] Wait 2-3 seconds
- [ ] You should get an answer with sources shown below

**If this works: YOU'RE DONE!** ✅

---

## 🎉 SUCCESS CRITERIA

Your system is working if:
- ✅ Backend server starts without errors
- ✅ Test curl command returns an answer
- ✅ Frontend loads at `/doubt-solver`
- ✅ Chat interface responds to questions
- ✅ Sources are displayed with answers
- ✅ Response time is under 5 seconds

---

## ⚠️ COMMON MISTAKES TO AVOID

1. **Forgot to create vector index** → Most common issue!
   - Must create in MongoDB Atlas UI
   - Must wait for status to be "Active"

2. **Wrong .env location**
   - Must be in `backend/.env`, NOT project root

3. **Didn't replace <password> in MongoDB URI**
   - Copy-paste the connection string
   - Replace `<password>` with actual password

4. **IP not whitelisted in MongoDB**
   - Go to Network Access → Add 0.0.0.0/0

5. **Used wrong MongoDB database/collection names**
   - Database: `jee_tutor`
   - Collection: `document_chunks`
   - Index: `vector_index`

---

## 📊 WHAT I ALREADY DID FOR YOU

I've created ALL the code:
- ✅ 15+ Python files for RAG pipeline
- ✅ API endpoints for doubt solver
- ✅ Frontend chat UI component
- ✅ Document loader script
- ✅ Configuration files
- ✅ 3 comprehensive documentation guides

**You only need to:**
1. Get API keys (Gemini + MongoDB)
2. Configure .env file
3. Download PDF materials
4. Run the loader script

That's it!

---

## 💡 QUICK TROUBLESHOOTING

### "GEMINI_API_KEY not configured"
→ Check `backend/.env` file exists and has the key

### "MongoDB connection failed"
→ Check URI is correct, IP whitelisted (0.0.0.0/0)

### "No relevant context found"
→ Vector index not built yet (wait 5-10 min) OR no data loaded

### "ModuleNotFoundError"
→ Run `pip install -r requirements.txt` in backend folder

### API returns empty answer
→ Check `curl http://localhost:8001/api/v1/doubt/stats` - should show chunks > 0

---

## 📞 NEED HELP?

1. Check backend terminal for error messages
2. Check browser console (F12) for frontend errors
3. Verify MongoDB Atlas:
   - Cluster is running (green status)
   - Vector index is "Active"
   - Database `jee_tutor` exists
4. Review `docs/RAG_SETUP_GUIDE.md` for detailed troubleshooting

---

## 📚 DOCUMENTATION REFERENCES

- **Quick Start**: `docs/QUICKSTART_RAG.md`
- **Detailed Setup**: `docs/RAG_SETUP_GUIDE.md`
- **Implementation Summary**: `docs/IMPLEMENTATION_SUMMARY.md`
- **Full Plan**: `docs/ai-learning-platform-inspiration.md`

---

## ⏱️ TIME ESTIMATE

- Setup (first time): **45-60 minutes**
- Loading 3-5 PDFs: **10-15 minutes**
- Testing: **5 minutes**
- **Total: ~1-1.5 hours**

Once set up, adding new PDFs takes just 2-3 minutes each!

---

**🚀 You're ready to go! Follow the checklist and you'll have a working doubt solver in about an hour.**

**Questions? Everything is documented in the guides I created.**
