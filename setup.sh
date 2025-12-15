#!/bin/bash

# Quick Start Script for AI Resume Coach
# This script sets up both backend and frontend for local development

set -e  # Exit on error

echo "🚀 AI Resume Coach - Quick Start Setup"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js found${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm found${NC}"

echo ""
echo "🔧 Setting up backend..."
echo "----------------------"

# Backend setup
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  .env file not found. Let's create one.${NC}"
    echo ""
    
    # Copy example
    cp ../.env.example .env
    
    echo "Please configure the following in backend/.env:"
    echo "1. DATABASE_URL - Your PostgreSQL connection string"
    echo "2. SECRET_KEY - Generate with: openssl rand -hex 32"
    echo "3. HUGGINGFACE_API_KEY - Get from https://huggingface.co/settings/tokens"
    echo ""
    echo -e "${YELLOW}Press Enter after configuring .env file...${NC}"
    read
fi

echo -e "${GREEN}✅ Backend setup complete${NC}"
cd ..

echo ""
echo "🎨 Setting up frontend..."
echo "----------------------"

# Frontend setup
cd frontend

# Install dependencies
echo "Installing npm dependencies..."
npm install --silent

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created frontend/.env with default values"
fi

echo -e "${GREEN}✅ Frontend setup complete${NC}"
cd ..

echo ""
echo "======================================"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "======================================"
echo ""
echo "To start development:"
echo ""
echo "1️⃣  Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo "   → http://localhost:8000"
echo ""
echo "2️⃣  Start Frontend (in new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo "   → http://localhost:5173"
echo ""
echo "📚 Documentation:"
echo "   → README.md - Overview & setup"
echo "   → DEPLOYMENT.md - Production deployment"
echo "   → SECURITY.md - Security features"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
