#!/bin/bash

# AI Resume Coach - Local Development Startup Script

echo "🚀 Starting AI Resume Coach Backend..."
echo ""

# Change to backend directory
cd "$(dirname "$0")/backend"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found in backend/"
    echo "📝 Please create backend/.env with required environment variables"
    echo ""
    echo "Required variables:"
    echo "  - DATABASE_URL"
    echo "  - SECRET_KEY"
    echo "  - OPENROUTER_API_KEY"
    echo ""
    echo "See .env.example for template"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found, creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the server
echo ""
echo "🎯 Starting FastAPI server on http://localhost:8000"
echo "📚 API Docs available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo "─────────────────────────────────────────────────────"

# Start uvicorn
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
