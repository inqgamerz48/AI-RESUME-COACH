# 🧪 BROWSER TESTING GUIDE - AI Resume Coach

## 📋 Prerequisites Checklist

Before starting, you need:
- [x] Python 3.9+ (you have this ✅)
- [x] Node.js 18+ (you have this ✅)
- [ ] python3-venv (need to install)
- [ ] Hugging Face API Key (FREE - we'll get this)

---

## 🔧 STEP-BY-STEP SETUP

### Step 0: Install Python venv

```bash
sudo apt install python3.10-venv
```

### Step 1: Get Your FREE Hugging Face API Key

1. **Open**: https://huggingface.co/settings/tokens
2. **Sign Up/Login** (completely FREE)
3. **Click**: "New token" button
4. **Name**: "resume-coach"
5. **Type**: Select "Read"
6. **Click**: "Generate token"
7. **Copy**: Your token (starts with `hf_...`)

**Keep this token handy** - you'll need it in Step 3!

---

### Step 2: Setup Backend

```bash
cd /home/inq/Desktop/FRESHER\ RESUME\ MAKER/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies (takes 1-2 minutes)
pip install -r requirements.txt
```

---

### Step 3: Configure Backend Environment

Create a file `backend/.env` with this content:

```bash
# Copy this ENTIRE block and save as backend/.env

DATABASE_URL=sqlite:///./test.db

SECRET_KEY=81536d39dc9b9a170d60c8699a9074f75bbc0076098b10fcbf898c0250535d23

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# PASTE YOUR HUGGING FACE API KEY HERE (from Step 1)
HUGGINGFACE_API_KEY=hf_your_key_here

FRONTEND_URL=http://localhost:5173

ENVIRONMENT=development

RATE_LIMIT_PER_MINUTE=10
```

**IMPORTANT**: Replace `hf_your_key_here` with your actual Hugging Face API key!

---

### Step 4: Setup Frontend

```bash
cd /home/inq/Desktop/FRESHER\ RESUME\ MAKER/frontend

# Install dependencies (takes 1-2 minutes)
npm install
```

Create a file `frontend/.env` with this content:

```bash
VITE_API_URL=http://localhost:8000
```

---

### Step 5: Start Backend (Terminal 1)

Open a terminal and run:

```bash
cd /home/inq/Desktop/FRESHER\ RESUME\ MAKER/backend

# Activate virtual environment
source venv/bin/activate

# Start server
uvicorn app.main:app --reload
```

**You should see**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
✅ Database tables created
```

**Keep this terminal running!**

---

### Step 6: Start Frontend (Terminal 2)

Open a **NEW terminal** and run:

```bash
cd /home/inq/Desktop/FRESHER\ RESUME\ MAKER/frontend

# Start dev server
npm run dev
```

**You should see**:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Keep this terminal running too!**

---

### Step 7: Test in Browser! 🎉

1. **Open your browser** and go to: http://localhost:5173

2. **You should see** the landing page with:
   - "AI Resume Coach" logo
   - "Build Your Dream Resume With AI Assistance"
   - "Get Started Free" button

3. **Test Registration**:
   - Click "Get Started"
   - Enter email: test@example.com
   - Enter password: password123
   - Click "Create Account"

4. **Test AI Features**:
   - You'll be redirected to Dashboard
   - In "AI Resume Improver" section
   - Enter: "Worked on a React project"
   - Click "Improve with AI"
   - **Wait 5-10 seconds** (first AI call takes time)
   - You should see a professional rewrite!

5. **Check Usage Tracking**:
   - Notice the "AI Usage: 1/3" display
   - You can make 2 more AI calls (FREE tier limit)

6. **Try Pricing Page**:
   - Click "Pricing" in navigation
   - See all 3 tiers: FREE, PRO, ULTIMATE

---

## 🎯 What You Can Test

### Working Features ✅
- ✅ User Registration
- ✅ User Login
- ✅ AI Bullet Point Rewriting (3 times on FREE tier)
- ✅ Usage Tracking (shows used/remaining)
- ✅ Tier Limits Enforcement
- ✅ Pricing Page Display
- ✅ Upgrade CTAs (when limit reached)
- ✅ Resume Preview Panel
- ✅ Responsive Design

### Locked Features (PRO/ULTIMATE) 🔒
- 🔒 Project Description Generator (shows lock overlay)
- 🔒 Resume Summary Generator (shows lock overlay)
- 🔒 Advanced Tone Control

---

## 🧪 Testing Checklist

### 1. Authentication ✅
- [ ] Register new user
- [ ] Logout
- [ ] Login again
- [ ] Invalid credentials show error

### 2. AI Features ✅
- [ ] Rewrite bullet point (1st call)
- [ ] Rewrite bullet point (2nd call)
- [ ] Rewrite bullet point (3rd call)
- [ ] 4th call shows "limit reached" error
- [ ] Upgrade modal appears

### 3. Tier System ✅
- [ ] Usage counter updates after each AI call
- [ ] Locked features show overlay
- [ ] Click on locked feature shows upgrade modal

### 4. UI/UX ✅
- [ ] Navigation works
- [ ] Buttons respond to clicks
- [ ] Loading states appear
- [ ] Error messages display
- [ ] Responsive on mobile (resize browser)

---

## 🐛 Troubleshooting

### Backend won't start
**Error**: "No module named 'fastapi'"
**Fix**: Make sure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### AI requests fail
**Error**: "AI service unavailable"
**Fix**: Check your Hugging Face API key in `backend/.env`

**Note**: First AI request takes 10-20 seconds (model loading)

### Frontend can't connect
**Error**: "Network Error" in browser console
**Fix**: Make sure backend is running on http://localhost:8000

### Database errors
**Error**: "Table not found"
**Fix**: Delete `backend/test.db` and restart backend (tables auto-create)

---

## 🎉 Success Indicators

If everything works, you should be able to:

1. ✅ Register and login
2. ✅ See the dashboard
3. ✅ Use AI to improve resume text
4. ✅ See usage counter update
5. ✅ Hit the FREE tier limit (3 calls)
6. ✅ See upgrade modal
7. ✅ Navigate all pages

---

## 📊 Test Data Suggestions

### For AI Testing:
```
Input: "Made a website using React"
Expected: Professional 1-2 sentence rewrite

Input: "Did an internship at company"
Expected: Professional experience description

Input: "Built app with Python"
Expected: Technical project description
```

---

## 🚀 What Happens Behind the Scenes

When you click "Improve with AI":
1. Frontend sends request to `/api/v1/chat/rewrite`
2. Backend checks your authentication (JWT token)
3. Backend checks tier limits (FREE = 3 calls)
4. Backend sanitizes your input (security)
5. Backend calls Hugging Face API
6. Backend increments usage counter
7. Backend returns AI response + usage stats
8. Frontend displays result and updates counter

---

## 💡 Tips for Testing

1. **First AI call is slow** (10-20s) - model needs to load
2. **Subsequent calls are faster** (2-5s)
3. **Clear browser cache** if you see old data
4. **Check browser console** (F12) for errors
5. **Check terminal logs** for backend errors

---

## 🎯 Next Steps After Testing

Once everything works locally:
1. Read `DEPLOYMENT.md` for production deployment
2. Get a real PostgreSQL database (Neon)
3. Deploy backend to Render
4. Deploy frontend to Vercel
5. Add custom domain
6. Integrate payment (Stripe/Razorpay)

---

**Need Help?**
- Check terminal logs for errors
- Open browser DevTools (F12) → Console tab
- Review `API_DOCS.md` for endpoint details
- Check `SECURITY.md` for authentication info

**Happy Testing! 🚀**
