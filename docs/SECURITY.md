# 🔒 Security Measures - AI Resume Coach

## Overview
This document details all security measures implemented in the application.

## Authentication & Authorization

### 1. JWT Authentication
- **Algorithm**: HS256
- **Token Expiration**: Configurable (default 30 minutes)
- **Storage**: Frontend stores in localStorage (consider httpOnly cookies for production enhancement)
- **Validation**: Every protected endpoint validates token

### 2. Password Security
- **Hashing**: bcrypt with cost factor 12
- **Minimum Length**: 8 characters (enforced frontend + backend)
- **No plaintext storage**: Passwords are hashed immediately on registration

## Input Validation & Sanitization

### Backend Sanitization
All user inputs pass through `sanitize_input()` function:
```python
def sanitize_input(text: str, max_length: int = 500) -> str:
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Escape HTML entities  
    text = html.escape(text)
    # Limit length
    text = text[:max_length]
    return text.strip()
```

### Pydantic Validation
All API requests validated with Pydantic schemas:
- Email format validation
- Field length restrictions
- Type checking

## Rate Limiting

### Implementation
- **Library**: SlowAPI
- **Default**: 10 requests/minute per IP
- **Per-user limits**: Enforced via tier system

### Configuration
```python
RATE_LIMIT_PER_MINUTE: int = 10
```

## Database Security

### SQL Injection Prevention
- **ORM**: SQLAlchemy with parameterized queries
- **No raw SQL**: All queries use ORM methods

### Connection Security
- **SSL**: Recommended for production databases
- **Connection pooling**: Limited connections (pool_size=10, max_overflow=20)

## API Security

### 1. CORS Configuration
```python
allow_origins=[settings.FRONTEND_URL]  # NOT '*'
allow_credentials=True
```

### 2. API Documentation
- **Disabled in production**: `/docs` and `/redoc` only in development
- **OpenAPI spec**: Hidden in production

### 3. Error Handling
- **Production**: Generic error messages (no stack traces)
- **Development**: Detailed errors for debugging

## AI Security

### Locked System Prompt
The AI system prompt is hardcoded and unexposed:
```python
SYSTEM_PROMPT = """You are an AI Resume Coach..."""
# This prompt CANNOT be modified by users
```

### AI Input Limits
- **Max length**: 500 characters per input
- **Sanitized**: All inputs cleaned before AI call
- **Timeout**: 30-second timeout on AI requests

### No Free Chat
AI can ONLY perform predefined tasks:
- Rewrite bullet points
- Generate project descriptions
- Generate summaries

## Environment Variables

### Required Secrets
All secrets via environment variables:
- `SECRET_KEY`: Min 32 characters
- `DATABASE_URL`: Never committed to git
- `HUGGINGFACE_API_KEY`: API access key

### .env Security
- **.gitignore**: `.env` files excluded
- **.env.example**: Template with no real values

## Session Management

### Token Expiration
- **Access tokens**: Expire after configured time
- **No refresh tokens in MVP**: Consider adding for production

### Logout
- **Client-side**: Token removed from storage
- **Server-side**: Stateless (token becomes invalid after expiry)

## HTTPS & Transport Security

### Production Requirements
- **HTTPS Only**: Recommended for production
- **HSTS**: Consider adding Strict-Transport-Security header

## Tier Enforcement Security

### Backend Validation
All tier checks happen server-side:
```python
can_proceed, info = TierService.check_ai_limit(current_user, db)
if not can_proceed:
    raise HTTPException(403, detail=info)
```

**Frontend locks are UI-only** — backend enforces ALL limits.

## Payment Security (When Integrated)

### Webhook Verification
Always verify webhook signatures:
- **Stripe**: `stripe.Webhook.construct_event()`
- **Razorpay**: `Utility.verify_webhook_signature()`

### Never Trust Client
- **Server-side verification**: Always verify payment on backend
- **Don't trust amount**: Verify payment amount matches plan price

## Security Checklist for Production

- [ ] Change `SECRET_KEY` to production value (min 32 random chars)
- [ ] Set `ENVIRONMENT=production`
- [ ] Enable HTTPS
- [ ] Use production database with SSL
- [ ] Add HSTS headers
- [ ] Consider httpOnly cookies for tokens
- [ ] Set up monitoring and alerts
- [ ] Enable database backups
- [ ] Add Web Application Firewall (WAF)
- [ ] Implement request logging
- [ ] Set up intrusion detection

## Incident Response

### If Security Breach Occurs
1. Immediately rotate `SECRET_KEY`
2. Invalidate all active sessions
3. Force password resets
4. Audit database for unauthorized access
5. Review logs for attack patterns
6. Notify affected users

## Compliance Notes

### GDPR Considerations
- **Data minimization**: Only collect necessary data
- **Right to deletion**: Implement user deletion endpoint
- **Data export**: Add endpoint to export user data

### SOC 2 Readiness
- **Logging**: Implement comprehensive audit logs
- **Access control**: Role-based access in future versions
- **Encryption**: At rest and in transit

---

**Last Updated**: 2025-12-14  
**Security Review**: Required before production deployment
