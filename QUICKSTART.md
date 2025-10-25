# Quick Start Guide - RL Educational Tutor

Get the application running in 5 minutes!

## Prerequisites
- Python 3.10+ or Docker
- Node.js 18+ (if not using Docker)

---

## 🚀 Method 1: Quick Local Setup (Recommended for Development)

### Step 1: Start Backend (Terminal 1)
```bash
cd backend

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Seed database with sample questions
python seed_db.py

# Start server
uvicorn main:app --reload
```

✅ Backend running at: **http://localhost:8000**  
📚 API Docs at: **http://localhost:8000/docs**

### Step 2: Start Frontend (Terminal 2)
```bash
cd mini_project

# Install dependencies
npm install

# Create environment file
echo NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 > .env.local

# Start development server
npm run dev
```

✅ Frontend running at: **http://localhost:3000**

### Step 3: Test It!
1. Open http://localhost:3000
2. Click "Get Started" or "Sign Up"
3. Create an account
4. Start learning!

---

## 🐳 Method 2: Docker (Fastest)

### One Command Start
```bash
docker-compose up --build
```

That's it! 🎉

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Stop
```bash
docker-compose down
```

---

## 📝 First Time Usage

### 1. Register a New Account
- Go to http://localhost:3000
- Click "Sign Up"
- Fill in:
  - Email: your@email.com
  - Username: yourname
  - Password: yourpassword
  - Full Name: Your Name

### 2. Explore the Dashboard
After registration, you'll see:
- Your learning statistics
- Knowledge progress by topic
- Topics mastered
- Learning profile

### 3. Start a Learning Session
- Click "Start Learning"
- Choose a topic (Algebra, Calculus, Geometry, Statistics)
- Or let the RL agent pick for you!
- Answer questions
- Get instant feedback
- Watch your progress grow!

### 4. View Analytics
- Click your profile or navigate to `/analytics`
- See your performance over time
- Track accuracy trends
- View RL agent statistics

---

## 🔧 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill process if needed
taskkill /F /PID <pid>        # Windows
kill -9 <pid>                 # Linux/Mac
```

### Frontend build errors
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

### Database errors
```bash
cd backend
# Delete and recreate database
rm -f tutor.db q_table.pkl
python seed_db.py
```

### API connection errors
- Check backend is running on port 8000
- Verify .env.local has correct API URL
- Check browser console for CORS errors
- Restart both frontend and backend

---

## 📊 Default Database

The seeded database includes:
- **17 sample questions** across 4 topics:
  - Algebra (5 questions)
  - Calculus (4 questions)
  - Geometry (4 questions)
  - Statistics (4 questions)
- Difficulty levels 1-5
- Multiple choice options
- Detailed explanations

---

## 🎯 What to Try

1. **Answer questions correctly** → See reward increase
2. **Try different topics** → Watch knowledge state update
3. **Check analytics** → View performance trends
4. **Let RL agent choose** → See personalized recommendations
5. **Multiple sessions** → Track accuracy over time

---

## 🔑 Test Account (After Seeding)

If you want to skip registration for quick testing, you can:
1. Run the integration test to create a test user:
   ```bash
   cd backend
   python test_integration.py
   ```
2. Use the test credentials provided in the output

---

## 📖 Next Steps

- **Read INTEGRATION.md** for API details
- **Check TODO.txt** for project status
- **See DEPLOYMENT.md** for production deployment
- **Review backend/README.md** for RL agent details

---

## 🎉 You're All Set!

The RL Educational Tutor is now running. The reinforcement learning agent will:
- ✅ Track your knowledge state
- ✅ Recommend personalized content
- ✅ Adapt to your learning style
- ✅ Optimize for maximum learning efficiency

Happy Learning! 🚀

---

*Having issues? Check the troubleshooting section or review the full documentation.*
