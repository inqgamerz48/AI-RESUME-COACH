"""
AI Chat endpoints with tier enforcement.
ALL AI endpoints require authentication and tier checks.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.schemas import AIRewriteRequest, AIProjectRequest, AISummaryRequest, AIResponse
from app.services.ai_service import AIService
from app.services.tier_service import TierService
from app.api.dependencies import get_current_user


router = APIRouter()


@router.post("/chat/rewrite", response_model=AIResponse)
def rewrite_bullet_point(
    request: AIRewriteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rewrite a resume bullet point.
    Available for: ALL tiers (with usage limits)
    """
    # Check AI usage limit
    can_proceed, info = TierService.check_ai_limit(current_user, db)
    if not can_proceed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=info
        )
    
    # Call AI service
    try:
        result = AIService.rewrite_bullet_point(request.text, request.tone)
        
        # Increment usage
        TierService.increment_ai_usage(current_user, db)
        
        # Get updated usage
        _, usage_info = TierService.check_ai_limit(current_user, db)
        
        return {
            "result": result,
            "usage": {
                "used": usage_info.get("used", 0),
                "limit": usage_info.get("limit", 0),
                "remaining": usage_info.get("remaining", 0)
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")


@router.post("/chat/project", response_model=AIResponse)
def generate_project_description(
    request: AIProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate project description.
    Available for: PRO and ULTIMATE tiers
    """
    # Check feature access
    if not TierService.can_use_feature(current_user, "project_gen"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "feature_locked",
                "message": "Project generation is only available for PRO and ULTIMATE plans.",
                "upgrade_required": True
            }
        )
    
    # Check AI usage limit
    can_proceed, info = TierService.check_ai_limit(current_user, db)
    if not can_proceed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=info)
    
    # Call AI service
    try:
        result = AIService.generate_project_description(
            request.project_name,
            request.tech_stack,
            request.key_points
        )
        
        # Increment usage
        TierService.increment_ai_usage(current_user, db)
        
        # Get updated usage
        _, usage_info = TierService.check_ai_limit(current_user, db)
        
        return {
            "result": result,
            "usage": {
                "used": usage_info.get("used", 0),
                "limit": usage_info.get("limit", 0),
                "remaining": usage_info.get("remaining", 0)
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")


@router.post("/chat/summary", response_model=AIResponse)
def generate_resume_summary(
    request: AISummaryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate resume summary/objective.
    Available for: PRO and ULTIMATE tiers
    """
    # Check feature access
    if not TierService.can_use_feature(current_user, "summary"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "feature_locked",
                "message": "Resume summary generation is only available for PRO and ULTIMATE plans.",
                "upgrade_required": True
            }
        )
    
    # Check AI usage limit
    can_proceed, info = TierService.check_ai_limit(current_user, db)
    if not can_proceed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=info)
    
    # Call AI service
    try:
        result = AIService.generate_resume_summary(
            request.skills,
            request.experience,
            request.goal
        )
        
        # Increment usage
        TierService.increment_ai_usage(current_user, db)
        
        # Get updated usage
        _, usage_info = TierService.check_ai_limit(current_user, db)
        
        return {
            "result": result,
            "usage": {
                "used": usage_info.get("used", 0),
                "limit": usage_info.get("limit", 0),
                "remaining": usage_info.get("remaining", 0)
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")
