# JEE RL Tutor - Startup Guide

## Quick Start

### Windows
Simply double-click `start.bat` or run:
```bash
start.bat
```

This will open two separate terminal windows:
- **Backend**: FastAPI server on http://localhost:8002
- **Frontend**: Next.js app on http://localhost:3000

### Linux/Mac (Git Bash on Windows)
```bash
chmod +x start.sh  # First time only
./start.sh
```

Press `Ctrl+C` to stop all services.

## Manual Startup

### Backend (Terminal 1)
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8002
```

### Frontend (Terminal 2)
```bash
npm run dev
```

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8002
- **API Documentation**: http://localhost:8002/docs
- **Interactive API**: http://localhost:8002/redoc

## First Time Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Setup
```bash
npm install
```

### Database Setup
The SQLite database (`rl_tutor.db`) should already be populated with 39 JEE questions across 13 topics:

**Physics**: mechanics, electromagnetism, optics, modern_physics  
**Chemistry**: physical_chemistry, organic_chemistry, inorganic_chemistry  
**Mathematics**: algebra, calculus, coordinate_geometry, trigonometry, vectors, probability

If you need to repopulate:
```bash
cd backend
python populate_jee_questions.py
```

## Troubleshooting

### Port Already in Use
If port 8002 or 3000 is already in use:

**Backend**: Edit `start.bat` or `start.sh` to use a different port
```bash
python -m uvicorn app.main:app --reload --port 8003
```

**Frontend**: It will automatically try port 3001, 3002, etc.

### Module Not Found
Make sure dependencies are installed:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
npm install
```

### Database Issues
If you encounter database errors, check that `backend/rl_tutor.db` exists and has the correct schema. You can reset it by deleting the file and running the populate script again.

## Development

- **Backend**: FastAPI with auto-reload enabled (changes reflect automatically)
- **Frontend**: Next.js with Turbopack (hot module replacement)
- **Database**: SQLite (file-based, no server needed)

## Project Structure
```
mini_project/
├── start.sh              # Linux/Mac startup script
├── start.bat             # Windows startup script
├── backend/
│   ├── app/
│   │   ├── main.py      # FastAPI application
│   │   ├── api/         # API endpoints
│   │   ├── models/      # Database models
│   │   └── services/    # Business logic
│   ├── rl_tutor.db      # SQLite database
│   └── requirements.txt
├── app/                  # Next.js pages
├── components/           # React components
└── package.json
```

## Support

For issues or questions, check the API documentation at http://localhost:8002/docs when the backend is running.
