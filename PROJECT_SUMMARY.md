# RL-Based Personalized Educational Tutor
## University Mini-Project - Complete System

---

## 🎯 Project Overview

A full-stack intelligent tutoring system that uses **Reinforcement Learning (Q-Learning)** to personalize educational content delivery based on individual student performance and learning patterns.

### Tech Stack
- **Frontend**: Next.js 16 + React 19 + TypeScript + Tailwind CSS v4 + Framer Motion
- **Backend**: FastAPI + Python + SQLAlchemy + Uvicorn
- **ML/RL**: NumPy + Pandas + Scikit-learn + Custom Q-Learning Agent
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **UI Components**: Aceternity UI (custom animations)

---

## 📁 Project Structure

```
mini_project/
├── app/                        # Next.js Frontend
│   ├── components/ui/         # Aceternity UI components
│   │   ├── spotlight.tsx
│   │   ├── text-generate-effect.tsx
│   │   ├── bento-grid.tsx
│   │   ├── background-gradient.tsx
│   │   ├── moving-border.tsx
│   │   └── ...
│   ├── lib/utils.ts           # Utility functions
│   ├── page.tsx               # Landing page
│   ├── layout.tsx
│   └── globals.css
│
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── session.py     # Learning sessions
│   │   │   └── analytics.py   # Analytics & dashboard
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/            # Data models
│   │   │   ├── models.py      # SQLAlchemy models
│   │   │   └── schemas.py     # Pydantic schemas
│   │   └── services/          # Business logic
│   │       ├── rl_agent.py    # Q-Learning agent
│   │       └── student_model.py
│   ├── main.py                # FastAPI app
│   ├── seed_db.py            # Database seeding
│   ├── test_api.py           # API testing script
│   ├── requirements.txt       # Python dependencies
│   └── README.md
│
├── INTEGRATION.md             # Integration guide
├── TODO.txt                   # Project checklist
├── package.json
├── tsconfig.json
└── README.md                  # This file
```

---

## ✨ Features Implemented

### Frontend (Next.js)
✅ Modern landing page with dark theme
✅ 7 sections (Hero, About, Architecture, Features, Team, Contact, Footer)
✅ Animated components (Spotlight, Text Generation, Hover Effects, Gradient Borders)
✅ Bento Grid layout for system architecture
✅ Responsive design
✅ Aceternity UI integration

### Backend (FastAPI)
✅ RESTful API with FastAPI
✅ JWT-based authentication
✅ User registration & login
✅ Learning session management
✅ Real-time RL content recommendation
✅ Student knowledge tracking
✅ Performance analytics
✅ Dashboard endpoint
✅ CORS enabled for Next.js

### RL Agent
✅ Q-Learning algorithm implementation
✅ Epsilon-greedy exploration (ε = 0.1)
✅ State space: Student knowledge vectors
✅ Action space: Content selection
✅ Reward function: Correctness + Time + Difficulty matching
✅ Q-table persistence (save/load)
✅ Adaptive difficulty adjustment
✅ Real-time learning from interactions

### Database
✅ 5 tables: Students, Content, LearningSession, StudentKnowledge, PerformanceMetrics
✅ 17 seeded questions (Algebra, Calculus, Geometry, Statistics)
✅ Automatic initialization
✅ Session tracking with RL data

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.8+
- npm or yarn

### Frontend Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on: **http://localhost:3000**

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_db.py

# Run server
uvicorn main:app --reload
```

Backend runs on: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

---

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new student
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current student profile

### Learning Sessions
- `POST /api/v1/session/start` - Start session, get recommended content
- `POST /api/v1/session/answer` - Submit answer, get feedback
- `GET /api/v1/session/progress` - Get learning progress

### Analytics
- `GET /api/v1/analytics/dashboard` - Complete dashboard data
- `GET /api/v1/analytics/rl-stats` - RL agent statistics
- `GET /api/v1/analytics/performance-chart` - Performance data

---

## 🧠 RL Agent Details

### Q-Learning Implementation
- **Algorithm**: Q-Learning with epsilon-greedy exploration
- **State**: 4D vector (algebra, calculus, geometry, statistics scores)
- **Actions**: Select content from available pool
- **Reward**: 
  - +1.0 for correct answer
  - -0.5 for wrong answer
  - +0.2 bonus for quick correct answers
  - +0.3 bonus for appropriate difficulty match

### Learning Process
1. Student answers question
2. System calculates reward based on correctness, time, difficulty
3. RL agent updates Q-table: `Q(s,a) = Q(s,a) + α(r + γ max Q(s',a') - Q(s,a))`
4. Agent recommends next content based on updated policy
5. Student knowledge state updated
6. Difficulty adapted based on performance

---

## 📊 Database Schema

### Students
- id, email, username, hashed_password, full_name, created_at

### Content
- id, title, description, topic, difficulty, content_type, question_text, 
  correct_answer, options, explanation, tags

### LearningSession
- id, student_id, content_id, student_answer, is_correct, time_spent,
  state_before, action_taken, reward, state_after

### StudentKnowledge
- id, student_id, algebra_score, calculus_score, geometry_score, 
  statistics_score, total_attempts, correct_answers, accuracy_rate,
  preferred_difficulty, learning_style

### PerformanceMetrics
- id, student_id, date, questions_attempted, questions_correct,
  average_difficulty, total_time_spent, skill_improvement

---

## 🧪 Testing

### Test Backend API
```bash
cd backend
python test_api.py
```

### Test Credentials
- Username: `testuser`
- Password: `test123`
- Email: `test@example.com`

### Manual Testing
Visit: http://localhost:8000/docs for interactive API testing (Swagger UI)

---

## 📈 Current Progress

### Completed ✅
- [x] Next.js frontend with landing page
- [x] Aceternity UI components
- [x] FastAPI backend server
- [x] Database models & schemas
- [x] Q-Learning agent implementation
- [x] Authentication system (JWT)
- [x] Learning session endpoints
- [x] Student knowledge tracking
- [x] Analytics dashboard
- [x] Database seeding
- [x] CORS configuration
- [x] Backend running successfully

### In Progress 🚧
- [ ] Frontend-backend integration
- [ ] Login/Register pages
- [ ] Student dashboard UI
- [ ] Learning session interface
- [ ] Progress visualization

### Next Steps ⏭️
1. Create API client in Next.js
2. Build authentication pages
3. Create dashboard page
4. Build quiz/learning interface
5. Add charts for analytics
6. Implement RL visualization
7. Deploy to production

---

## 🎓 University Project Information

**Course**: Reinforcement Learning / AI Systems
**Title**: RL-Based Personalized Educational Tutor
**Objective**: Demonstrate adaptive learning using Q-Learning algorithm
**Key Innovation**: Real-time content recommendation based on student performance

### Project Highlights
- ✨ Real reinforcement learning implementation (not simulated)
- ✨ Practical application of Q-Learning
- ✨ Full-stack development
- ✨ Modern UI/UX with animations
- ✨ RESTful API design
- ✨ Scalable architecture
- ✨ Professional-grade code quality

---

## 📚 Documentation

- **Integration Guide**: `INTEGRATION.md`
- **Backend README**: `backend/README.md`
- **API Documentation**: http://localhost:8000/docs (when running)
- **TODO List**: `TODO.txt`

---

## 🛠️ Development Commands

### Frontend
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Backend
```bash
uvicorn main:app --reload          # Start with hot reload
python seed_db.py                  # Seed database
python test_api.py                 # Test API endpoints
```

---

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

---

## 👥 Team

- **Dr. Sarah Chen** - AI Research Lead
- **Alex Kumar** - Full-Stack Developer
- **Maya Patel** - ML Engineer
- **James Wilson** - UX Designer

---

## 📝 License

This is a university mini-project for educational purposes.

---

## 🎉 Acknowledgments

- FastAPI for excellent documentation
- Next.js for amazing developer experience
- Aceternity UI for beautiful components
- University for the project opportunity

---

**Status**: ✅ Backend Complete & Running | ⏳ Frontend Integration In Progress
**Last Updated**: October 22, 2025
