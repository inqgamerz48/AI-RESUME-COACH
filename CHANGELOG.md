# Changelog

All notable changes to AI Resume Coach will be documented in this file.

## [1.1.0] - 2025-12-17

### 🚀 Major Updates

#### Changed
- **Migrated from Hugging Face to OpenRouter API** for AI features
  - More reliable AI service with multiple model options
  - Default to `meta-llama/llama-3.1-8b-instruct:free` (free tier)
  - OpenAI-compatible API format for better compatibility
  - Improved error handling and timeout management

#### Added
- **Dashboard AI Features** fully implemented
  - Project Description Generator (PRO+)
  - Resume Summary Generator (PRO+)
  - All features with proper loading states and error handling
- **OpenRouter Setup Guide** (`OPENROUTER_SETUP.md`)
  - Complete integration instructions
  - Model selection guide
  - Troubleshooting section

#### Fixed
- **Backend Authentication** - Fixed token extraction from HTTPAuthorizationCredentials
- **Frontend Error Handling** - Safely parse backend validation errors (objects/arrays)
- **React Crash Fix** - Prevent Error #31 when rendering error objects
- **ESLint Warnings** - Resolved all linting issues in Navbar and TemplateGallery
- **HTML Entities** - Fixed unescaped apostrophes across multiple files

#### Security
- Enhanced error message parsing to prevent object rendering in React
- Improved input sanitization in AI service

### 📝 Documentation Updates
- Updated README with OpenRouter integration details
- Added comprehensive setup guide for OpenRouter
- Updated all environment variable examples
- Updated tech stack documentation

---

## [1.0.0] - 2024-12-14

### 🎉 Initial MVP Release

#### Features
- **Three-tier system**: FREE, PRO, ULTIMATE plans
- **AI-powered resume improvement** using Hugging Face
- **Project description generation** (PRO+)
- **Resume summary generation** (PRO+)
- **PDF export** with tier-based watermarking
- **User authentication** with JWT
- **Resume management** (CRUD operations)
- **Pricing page** with plan comparison
- **Chat-based UI** for AI interactions

#### Security
- JWT authentication with bcrypt password hashing
- Input sanitization (XSS prevention)
- Rate limiting (per IP + per user)
- CORS restricted to frontend domain
- API docs disabled in production
- Secure error handling

#### Backend
- FastAPI with modular structure
- PostgreSQL with SQLAlchemy ORM
- Centralized tier enforcement
- AI service with locked system prompt
- PDF generation with ReportLab
- Parameterized queries for SQL injection prevention

#### Frontend
- React 18 with Vite
- Tailwind CSS for styling
- Zustand for state management
- Protected routes
- Feature locks with upgrade CTAs
- Responsive design

#### Documentation
- Comprehensive README
- Security documentation
- Deployment guide
- Payment integration guide
- Architecture documentation

#### Payment-Ready
- Upgrade/downgrade functions
- Placeholder billing endpoints
- Stripe integration examples
- Razorpay integration examples

### Known Limitations
- Payment integration not implemented (ready for integration)
- Single resume template (expandable)
- No email verification
- No password reset flow
- No admin panel

### Future Enhancements (Roadmap)
- [ ] Multiple resume templates
- [ ] LinkedIn profile import
- [ ] Cover letter generation
- [ ] Email verification
- [ ] Password reset
- [ ] Admin dashboard
- [ ] Analytics and reporting
- [ ] Email notifications
- [ ] Resume sharing links
- [ ] ATS score calculator

---

## How to Use This Changelog

When adding new features:
1. Add a new version header
2. Categorize changes:
   - **Added**: New features
   - **Changed**: Changes in existing functionality
   - **Deprecated**: Soon-to-be removed features
   - **Removed**: Removed features
   - **Fixed**: Bug fixes
   - **Security**: Security improvements

## Version Numbering

Following Semantic Versioning (SemVer):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

Example: 1.2.3
- 1 = Major version
- 2 = Minor version
- 3 = Patch version
