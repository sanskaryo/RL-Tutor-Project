# JEE RL Tutor 🎓

An AI-powered adaptive learning platform for JEE (Joint Entrance Examination) preparation using Reinforcement Learning.

![Next.js](https://img.shields.io/badge/Next.js-16.0-black)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)

## ✨ Features

### 🤖 AI-Powered Learning
- **Reinforcement Learning Agent** adapts to your learning patterns
- **Personalized Question Recommendations** based on your knowledge state
- **Smart Difficulty Adjustment** matches your current skill level

### 📚 JEE Content
- **39 Authentic Questions** from past 10 years JEE papers
- **13 Topics** across Physics, Chemistry, and Mathematics
  - **Physics**: Mechanics, Electromagnetism, Optics, Modern Physics
  - **Chemistry**: Physical, Organic, Inorganic Chemistry
  - **Mathematics**: Algebra, Calculus, Coordinate Geometry, Trigonometry, Vectors, Probability

### 📊 Comprehensive Analytics
- **Real-time Performance Tracking** with interactive charts
- **Knowledge Progress Visualization** across all JEE topics
- **Skill Gap Analysis** identifies weak areas
- **Learning Pace Monitoring** tracks your study patterns

### 🎯 Learning Tools
- **Adaptive Practice** with RL-recommended questions
- **Flashcards System** for quick revision
- **Learning Style Quiz** (VARK assessment)
- **Personalized Study Plans** based on your profile
- **Achievement System** with badges and milestones
- **Skill Tree** visualization of mastery progression

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/jee-rl-tutor.git
   cd jee-rl-tutor
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd ..
   npm install
   ```

4. **Start the Application**
   
   **Windows:**
   ```bash
   start.bat
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8002
   - API Docs: http://localhost:8002/docs

## 🏗️ Architecture

### Backend (FastAPI + Python)
- RESTful API with FastAPI
- SQLite database (39 JEE questions pre-loaded)
- Reinforcement Learning agent (Q-Learning)
- Student knowledge modeling
- JWT authentication

### Frontend (Next.js + TypeScript)
- Modern React with Next.js 16
- TypeScript for type safety
- Tailwind CSS for styling
- Responsive design with collapsible sidebar
- Real-time data visualization

## 📁 Project Structure

```
jee-rl-tutor/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── core/           # Config & database
│   ├── main.py             # Application entry
│   └── requirements.txt    # Python dependencies
│
├── app/                     # Next.js pages (App Router)
│   ├── dashboard/          # Main dashboard
│   ├── learn/              # Practice questions
│   ├── analytics/          # Performance analytics
│   ├── flashcards/         # Flashcard system
│   ├── components/         # React components
│   └── api/                # API client
│
└── public/                  # Static assets
```

## 🎮 How It Works

1. **Student Registration/Login** - Create account and get started
2. **Learning Style Assessment** - Take VARK quiz to identify your learning style
3. **Adaptive Practice** - RL agent recommends questions based on:
   - Current knowledge state across 13 topics
   - Learning style preferences
   - Past performance and difficulty progression
4. **Real-time Feedback** - Get instant feedback and explanations
5. **Progress Tracking** - Monitor improvement with detailed analytics
6. **Continuous Adaptation** - System learns from your responses and adjusts recommendations

## 🔬 RL Agent Details

The Reinforcement Learning agent uses:
- **Q-Learning Algorithm** for content recommendation
- **State Space**: Student knowledge levels across 13 topics
- **Action Space**: Available question IDs to recommend
- **Reward Function**: Based on correctness, difficulty match, and learning efficiency
- **Exploration vs Exploitation**: ε-greedy strategy with decaying exploration rate

## 📊 Database Schema

- **Students**: User accounts and profiles
- **Content**: 39 JEE questions with metadata
- **StudentKnowledge**: Knowledge scores for 13 topics per student
- **Session**: Practice session tracking
- **LearningStyleProfile**: VARK assessment results
- **Achievement**: Student achievements and badges

## 🚀 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

**Recommended Free Deployment:**
- **Frontend**: Vercel (https://vercel.com)
- **Backend**: Render (https://render.com)

Quick deploy:
1. Push code to GitHub
2. Connect Render for backend
3. Connect Vercel for frontend
4. Set environment variables
5. Deploy! 🎉

## 🛠️ Tech Stack

**Frontend:**
- Next.js 16.0
- TypeScript 5.0
- Tailwind CSS
- Lucide Icons
- Recharts for visualizations

**Backend:**
- FastAPI
- SQLAlchemy
- SQLite (PostgreSQL ready)
- Scikit-learn
- NumPy, Pandas

**Authentication:**
- JWT tokens
- Bcrypt password hashing

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more JEE questions
- Improve the RL algorithm
- Enhance UI/UX
- Add new features
- Fix bugs

## 📝 License

MIT License - feel free to use this project for learning or building your own adaptive learning platform!

## 🎓 Academic Context

This project demonstrates:
- Reinforcement Learning applications in education
- Adaptive learning systems
- Full-stack web development
- AI-powered personalization
- Modern web technologies

Perfect for:
- Final year projects
- ML/AI portfolios
- EdTech demonstrations
- Learning Next.js + FastAPI

## 📧 Contact

For questions, suggestions, or collaboration:
- GitHub Issues: [Open an issue](https://github.com/YOUR_USERNAME/jee-rl-tutor/issues)
- Email: your.email@example.com

---

**Built with ❤️ for JEE aspirants**

*Good luck with your preparation! 🚀*
