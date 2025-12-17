<div align="center">

![AI Resume Coach Banner](assets/banner.png)

# 🚀 AI Resume Coach for Freshers

### *Your AI-Powered Resume Building SaaS – Production Ready MVP*

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.0-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**[Features](#-key-features)** • 
**[Quick Start](#-quick-start)** • 
**[Documentation](#-documentation)** • 
**[Deployment](#-deployment)** • 
**[License](#-license)**

---

### ⚡ Production-Ready • 💰 Monetization Built-In • 🔒 Enterprise Security

</div>

---

## � Screenshots

<div align="center">

### Dashboard Preview
![Dashboard](assets/dashboard-preview.png)

*Modern, intuitive interface with AI-powered resume improvement*

</div>

---

## �📖 What is AI Resume Coach?

**AI Resume Coach for Freshers** is a **complete, production-ready SaaS MVP** that helps students and fresh graduates create professional, ATS-optimized resumes using AI assistance. 

Built with a **3-tier monetization system** (FREE, PRO, ULTIMATE), this application is ready to deploy, customize, and start generating revenue immediately.

### 🎯 Perfect For

- 🚀 **Entrepreneurs** looking to launch an AI SaaS product
- 🏢 **Agencies** wanting to offer resume services to clients
- 👨‍💻 **Developers** seeking a production-quality reference project
- 🎓 **Educators** teaching full-stack development
- 💼 **Freelancers** building portfolio projects

---

## ✨ Key Features

### 🤖 AI-Powered Features
- **Smart Resume Writing**: Transform basic bullet points into professional content
- **Project Description Generator**: AI-generated project descriptions (PRO+)
- **Resume Summary Creator**: Compelling summary statements (PRO+)
- **Tone Variations**: Professional, confident, concise, and impactful tones (ULTIMATE)

### 💎 Premium Capabilities
- **Multi-Resume Management**: Create and manage multiple resumes
- **ATS-Safe PDF Export**: Industry-standard formatting
- **Template System**: Ready for expansion with more designs
- **Usage Analytics**: Track AI usage and tier limits

### 🔐 Enterprise-Grade Security
- ✅ JWT Authentication with bcrypt password hashing
- ✅ Input sanitization & XSS prevention
- ✅ Rate limiting (IP-based & user-based)
- ✅ CORS protection
- ✅ SQL injection prevention via ORM
- ✅ Secure error handling (no info leakage)

### 💰 Built-In Monetization
- ✅ 3-Tier pricing system (FREE/PRO/ULTIMATE)
- ✅ Backend-enforced usage limits
- ✅ Payment integration ready (Stripe & Razorpay)
- ✅ Subscription management infrastructure
- ✅ Upgrade/downgrade flows

---

## 🏗️ Tech Stack

<div align="center">

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Next.js 15+, Tailwind CSS 3.4+, Zustand, Axios |
| **Backend** | FastAPI, Python 3.9+, SQLAlchemy, Pydantic, JWT |
| **Database** | PostgreSQL (Neon recommended) |
| **AI** | Hugging Face Inference API (`google/flan-t5-small`) |
| **PDF** | ReportLab |
| **Deployment** | Render (Backend), Vercel (Frontend) |

</div>

---

## 💎 Tier Comparison

| Feature | FREE | PRO ($9.99/mo) | ULTIMATE ($19.99/mo) |
|---------|:----:|:--------------:|:--------------------:|
| AI Actions/Month | 3 | 50 | ♾️ Unlimited |
| Resume Count | 1 | 10 | ♾️ Unlimited |
| Templates | 1 Basic | All | All + Future |
| PDF Watermark | ✅ | ❌ | ❌ |
| Resume Summary | ❌ | ✅ | ✅ |
| Project Generation | ❌ | ✅ | ✅ |
| Tone Control | Basic | Basic | Advanced |
| Priority Processing | ❌ | ❌ | ✅ |

> **💡 Tier enforcement happens on the backend** – Frontend only displays locks, server validates all requests.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- PostgreSQL database ([Neon](https://neon.tech) recommended for free tier)
- [Hugging Face API Key](https://huggingface.co/settings/tokens) (free)

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd FRESHER-RESUME-MAKER

# Run the setup script
chmod +x setup.sh
./setup.sh

# Follow the interactive prompts
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your DATABASE_URL, SECRET_KEY, HUGGINGFACE_API_KEY

# Run server
uvicorn app.main:app --reload
```

**Backend runs at:** `http://localhost:8000`

#### Frontend Setup
 
 ```bash
 cd frontend
 
 # Install dependencies
 npm install
 
 # Configure environment
 echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
 
 # Run development server
 npm run dev
 ```
 
 **Frontend runs at:** `http://localhost:3000`
 
 ### Environment Variables
 
 <details>
 <summary>📝 Click to see all required environment variables</summary>
 
 **Backend `.env`:**
 ```bash
 DATABASE_URL=postgresql://user:password@host:5432/database
 SECRET_KEY=your-secret-key-min-32-characters
 ALGORITHM=HS256
 ACCESS_TOKEN_EXPIRE_MINUTES=30
 HUGGINGFACE_API_KEY=hf_your_api_key_here
 FRONTEND_URL=http://localhost:3000
 ENVIRONMENT=development
 RATE_LIMIT_PER_MINUTE=10
 ```
 
 **Frontend `.env.local`:**
 ```bash
 NEXT_PUBLIC_API_URL=http://localhost:8000
 ```
 
 </details>

---

## 📚 Documentation

Comprehensive guides are available in the repository:

| Document | Description |
|----------|-------------|
| **[API Documentation](docs/API_DOCS.md)** | Complete API reference with examples |
| **[Security Guide](docs/SECURITY.md)** | Security features and best practices |
| **[Deployment Guide](docs/DEPLOYMENT.md)** | Step-by-step deployment guide |
| **[Contributing Guidelines](docs/CONTRIBUTING.md)** | Development guidelines |
| **[Quick Test Guide](docs/QUICK_TEST.md)** | Quick testing guide |
| **[Browser Testing](docs/BROWSER_TESTING.md)** | Browser testing instructions |
| **[Project Summary](docs/PROJECT_SUMMARY.md)** | Complete project overview |
| **[CHANGELOG](CHANGELOG.md)** | Version history |

---

## 🌐 Deployment

### Backend → Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables (see [DEPLOYMENT.md](DEPLOYMENT.md))

### Frontend → Vercel

1. Import your repository on [Vercel](https://vercel.com)
2. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (or `next build`)
3. Add `NEXT_PUBLIC_API_URL` environment variable pointing to your backend URL

### Database → Neon

1. Create a project at [neon.tech](https://neon.tech)
2. Copy the connection string
3. Add as `DATABASE_URL` in backend environment

**Full deployment guide:** [DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 💳 Payment Integration

The application is **payment-ready** with infrastructure for Stripe and Razorpay.

### Integration Points

- **Upgrade Function**: `/backend/app/services/tier_service.py`
- **Billing Endpoints**: `/backend/app/api/v1/endpoints/billing.py`
- **Frontend Pricing**: `/frontend/src/pages/Pricing.jsx`

### Example: Stripe Integration

```python
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{'price': 'price_XXX', 'quantity': 1}],
    mode='subscription',
    success_url=f'{settings.FRONTEND_URL}/success',
    cancel_url=f'{settings.FRONTEND_URL}/cancel',
    client_reference_id=str(user_id)
)
```

**Full payment guide:** See comments in `billing.py`

---

## 🏗️ Project Structure

```
FRESHER RESUME MAKER/
├── 📁 backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # API routes
│   │   ├── core/                 # Config & security
│   │   ├── db/                   # Database connection
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   │   ├── tier_service.py   # 🔑 Tier enforcement
│   │   │   ├── ai_service.py     # 🤖 AI integration
│   │   │   └── pdf_service.py    # PDF generation
│   │   └── main.py               # FastAPI app
│   └── requirements.txt
│
├── 📁 frontend/
│   ├── src/
│   │   ├── app/                  # Next.js App Router Pages
│   │   ├── components/           # Reusable components
│   │   ├── services/             # API client
│   │   ├── store/                # State management (Zustand)
│   ├── public/                   # Static assets
│   ├── package.json
│   ├── next.config.mjs
│   └── tailwind.config.js
│
├── 📄 README.md
├── 📁 docs/                      # Documentation
├── 📁 scripts/                   # Setup scripts
└── 📄 LICENSE
```

---

## 🛡️ Security Features

This application implements enterprise-grade security:

- ✅ **Authentication**: JWT tokens with configurable expiration
- ✅ **Password Security**: bcrypt hashing with cost factor 12
- ✅ **Input Validation**: All inputs sanitized and validated
- ✅ **Rate Limiting**: 10 requests/minute per IP (configurable)
- ✅ **CORS Protection**: Restricted to frontend domain
- ✅ **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- ✅ **XSS Prevention**: HTML sanitization on all text inputs
- ✅ **Production Hardening**: API docs disabled, secure error messages

**Full security documentation:** [SECURITY.md](docs/SECURITY.md)

---

## 🎨 Customization

### Easy Customizations

1. **Branding**: Update colors in `frontend/tailwind.config.js`
2. **Tier Limits**: Modify `backend/app/core/config.py`
3. **AI Model**: Switch to GPT-3.5, Claude, or other models in `ai_service.py`
4. **Templates**: Add resume templates in `pdf_service.py`
5. **Pricing**: Adjust prices in `frontend/src/pages/Pricing.jsx`

### Advanced Extensions

- Email verification system
- Password reset functionality
- Cover letter generation
- LinkedIn profile optimization
- ATS score calculator
- Team/agency accounts

---

## 📊 Business Model Examples

### SaaS (Direct to Consumer)

- **FREE Tier**: Lead generation (3 AI credits)
- **PRO Tier**: $9.99/month → Target 1,000 users = **$9,990/month MRR**
- **ULTIMATE Tier**: $19.99/month → Target 100 users = **$1,999/month MRR**

**Total Potential**: ~$12,000/month recurring revenue

### White-Label (B2B)

- Sell to recruitment agencies or universities
- One-time setup: $2,000-$5,000 per client
- Monthly hosting/support: $500/month
- **Target**: 10 clients = $60,000 setup + $5,000/mo recurring

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for:

- Code style guidelines
- Pull request process
- Development setup
- Testing requirements

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**You can:**
- ✅ Use commercially
- ✅ Modify freely
- ✅ Distribute
- ✅ Include in proprietary software

**Requirements:**
- Include original license and copyright notice

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Hugging Face](https://huggingface.co/) - AI model infrastructure
- [Neon](https://neon.tech/) - Serverless PostgreSQL

---

## 📞 Support

For questions or issues:

1. Check the [documentation](#-documentation)
2. Review inline code comments
3. Open an issue on GitHub

---

<div align="center">

### ⭐ Star this repo if you find it useful!

**Built with ❤️ for developers, entrepreneurs, and innovators**

[Report Bug](../../issues) • [Request Feature](../../issues) • [Documentation](#-documentation)

---

**Ready to deploy, customize, and monetize!** 🚀

</div>
