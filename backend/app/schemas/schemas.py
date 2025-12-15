"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.user import PlanTier


# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


# User Schemas
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    plan: PlanTier
    plan_expires_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# AI Chat Schemas
class AIRewriteRequest(BaseModel):
    text: str = Field(..., max_length=300)
    tone: str = "professional"


class AIProjectRequest(BaseModel):
    project_name: str = Field(..., max_length=100)
    tech_stack: str = Field(..., max_length=200)
    key_points: str = Field(..., max_length=300)


class AISummaryRequest(BaseModel):
    skills: str = Field(..., max_length=200)
    experience: str = Field(..., max_length=200)
    goal: str = Field(..., max_length=200)


class AIResponse(BaseModel):
    result: str
    usage: Dict[str, int]


# Resume Schemas
class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str
    location: Optional[str] = None


class Education(BaseModel):
    degree: str
    institution: str
    year: str
    gpa: Optional[str] = None


class Project(BaseModel):
    name: str
    description: str
    tech_stack: Optional[str] = None
    duration: Optional[str] = None


class ResumeCreate(BaseModel):
    title: str = "My Resume"
    template_id: str = "basic"
    personal_info: PersonalInfo
    summary: Optional[str] = None
    education: List[Education] = []
    skills: List[str] = []
    projects: List[Project] = []


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    template_id: Optional[str] = None
    content: Optional[Dict[str, Any]] = None


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    title: str
    template_id: str
    content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Payment Schemas (PLACEHOLDER - NOT IMPLEMENTED)
class UpgradeRequest(BaseModel):
    plan: PlanTier
    payment_method: str  # "stripe" or "razorpay"


class WebhookEvent(BaseModel):
    event_type: str
    data: Dict[str, Any]


# Resume Analyzer Schemas
class ResumeAnalysisResponse(BaseModel):
    id: int
    filename: str
    overall_score: float
    ats_score: float
    content_score: float
    structure_score: float
    suggestions: List[Dict[str, Any]]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class EnhanceResumeRequest(BaseModel):
    accepted_suggestions: List[int] = Field(..., description="List of suggestion indices to accept")

