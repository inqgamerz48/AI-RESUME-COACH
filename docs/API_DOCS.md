# API Documentation - AI Resume Coach

## Base URL

**Development**: `http://localhost:8000`  
**Production**: `https://your-api.onrender.com`

---

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Token Expiration
- **Default**: 30 minutes
- **Renewable**: No (user must re-login)

---

## Endpoints

### 1. Authentication

#### POST `/api/v1/auth/register`

Register a new user. Default plan is FREE.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"  // Optional
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "plan": "FREE"
  }
}
```

**Errors:**
- `400`: Email already registered
- `400`: Invalid email format
- `400`: Password too short

---

#### POST `/api/v1/auth/login`

Login with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "plan": "FREE"
  }
}
```

**Errors:**
- `401`: Incorrect email or password

---

### 2. AI Chat

All AI endpoints require authentication and enforce tier limits.

#### POST `/api/v1/chat/rewrite`

Rewrite a resume bullet point.

**Available for**: ALL tiers (with usage limits)

**Request Body:**
```json
{
  "text": "Worked on React project",
  "tone": "professional"  // Optional: professional, neutral
}
```

**Response (200):**
```json
{
  "result": "Developed and maintained React-based web applications, implementing modern UI components and ensuring code quality",
  "usage": {
    "used": 1,
    "limit": 3,
    "remaining": 2
  }
}
```

**Errors:**
- `400`: Text is required
- `403`: AI usage limit reached (FREE tier: 3, PRO: 50, ULTIMATE: unlimited)
- `503`: AI service unavailable

---

#### POST `/api/v1/chat/project`

Generate project description.

**Available for**: PRO and ULTIMATE tiers

**Request Body:**
```json
{
  "project_name": "E-commerce Platform",
  "tech_stack": "React, Node.js, MongoDB",
  "key_points": "Built shopping cart, integrated payment gateway, deployed on AWS"
}
```

**Response (200):**
```json
{
  "result": "Developed a full-stack e-commerce platform using React, Node.js, and MongoDB. Implemented secure shopping cart functionality, integrated payment gateway for transactions, and deployed the application on AWS infrastructure.",
  "usage": {
    "used": 2,
    "limit": 50,
    "remaining": 48
  }
}
```

**Errors:**
- `403`: Feature locked (FREE tier)
- `403`: AI usage limit reached

---

#### POST `/api/v1/chat/summary`

Generate resume summary/objective.

**Available for**: PRO and ULTIMATE tiers

**Request Body:**
```json
{
  "skills": "React, Python, SQL",
  "experience": "2 internships in web development",
  "goal": "Seeking full-stack developer position"
}
```

**Response (200):**
```json
{
  "result": "Motivated computer science graduate with hands-on experience in React, Python, and SQL. Completed 2 internships in web development, demonstrating proficiency in full-stack technologies. Seeking to leverage technical skills and problem-solving abilities in a full-stack developer role.",
  "usage": {
    "used": 3,
    "limit": 50,
    "remaining": 47
  }
}
```

**Errors:**
- `403`: Feature locked (FREE tier)
- `403`: AI usage limit reached

---

### 3. Resume Management

#### POST `/api/v1/resume`

Create a new resume.

**Request Body:**
```json
{
  "title": "Software Engineer Resume",
  "template_id": "basic",
  "personal_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "location": "New York, NY"
  },
  "summary": "Motivated software engineer...",
  "education": [
    {
      "degree": "B.Tech in Computer Science",
      "institution": "XYZ University",
      "year": "2024",
      "gpa": "3.8"
    }
  ],
  "skills": ["React", "Python", "SQL"],
  "projects": [
    {
      "name": "E-commerce Platform",
      "description": "Built full-stack web app",
      "tech_stack": "React, Node.js",
      "duration": "3 months"
    }
  ]
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Software Engineer Resume",
  "template_id": "basic",
  "content": { /* full resume structure */ },
  "created_at": "2024-12-14T10:00:00Z",
  "updated_at": "2024-12-14T10:00:00Z"
}
```

**Errors:**
- `403`: Resume limit reached (FREE: 1, PRO: 10, ULTIMATE: unlimited)

---

#### GET `/api/v1/resume`

Get all resumes for current user.

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Software Engineer Resume",
    "template_id": "basic",
    "content": { /* ... */ },
    "created_at": "2024-12-14T10:00:00Z",
    "updated_at": "2024-12-14T10:00:00Z"
  }
]
```

---

#### GET `/api/v1/resume/{resume_id}`

Get a specific resume.

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Software Engineer Resume",
  "content": { /* ... */ },
  "created_at": "2024-12-14T10:00:00Z",
  "updated_at": "2024-12-14T10:00:00Z"
}
```

**Errors:**
- `404`: Resume not found

---

#### PUT `/api/v1/resume/{resume_id}`

Update a resume.

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": { /* updated content */ }
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Updated Title",
  /* ... */
}
```

---

#### DELETE `/api/v1/resume/{resume_id}`

Delete a resume (soft delete).

**Response (204):** No content

**Errors:**
- `404`: Resume not found

---

#### GET `/api/v1/resume/{resume_id}/pdf`

Export resume as PDF.

**Response (200):**
- Content-Type: `application/pdf`
- File download with name: `resume_{id}.pdf`

**Notes:**
- FREE tier: PDF includes watermark
- PRO/ULTIMATE: No watermark

---

### 4. Billing

#### GET `/api/v1/billing/plans`

Get pricing information for all plans.

**Response (200):**
```json
{
  "plans": [
    {
      "tier": "FREE",
      "name": "Free Trial",
      "price": 0,
      "currency": "USD",
      "billing_cycle": "forever",
      "features": [
        "3 AI resume improvements",
        "1 resume only",
        /* ... */
      ],
      "limitations": [
        "Limited AI usage",
        /* ... */
      ]
    },
    {
      "tier": "PRO",
      "name": "Professional",
      "price": 9.99,
      "currency": "USD",
      "billing_cycle": "monthly",
      "features": [ /* ... */ ],
      "popular": true
    },
    {
      "tier": "ULTIMATE",
      "name": "Ultimate",
      "price": 19.99,
      "currency": "USD",
      "billing_cycle": "monthly",
      "features": [ /* ... */ ],
      "recommended_for": "Power users & job agencies"
    }
  ]
}
```

---

#### POST `/api/v1/billing/upgrade`

**⚠️ PLACEHOLDER - NOT IMPLEMENTED**

Upgrade user plan.

**Request Body:**
```json
{
  "plan": "PRO",
  "payment_method": "stripe"  // or "razorpay"
}
```

**Response (501):**
```json
{
  "message": "Payment integration not yet implemented. This is a placeholder endpoint.",
  "payment_provider": "stripe",
  "target_plan": "PRO",
  "documentation": "See README.md for integration guide"
}
```

---

#### POST `/api/v1/billing/webhook`

**⚠️ PLACEHOLDER - NOT IMPLEMENTED**

Handle payment webhooks from Stripe/Razorpay.

**Response (501):**
```json
{
  "message": "Webhook not yet implemented. This is a placeholder endpoint.",
  "documentation": "See README.md for webhook integration guide"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

### Standard HTTP Status Codes

- `200`: Success
- `201`: Created
- `204`: No Content (successful deletion)
- `400`: Bad Request (validation error)
- `401`: Unauthorized (missing/invalid token)
- `403`: Forbidden (tier limit or feature lock)
- `404`: Not Found
- `500`: Internal Server Error
- `503`: Service Unavailable (AI service down)

---

## Rate Limiting

### Global Limits
- **Rate**: 10 requests per minute per IP
- **Headers**: 
  - `X-RateLimit-Limit`: Maximum requests
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

### Tier-Based Limits

AI usage limits reset daily:

| Tier | AI Calls/Day | Resumes |
|------|--------------|---------|
| FREE | 3 | 1 |
| PRO | 50 | 10 |
| ULTIMATE | Unlimited | Unlimited |

---

## Tier Feature Matrix

| Feature | FREE | PRO | ULTIMATE |
|---------|------|-----|----------|
| Bullet Rewrite | ✅ | ✅ | ✅ |
| Project Generation | ❌ | ✅ | ✅ |
| Summary Generation | ❌ | ✅ | ✅ |
| PDF No Watermark | ❌ | ✅ | ✅ |
| Advanced Tone | ❌ | ❌ | ✅ |
| Priority Processing | ❌ | ❌ | ✅ |

---

## Example API Calls

### Using cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Rewrite Bullet (with token):**
```bash
curl -X POST http://localhost:8000/api/v1/chat/rewrite \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"text":"Worked on React project"}'
```

### Using JavaScript (Axios)

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Register
const register = async () => {
  const response = await axios.post(`${API_URL}/api/v1/auth/register`, {
    email: 'test@example.com',
    password: 'password123'
  });
  return response.data;
};

// Rewrite with auth
const rewrite = async (text, token) => {
  const response = await axios.post(
    `${API_URL}/api/v1/chat/rewrite`,
    { text },
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  return response.data;
};
```

---

## WebSocket Support

**Currently not implemented.**

For real-time features (chat, notifications), consider adding WebSocket support in future versions.

---

**Last Updated**: 2024-12-14  
**API Version**: 1.0.0
