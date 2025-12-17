# Deployment Guide - AI Resume Coach

## Production Deployment Checklist

### Pre-Deployment

- [ ] All environment variables configured
- [ ] Database migrations tested
- [ ] Security review completed
- [ ] Payment integration tested (if enabled)
- [ ] HTTPS certificates obtained
- [ ] Backup strategy in place

---

## Backend Deployment (Render)

### Step 1: Prepare Repository

```bash
# Ensure .gitignore excludes:
# - .env
# - __pycache__/
# - venv/
```

### Step 2: Create Web Service

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: ai-resume-coach-api
   - **Region**: Choose closest to users
   - **Branch**: main
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables

Add these in Render dashboard:

```
DATABASE_URL=postgresql://user:password@host:5432/db
SECRET_KEY=<GENERATE_NEW_32_CHAR_KEY>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key
FRONTEND_URL=https://your-frontend-domain.com
ENVIRONMENT=production
RATE_LIMIT_PER_MINUTE=10
```

**Generate SECRET_KEY:**
```bash
openssl rand -hex 32
```

### Step 4: Deploy

Click "Create Web Service" — Render will build and deploy automatically.

### Step 5: Verify

```bash
curl https://your-api.onrender.com/health
# Should return: {"status":"healthy"}
```

---

## Frontend Deployment (Vercel)
 
 ### Step 1: Prepare for Build
 
 Ensure `frontend/package.json` has next scripts:
 ```json
 {
   "scripts": {
     "dev": "next dev",
     "build": "next build",
     "start": "next start"
   }
 }
 ```
 
 ### Step 2: Create Vercel Project
 
 1. Go to [vercel.com](https://vercel.com)
 2. Click "Add New" → "Project"
 3. Import your GitHub repository
 4. Configure:
    - **Framework Preset**: Next.js (Usually auto-detected)
    - **Root Directory**: `frontend`
    - **Build Command**: `next build` (or `npm run build`)
    - **Output Directory**: (Leave Default)
    - **Install Command**: `npm install`
 
 ### Step 3: Environment Variables
 
 Add in Vercel dashboard:
 
 ```
 NEXT_PUBLIC_API_URL=https://your-api.onrender.com
 ```
 
 ### Step 4: Deploy
 
 Click "Deploy" — Vercel will build and deploy automatically.
 
 ### Step 5: Custom Domain (Optional)
 
 1. Go to Project Settings → Domains
 2. Add your custom domain
 3. Configure DNS records as instructed

---

## Database Setup (Neon)

### Step 1: Create Project

1. Go to [neon.tech](https://neon.tech)
2. Sign up / Log in
3. Click "Create Project"
4. Configure:
   - **Name**: ai-resume-coach-db
   - **Region**: Same as your backend
   - **PostgreSQL Version**: 15+

### Step 2: Get Connection String

1. Go to project dashboard
2. Copy connection string
3. Format: `postgresql://user:password@host/dbname?sslmode=require`

### Step 3: Add to Backend

Paste as `DATABASE_URL` in Render environment variables.

### Step 4: Verify Tables

Tables auto-create on first backend startup. Verify by checking logs.

---

## Post-Deployment

### 1. Test Complete Flow

1. **Register**: Create a test account
2. **Login**: Verify JWT auth works
3. **AI Call**: Test resume improvement
4. **Tier Limits**: Verify FREE tier stops at 3 AI calls
5. **Pricing Page**: Check all plans display
6. **PDF Export**: Test resume PDF generation

### 2. Monitoring

**Backend (Render)**
- Check deployment logs
- Monitor request latency
- Set up health check alerts

**Frontend (Vercel)**
- Monitor build status
- Check deployment previews

**Database (Neon)**
- Monitor connection count
- Check query performance
- Enable auto-suspend for cost savings

### 3. Security Check

- [ ] HTTPS enabled on both frontend and backend
- [ ] CORS only allows your frontend domain
- [ ] API docs disabled (`/docs`, `/redoc` return 404)
- [ ] Environment variables not exposed in frontend build
- [ ] Database uses SSL connection

---

## Scaling Strategies

### Vertical Scaling (Render)

Upgrade instance type:
- **Starter**: 0.5 GB RAM (free tier)
- **Standard**: 2 GB RAM ($7/month)
- **Pro**: 4 GB RAM ($25/month)

### Horizontal Scaling

1. **Add Redis for caching**
   - Cache AI responses by hash of input
   - Store tier limits in Redis

2. **Use CDN for frontend**
   - Cloudflare or Vercel Edge Network

3. **Database connection pooling**
   - Increase pool size in production
   - Use PgBouncer for Postgres

---

## Backup Strategy

### Database Backups (Neon)

- **Automatic**: Neon auto-backups daily
- **Manual**: Use pg_dump for manual backups

```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Code Backups

- **GitHub**: Primary backup
- **Local**: Keep local copy

---

## Rollback Plan

### If Deployment Fails

**Render:**
1. Go to "Deployments" tab
2. Click on last successful deployment
3. Click "Redeploy"

**Vercel:**
1. Go to "Deployments" tab
2. Click on last successful deployment
3. Click "Promote to Production"

---

## Cost Estimation

### Free Tier Setup
- **Render**: Free web service (sleeps after 15min inactivity)
- **Vercel**: Free hobby plan
- **Neon**: Free tier (0.5 GB storage)
- **OpenRouter**: Free tier models available

**Total**: $0/month

### Production Setup
- **Render**: Standard ($7/month)
- **Vercel**: Pro ($20/month)
- **Neon**: Pro ($19/month)
- **OpenRouter**: Free tier or pay-as-you-go (depends on usage)

**Total**: ~$46-60/month

---

## Monitoring & Alerts

### Set Up Alerts

**Render:**
- Deployment failures
- High memory usage
- Slow response times

**Vercel:**
- Build failures
- Deployment errors

**Neon:**
- Connection limits reached
- Storage approaching limit

### Recommended Tools
- **Sentry**: Error tracking
- **LogRocket**: Session replay
- **Uptime Robot**: Uptime monitoring

---

## Troubleshooting

### Backend Issues

**503 Service Unavailable**
- Check Render logs
- Verify DATABASE_URL is correct
- Ensure environment variables are set

**AI Timeout**
- Increase timeout in `ai_service.py`
- Check OpenRouter API status at https://openrouter.ai/status
- Verify OPENROUTER_API_KEY is valid

### Frontend Issues

**White Screen**
- Check browser console
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS settings

**API Connection Failed**
- Verify backend is running
- Check network tab in DevTools

---

## Production Optimization

### 1. Caching

Add Redis for:
- AI response caching
- Session storage
- Rate limit counters

### 2. Database Optimization

- Add indexes on frequently queried fields
- Use database read replicas
- Optimize JSON queries on resume content

### 3. Frontend Optimization

- Code splitting with React.lazy()
- Image optimization
- Enable Gzip compression

---

## CI/CD Setup (Optional)

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: curl ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

**Deployment Complete!** 🚀

Your AI Resume Coach is now live and ready to serve users.
