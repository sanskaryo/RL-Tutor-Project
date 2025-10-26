# RAG Doubt Solver - Setup Guide

## 🎯 Overview

This guide will help you set up the RAG (Retrieval-Augmented Generation) powered doubt solver feature for the RL-Tutor-Project. This feature allows students to ask questions and get answers grounded in actual JEE study materials.

---

## 📋 Prerequisites

Before starting, you need:

1. **Google Gemini API Key** (for embeddings and LLM)
2. **MongoDB Atlas Account** (free tier works fine)
3. **Python 3.10+** installed
4. **Node.js 18+** installed
5. **JEE Study Material PDFs** (NCERT textbooks, notes, etc.)

---

## 🚀 Step-by-Step Setup

### Step 1: Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key (you'll need it later)
4. **Cost**: Free tier includes 60 requests/minute, 1500 requests/day

### Step 2: Set Up MongoDB Atlas

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for free account
   - Create a new cluster (M0 free tier is sufficient)

2. **Create Database and Collection**
   - Database name: `jee_tutor`
   - Collection name: `document_chunks`

3. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`)
   - Replace `<password>` with your actual password

4. **Create Vector Search Index** (IMPORTANT!)
   - Go to your cluster → "Search" tab
   - Click "Create Search Index"
   - Choose "Atlas Vector Search"
   - Use the following JSON configuration:

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

   - Index name: `vector_index`
   - Collection: `document_chunks`
   - Database: `jee_tutor`
   - Click "Create"
   - **Wait 5-10 minutes** for the index to build

### Step 3: Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# MongoDB Atlas Connection String
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority

# MongoDB Configuration
MONGODB_DB_NAME=jee_tutor
MONGODB_COLLECTION_NAME=document_chunks

# Existing settings (keep these)
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///./rl_tutor.db
FRONTEND_URL=http://localhost:3000
```

**⚠️ IMPORTANT**: Never commit the `.env` file to Git! It's already in `.gitignore`.

### Step 4: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `google-generativeai` (Gemini API)
- `pymongo` (MongoDB driver)
- `pymupdf` (PDF processing)
- `tiktoken` (text chunking)
- Plus all existing dependencies

### Step 5: Load Study Materials into Vector Database

1. **Prepare PDF Files**
   - Place your JEE study materials in `backend/data/documents/`
   - Example structure:
     ```
     backend/data/documents/
     ├── physics/
     │   ├── ncert_class11_physics.pdf
     │   └── ncert_class12_physics.pdf
     ├── chemistry/
     │   └── ncert_class11_chemistry.pdf
     └── math/
         └── ncert_class12_math.pdf
     ```

2. **Run Document Loader Script**

Create a script `backend/load_documents.py`:

```python
"""
Script to load JEE study materials into MongoDB vector database.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from app.services.rag.embedder import GeminiEmbedder
from app.services.rag.chunker import TextChunker
from app.services.rag.document_loader import PDFDocumentLoader
from app.services.rag.retriever import VectorRetriever

load_dotenv()

def load_documents(pdf_dir: str, subject: str):
    """Load all PDFs from a directory."""
    
    # Initialize services
    api_key = os.getenv("GEMINI_API_KEY")
    mongodb_uri = os.getenv("MONGODB_URI")
    
    embedder = GeminiEmbedder(api_key=api_key)
    chunker = TextChunker(chunk_size=500, chunk_overlap=50)
    loader = PDFDocumentLoader()
    retriever = VectorRetriever(mongodb_uri=mongodb_uri)
    
    # Get all PDF files
    pdf_files = list(Path(pdf_dir).glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDFs in {pdf_dir}")
    
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        
        # Load PDF
        doc_data = loader.load_pdf(str(pdf_file))
        
        # Chunk the text
        chunks = chunker.chunk_text(
            doc_data["full_text"],
            metadata={
                "filename": pdf_file.name,
                "subject": subject,
                "source": f"NCERT - {pdf_file.stem}"
            }
        )
        
        print(f"Created {len(chunks)} chunks")
        
        # Generate embeddings and prepare for insertion
        documents_to_insert = []
        for i, chunk in enumerate(chunks):
            print(f"Embedding chunk {i+1}/{len(chunks)}...", end="\r")
            
            embedding = embedder.embed_text(chunk["text"])
            
            doc = {
                "text": chunk["text"],
                "embedding": embedding,
                "metadata": chunk["metadata"],
                "chunk_id": chunk["chunk_id"],
                "token_count": chunk["token_count"]
            }
            documents_to_insert.append(doc)
        
        # Insert into MongoDB
        print(f"\nInserting {len(documents_to_insert)} chunks into MongoDB...")
        retriever.insert_chunks(documents_to_insert)
        print(f"✅ Completed: {pdf_file.name}")
    
    print("\n🎉 All documents loaded successfully!")
    retriever.close()

if __name__ == "__main__":
    # Load physics PDFs
    load_documents("data/documents/physics", "Physics")
    
    # Load chemistry PDFs
    load_documents("data/documents/chemistry", "Chemistry")
    
    # Load math PDFs
    load_documents("data/documents/math", "Mathematics")
```

3. **Run the loader**:
```bash
cd backend
python load_documents.py
```

This will:
- Extract text from PDFs
- Split into chunks (500 tokens each)
- Generate embeddings using Gemini
- Store in MongoDB with vector index

**⏱️ Time estimate**: 5-10 minutes for 3-4 NCERT books

### Step 6: Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8001
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Step 7: Test the API

Open another terminal and test:

```bash
curl -X POST "http://localhost:8001/api/v1/doubt/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is Newton's second law?\", \"subject\": \"Physics\"}"
```

Expected response:
```json
{
  "answer": "Newton's second law states that...",
  "sources": [
    {
      "text": "According to NCERT Class 11 Physics...",
      "subject": "Physics",
      "chapter": "Laws of Motion",
      "relevance_score": 0.92
    }
  ],
  "confidence": 0.89
}
```

### Step 8: Start the Frontend

```bash
# In project root
npm install  # If not already done
npm run dev
```

Navigate to: `http://localhost:3000/doubt-solver`

---

## 🧪 Testing the System

### Test 1: Ask a Simple Question
- Go to http://localhost:3000/doubt-solver
- Ask: "What is Newton's second law?"
- You should get an answer with sources

### Test 2: Subject-Specific Question
- Select "Chemistry" from the dropdown
- Ask: "What is the molecular formula of benzene?"

### Test 3: Check Vector Database Stats
```bash
curl "http://localhost:8001/api/v1/doubt/stats"
```

Expected:
```json
{
  "total_chunks": 1523,
  "subjects": ["Physics", "Chemistry", "Mathematics"],
  "collection_name": "document_chunks"
}
```

---

## 📊 What You Need to Provide

### Required:
1. ✅ **Gemini API Key** - Get from Google AI Studio
2. ✅ **MongoDB Atlas URI** - Create free cluster on MongoDB Atlas
3. ✅ **JEE Study Material PDFs** - NCERT textbooks or coaching notes

### Optional (for better results):
4. Previous year JEE question papers
5. Subject-wise formula sheets
6. Additional reference books

---

## 🎨 Customization Options

### 1. Adjust Chunk Size
In `backend/load_documents.py`:
```python
chunker = TextChunker(
    chunk_size=500,  # Increase for longer context
    chunk_overlap=50  # Increase for better continuity
)
```

### 2. Change Temperature (Creativity)
In API request or modify default in `backend/app/api/doubt_solver.py`:
```python
llm_client = GeminiClient(
    api_key=gemini_api_key,
    temperature=0.3  # Lower = more factual, Higher = more creative
)
```

### 3. Increase Context Limit
In frontend `DoubtSolverChat.tsx`:
```typescript
body: JSON.stringify({
  question: input,
  context_limit: 5,  // Retrieve more chunks
  ...
})
```

---

## 🐛 Troubleshooting

### Problem: "GEMINI_API_KEY not configured"
**Solution**: Make sure `.env` file exists in `backend/` and has the API key

### Problem: "MongoDB connection failed"
**Solution**: 
1. Check MongoDB URI is correct
2. Ensure IP is whitelisted in MongoDB Atlas (use 0.0.0.0/0 for testing)
3. Check username/password in connection string

### Problem: "No relevant context found"
**Solution**:
1. Verify documents were loaded: `curl http://localhost:8001/api/v1/doubt/stats`
2. Check vector index is built in MongoDB Atlas UI
3. Wait a few minutes after creating the index

### Problem: "Vector search not working"
**Solution**:
1. Ensure vector index name is `vector_index`
2. Check index definition has 768 dimensions
3. Verify collection name is `document_chunks`

### Problem: "API responses are slow"
**Solution**:
1. Reduce `context_limit` (default is 3)
2. Use a faster Gemini model: `gemini-1.5-flash`
3. Enable caching (add Redis for production)

---

## 💰 Cost Estimate

### Free Tier Usage (per month):
- **Gemini API**: FREE (60 req/min, 1500 req/day)
- **MongoDB Atlas**: FREE (512MB storage, good for 50-100 PDFs)
- **Total**: $0

### If You Exceed Free Tier:
- Gemini embeddings: $0.0001 per 1K tokens
- Gemini chat: $0.00015 per 1K tokens
- MongoDB Atlas M10: $10/month
- **Estimated for 1000 students**: $20-50/month

---

## 📈 Next Steps

Once the basic doubt solver is working:

1. **Add More Content**:
   - Upload previous year JEE papers
   - Add subject-wise notes
   - Include formula sheets

2. **Implement Study Planner**:
   - Use LLM to generate personalized study schedules
   - See `backend/app/services/llm/prompts.py` for templates

3. **Add Quiz Engine**:
   - Create adaptive quizzes
   - Integrate with RL agent

4. **Monitor Usage**:
   - Track API costs
   - Analyze popular questions
   - Improve responses based on feedback

---

## 🆘 Need Help?

If you encounter issues:

1. Check the logs:
   - Backend: Terminal running `uvicorn`
   - Frontend: Browser console (F12)

2. Verify environment variables:
   ```bash
   cd backend
   python -c "from app.core.config import settings; print(f'API Key: {settings.GEMINI_API_KEY[:10]}...'); print(f'MongoDB: {settings.MONGODB_URI[:20]}...')"
   ```

3. Test components individually:
   - Test embedder: `python -c "from app.services.rag.embedder import GeminiEmbedder; e = GeminiEmbedder('your_key'); print(len(e.embed_text('test')))"`
   - Test MongoDB: `curl http://localhost:8001/api/v1/doubt/stats`

---

## ✅ Checklist

Before going live, ensure:

- [ ] Gemini API key configured in `.env`
- [ ] MongoDB Atlas cluster created
- [ ] Vector search index created and built
- [ ] Study materials loaded into database
- [ ] Backend server starts without errors
- [ ] Frontend doubt solver page loads
- [ ] Test question returns answer with sources
- [ ] API response time < 3 seconds
- [ ] Sources are relevant and accurate

---

**Congratulations! Your RAG-powered doubt solver is now ready! 🎉**

Students can now ask JEE questions and get instant, citation-backed answers.
