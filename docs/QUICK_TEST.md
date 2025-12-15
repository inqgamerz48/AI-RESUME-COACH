# QUICK TESTING GUIDE - Local Browser Testing

## Step 1: Get Hugging Face API Key (FREE)

1. Go to: https://huggingface.co/settings/tokens
2. Sign up/Login (free)
3. Click "New token"
4. Name: "resume-coach"
5. Type: "Read"
6. Copy the token (starts with hf_...)

## Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy command below)
```

Create `backend/.env` with these contents:
```
# For local testing - using SQLite instead of PostgreSQL
DATABASE_URL=sqlite:///./test.db

# Generate secret key (copy result of this command):
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-paste-here-min-32-chars

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Your Hugging Face API key from Step 1
HUGGINGFACE_API_KEY=hf_paste_your_key_here

FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development
RATE_LIMIT_PER_MINUTE=10
```

## Step 3: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
```

## Step 4: Run the Application

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```
→ Backend runs at http://localhost:8000

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```
→ Frontend runs at http://localhost:5173

## Step 5: Test in Browser

Open: http://localhost:5173

Try:
1. Click "Get Started" → Register
2. Login with your credentials
3. Go to Dashboard
4. Try AI resume improvement
5. Check pricing page
6. Export PDF

---

**IMPORTANT**: You MUST have a Hugging Face API key for AI features to work!
