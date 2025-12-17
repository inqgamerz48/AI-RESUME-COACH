# Local Development Setup Guide

## Quick Start (Recommended)

### 1. Start Backend

```bash
./start-backend.sh
```

The backend will start at **http://localhost:8000**

### 2. Start Frontend (in a new terminal)

```bash
./start-frontend.sh
```

The frontend will start at **http://localhost:3000**

---

## Manual Setup (If Scripts Don't Work)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make sure .env file exists with required variables
# Edit backend/.env and add:
# - DATABASE_URL
# - SECRET_KEY  
# - OPENROUTER_API_KEY

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run the dev server
npm run dev
```

---

## Environment Variables

### Backend (.env file)

Create or edit `backend/.env`:

```bash
# Database (use Neon or local PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/ai_resume_coach

# Security (generate with: openssl rand -hex 32)
SECRET_KEY=your-super-secret-key-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI - OpenRouter (get from https://openrouter.ai/keys)
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
```

### Frontend (.env.local file)

Create `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Database Setup

### Option 1: Use Neon (Recommended)

1. Go to https://neon.tech
2. Create a free account
3. Create a new project
4. Copy the connection string
5. Add to `backend/.env` as `DATABASE_URL`

### Option 2: Local PostgreSQL

```bash
# Install PostgreSQL (if not installed)
sudo apt install postgresql postgresql-contrib  # Ubuntu/Debian
brew install postgresql  # macOS

# Create database
psql postgres
CREATE DATABASE ai_resume_coach;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_resume_coach TO your_user;
\q

# Update DATABASE_URL in backend/.env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/ai_resume_coach
```

---

## Troubleshooting

### Backend Won't Start

**Error: "No module named 'fastapi'"**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Error: "OPENROUTER_API_KEY field required"**
- Make sure `backend/.env` exists
- Add your OpenRouter API key to the file

**Error: Database connection failed**
- Verify `DATABASE_URL` is correct in `.env`
- Test the PostgreSQL connection

### Frontend Won't Start

**Error: "Cannot find module"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Error: "API connection failed"**
- Make sure backend is running at http://localhost:8000
- Check `frontend/.env.local` has correct API URL

### CORS Errors

The backend is configured to allow all origins in development. If you still get CORS errors:

1. Make sure backend is actually running (check http://localhost:8000/health)
2. Check browser console for exact error
3. Verify `.env.local` has the correct backend URL

---

## Testing the Setup

### 1. Test Backend

Open http://localhost:8000/health in your browser

Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Test API Docs

Open http://localhost:8000/docs

You should see the FastAPI interactive documentation.

### 3. Test Frontend

Open http://localhost:3000

You should see the AI Resume Coach homepage.

### 4. Test Full Flow

1. Register a new account
2. Login
3. Test AI features in Dashboard
4. Test Resume Analyzer

---

## Development Workflow

### Recommended Terminal Setup

**Terminal 1: Backend**
```bash
./start-backend.sh
# or
cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload
```

**Terminal 2: Frontend**
```bash
./start-frontend.sh
# or  
cd frontend && npm run dev
```

**Terminal 3: Git/Commands**
```bash
# Use for git commands, testing, etc.
```

---

## Hot Reload

Both backend and frontend support hot reload:

- **Backend**: Changes to Python files trigger automatic reload
- **Frontend**: Changes to React/Next.js files trigger automatic rebuild

---

## Viewing Logs

### Backend Logs
Uvicorn outputs logs directly to the terminal where it's running.

### Frontend Logs
- Server logs: Terminal where `npm run dev` is running
- Browser logs: Browser DevTools console (F12)

---

## Stopping the Servers

Press `Ctrl+C` in each terminal to stop the servers gracefully.

---

## Database Migrations

Tables are created automatically on backend startup. If you need to reset:

```bash
# In your database client (e.g., psql, pgAdmin, Neon console)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

# Restart backend - tables will be recreated
```

---

## Production vs Development

The app automatically detects the environment based on the `ENVIRONMENT` variable:

- **development**: API docs enabled, detailed errors, CORS allows all
- **production**: API docs disabled, generic errors, CORS restricted

---

## Getting Help

If you encounter issues:

1. Check the error message in terminal
2. Check browser DevTools console (F12)
3. Verify all environment variables are set
4. Check that both backend and frontend are running
5. Review the logs for detailed error information

---

**Happy Coding! 🚀**
