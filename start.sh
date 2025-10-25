#!/bin/bash

# JEE RL Tutor - Startup Script
# This script starts both backend and frontend services

echo "🚀 Starting JEE RL Tutor..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js not found. Please install Node.js${NC}"
    exit 1
fi

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down services...${NC}"
    kill $(jobs -p) 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo -e "${BLUE}� Starting Backend (FastAPI on port 8002)...${NC}"
cd backend
python -m uvicorn app.main:app --reload --port 8002 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start Frontend
echo -e "${BLUE}🎨 Starting Frontend (Next.js on port 3000)...${NC}"
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}✅ Services started successfully!${NC}"
echo ""
echo "📍 Backend:  http://localhost:8002"
echo "📍 Frontend: http://localhost:3000"
echo "📍 API Docs: http://localhost:8002/docs"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait for both processes
wait
echo ""

# Wait for user to stop
wait
