"""
Template API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.template import ResumeTemplate
from app.models.user import User, PlanTier
from app.api.dependencies import get_current_user
from pydantic import BaseModel


router = APIRouter()


# Schemas
class TemplateResponse(BaseModel):
    id: int
    name: str
    display_name: str
    description: Optional[str]
    industry: Optional[str]
    position_type: Optional[str]
    category: Optional[str]
    tier_required: str
    preview_image: Optional[str]
    is_featured: bool
    
    class Config:
        from_attributes = True


class TemplateListResponse(BaseModel):
    templates: List[TemplateResponse]
    total: int
    available_to_user: int


@router.get("/templates", response_model=TemplateListResponse)
def get_all_templates(
    industry: Optional[str] = None,
    position_type: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all resume templates with optional filtering.
    Returns templates available to user's tier and higher tiers (locked).
    """
    query = db.query(ResumeTemplate).filter(ResumeTemplate.is_active == True)
    
    # Apply filters
    if industry:
        query = query.filter(ResumeTemplate.industry == industry)
    if position_type:
        query = query.filter(ResumeTemplate.position_type == position_type)
    if category:
        query = query.filter(ResumeTemplate.category == category)
    
    # Order by featured first, then by usage count
    query = query.order_by(
        ResumeTemplate.is_featured.desc(),
        ResumeTemplate.usage_count.desc()
    )
    
    templates = query.all()
    
    # Count available templates based on user tier
    tier_hierarchy = {
        PlanTier.FREE: 0,
        PlanTier.PRO: 1,
        PlanTier.ULTIMATE: 2
    }
    user_tier_level = tier_hierarchy.get(current_user.plan, 0)
    
    available_count = sum(
        1 for t in templates 
        if tier_hierarchy.get(PlanTier[t.tier_required], 0) <= user_tier_level
    )
    
    return {
        "templates": templates,
        "total": len(templates),
        "available_to_user": available_count
    }


@router.get("/templates/{template_id}", response_model=TemplateResponse)
def get_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific template details"""
    template = db.query(ResumeTemplate).filter(
        ResumeTemplate.id == template_id,
        ResumeTemplate.is_active == True
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return template


@router.get("/templates/industries/list")
def get_industries(db: Session = Depends(get_db)):
    """Get list of all industries"""
    industries = db.query(ResumeTemplate.industry).distinct().all()
    return {"industries": [i[0] for i in industries if i[0]]}


@router.get("/templates/categories/list")
def get_categories(db: Session = Depends(get_db)):
    """Get list of all categories"""
    categories = db.query(ResumeTemplate.category).distinct().all()
    return {"categories": [c[0] for c in categories if c[0]]}


@router.get("/templates/position-types/list")
def get_position_types(db: Session = Depends(get_db)):
    """Get list of all position types"""
    position_types = db.query(ResumeTemplate.position_type).distinct().all()
    return {"position_types": [p[0] for p in position_types if p[0]]}


@router.get("/templates/featured")
def get_featured_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get featured templates"""
    templates = db.query(ResumeTemplate).filter(
        ResumeTemplate.is_featured == True,
        ResumeTemplate.is_active == True
    ).limit(6).all()
    
    return {"templates": templates}


@router.post("/templates/{template_id}/increment-usage")
def increment_template_usage(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Increment template usage count when user selects it"""
    template = db.query(ResumeTemplate).filter(
        ResumeTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template.usage_count += 1
    db.commit()
    
    return {"message": "Usage count updated", "usage_count": template.usage_count}
