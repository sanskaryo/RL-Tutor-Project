# RL-Based Educational Tutor - Backend API

FastAPI backend with Q-Learning agent for personalized educational content recommendation.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment**
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

4. **Initialize and seed database**
```bash
python seed_db.py
```

5. **Run the server**
```bash
uvicorn main:app --reload
```

Server will start at: `http://localhost:8000`
API docs available at: `http://localhost:8000/docs`

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── session.py    # Learning session endpoints
│   │   └── analytics.py  # Analytics endpoints
│   ├── core/             # Core configuration
│   │   ├── config.py     # App settings
│   │   ├── database.py   # Database setup
│   │   └── security.py   # JWT & password handling
│   ├── models/           # Data models
│   │   ├── models.py     # SQLAlchemy models
│   │   └── schemas.py    # Pydantic schemas
│   └── services/         # Business logic
│       ├── rl_agent.py   # Q-Learning agent
│       └── student_model.py  # Student knowledge tracker
├── main.py               # FastAPI app
├── seed_db.py           # Database seeding script
└── requirements.txt     # Python dependencies
```

## 🧠 RL Agent Architecture

### Q-Learning Implementation
- **State Space**: Student knowledge levels (algebra, calculus, geometry, statistics)
- **Action Space**: Content selection (questions with varying difficulty)
- **Reward Function**: 
  - Correctness (+1.0 correct, -0.5 wrong)
  - Time efficiency (bonus for quick correct answers)
  - Difficulty appropriateness (bonus for matching student level)

### Agent Features
- Epsilon-greedy exploration (ε = 0.1)
- Q-table persistence (saves/loads learned policy)
- Adaptive difficulty recommendation
- Real-time learning from student interactions

## 🔐 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new student
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current student profile

### Learning Sessions
- `POST /api/v1/session/start` - Start learning session, get recommended content
- `POST /api/v1/session/answer` - Submit answer, get feedback and next content
- `GET /api/v1/session/progress` - Get learning progress

### Analytics
- `GET /api/v1/analytics/dashboard` - Complete dashboard data
- `GET /api/v1/analytics/rl-stats` - RL agent statistics
- `GET /api/v1/analytics/performance-chart` - Performance data for charts

## 📊 Database Schema

### Tables
- **students**: User accounts and profiles
- **content**: Educational questions and materials
- **learning_sessions**: Interaction records with RL data
- **student_knowledge**: Knowledge state vectors by topic
- **performance_metrics**: Aggregate analytics

## 🧪 Testing

### Test with curl
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"test123"}'

# Start session
curl -X POST http://localhost:8000/api/v1/session/start \
  -H "Content-Type: application/json" \
  -d '{"topic":"algebra"}' \
  -G --data-urlencode "username=testuser"
```

### Interactive API Docs
Visit `http://localhost:8000/docs` for Swagger UI with interactive testing.

## 🔧 Configuration

Edit `.env` file:
```env
DATABASE_URL=sqlite:///./rl_tutor.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:3000
```

### RL Agent Parameters
In `app/core/config.py`:
- `EPSILON`: Exploration rate (default: 0.1)
- `LEARNING_RATE`: Q-learning alpha (default: 0.1)
- `DISCOUNT_FACTOR`: Q-learning gamma (default: 0.95)

## 📈 Features

✅ JWT-based authentication
✅ Q-Learning content recommendation
✅ Real-time knowledge state tracking
✅ Adaptive difficulty adjustment
✅ Performance analytics
✅ RESTful API design
✅ SQLite database (easily switch to PostgreSQL)
✅ CORS enabled for frontend integration

## 🔗 Frontend Integration

The backend is configured for CORS with Next.js frontend on `http://localhost:3000`.

Example frontend API call:
```typescript
const response = await fetch('http://localhost:8000/api/v1/session/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ topic: 'algebra' })
});
const content = await response.json();
```

## 📝 Notes

- SQLite used for development (data stored in `rl_tutor.db`)
- Q-table auto-saves after updates
- All endpoints return JSON
- Passwords are hashed with bcrypt
- JWTs expire after 30 minutes (configurable)

## 🐛 Troubleshooting

**Database locked error**
```bash
# Delete and recreate database
rm rl_tutor.db
python seed_db.py
```

**Module not found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 📚 Next Steps

1. Add more content via `seed_db.py`
2. Integrate with Next.js frontend
3. Add WebSocket support for real-time updates
4. Implement advanced RL algorithms (DQN, PPO)
5. Add content upload interface
6. Deploy to production (Railway, Render, AWS)
