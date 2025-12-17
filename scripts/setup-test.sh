#!/bin/bash

echo "🚀 AI Resume Coach - Browser Testing Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Step 1: Setting up Backend Environment${NC}"
echo "---------------------------------------"

cd backend

# Check if .env exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists. Skipping creation.${NC}"
else
    echo "Creating backend/.env file..."
    
    # Generate secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    cat > .env << EOF
# Database - SQLite for local testing
DATABASE_URL=sqlite:///./test.db

# Security
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI - IMPORTANT: Get your FREE key from https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=PASTE_YOUR_KEY_HERE

# CORS
FRONTEND_URL=http://localhost:5173

# Environment
ENVIRONMENT=development

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
EOF

    echo -e "${GREEN}✅ Created backend/.env${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: You need to add your Hugging Face API key!${NC}"
    echo ""
    echo "1. Go to: https://huggingface.co/settings/tokens"
    echo "2. Sign up/Login (FREE)"
    echo "3. Create new token (Read access)"
    echo "4. Copy the token"
    echo "5. Edit backend/.env and replace PASTE_YOUR_KEY_HERE"
    echo ""
    echo -e "${YELLOW}Press Enter after you've added your API key...${NC}"
    read
fi

cd ..

echo ""
echo -e "${BLUE}Step 2: Setting up Frontend Environment${NC}"
echo "---------------------------------------"

cd frontend

if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists. Skipping creation.${NC}"
else
    echo "Creating frontend/.env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
    echo -e "${GREEN}✅ Created frontend/.env${NC}"
fi

cd ..

echo ""
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "=================="
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Start Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2️⃣  Start Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3️⃣  Open Browser:"
echo "   http://localhost:5173"
echo ""
echo -e "${YELLOW}Remember: You NEED a Hugging Face API key for AI features!${NC}"
