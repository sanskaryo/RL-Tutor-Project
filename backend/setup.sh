#!/bin/bash
# Setup script for backend

echo "🚀 Setting up RL Educational Tutor Backend..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and set your SECRET_KEY"
fi

# Seed database
echo "🌱 Seeding database..."
python seed_db.py

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the server:"
echo "  1. Activate virtual environment: source venv/bin/activate (or venv\\Scripts\\activate on Windows)"
echo "  2. Run server: uvicorn main:app --reload"
echo "  3. Visit: http://localhost:8000/docs"
echo ""
