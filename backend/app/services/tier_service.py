"""
CRITICAL: Tier Enforcement Service
All tier-based access control logic is centralized here.
Backend is the SINGLE SOURCE OF TRUTH for tier limits.
"""
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.models.user import User, PlanTier
from app.models.usage_limit import UsageLimit
from app.core.config import settings
from fastapi import HTTPException, status


class TierService:
    """Centralized tier enforcement service."""
    
    @staticmethod
    def get_ai_limit(plan: PlanTier) -> int:
        """Get AI call limit based on plan tier."""
        limits = {
            PlanTier.FREE: settings.FREE_AI_LIMIT,
            PlanTier.PRO: settings.PRO_AI_LIMIT,
            PlanTier.ULTIMATE: settings.ULTIMATE_AI_LIMIT
        }
        return limits.get(plan, settings.FREE_AI_LIMIT)
    
    @staticmethod
    def get_resume_limit(plan: PlanTier) -> int:
        """Get resume count limit based on plan tier."""
        limits = {
            PlanTier.FREE: settings.FREE_RESUME_LIMIT,
            PlanTier.PRO: settings.PRO_RESUME_LIMIT,
            PlanTier.ULTIMATE: settings.ULTIMATE_RESUME_LIMIT
        }
        return limits.get(plan, settings.FREE_RESUME_LIMIT)
    
    @staticmethod
    def check_plan_active(user: User) -> bool:
        """Check if user's plan is still active."""
        if user.plan == PlanTier.FREE:
            return True
        
        if user.plan_expires_at is None:
            return True
        
        return datetime.utcnow() < user.plan_expires_at
    
    @staticmethod
    def reset_ai_usage_if_needed(usage: UsageLimit, db: Session) -> None:
        """Reset AI usage counter if it's a new day."""
        today = date.today()
        if usage.ai_calls_reset_date < today:
            usage.ai_calls_used = 0
            usage.ai_calls_reset_date = today
            db.commit()
    
    @staticmethod
    def check_ai_limit(user: User, db: Session) -> tuple[bool, dict]:
        """
        Check if user can make AI call.
        Returns: (can_proceed, info_dict)
        """
        # Check if plan is active
        if not TierService.check_plan_active(user):
            return False, {
                "error": "plan_expired",
                "message": "Your plan has expired. Please upgrade to continue.",
                "upgrade_required": True
            }
        
        # Get or create usage limit
        usage = db.query(UsageLimit).filter(UsageLimit.user_id == user.id).first()
        if not usage:
            usage = UsageLimit(user_id=user.id)
            db.add(usage)
            db.commit()
            db.refresh(usage)
        
        # Reset usage if needed
        TierService.reset_ai_usage_if_needed(usage, db)
        
        # Check limit
        limit = TierService.get_ai_limit(user.plan)
        if usage.ai_calls_used >= limit:
            return False, {
                "error": "limit_reached",
                "message": f"You've reached your {user.plan} plan limit of {limit} AI calls.",
                "used": usage.ai_calls_used,
                "limit": limit,
                "upgrade_required": True if user.plan != PlanTier.ULTIMATE else False
            }
        
        return True, {
            "can_proceed": True,
            "used": usage.ai_calls_used,
            "limit": limit,
            "remaining": limit - usage.ai_calls_used
        }
    
    @staticmethod
    def increment_ai_usage(user: User, db: Session) -> None:
        """Increment AI usage counter."""
        usage = db.query(UsageLimit).filter(UsageLimit.user_id == user.id).first()
        if usage:
            usage.ai_calls_used += 1
            db.commit()
    
    @staticmethod
    def check_resume_limit(user: User, db: Session) -> tuple[bool, dict]:
        """Check if user can create another resume."""
        usage = db.query(UsageLimit).filter(UsageLimit.user_id == user.id).first()
        if not usage:
            return True, {"can_proceed": True}
        
        limit = TierService.get_resume_limit(user.plan)
        if usage.resume_count >= limit:
            return False, {
                "error": "limit_reached",
                "message": f"You've reached your {user.plan} plan limit of {limit} resumes.",
                "used": usage.resume_count,
                "limit": limit,
                "upgrade_required": True if user.plan != PlanTier.ULTIMATE else False
            }
        
        return True, {
            "can_proceed": True,
            "used": usage.resume_count,
            "limit": limit
        }
    
    @staticmethod
    def increment_resume_count(user: User, db: Session) -> None:
        """Increment resume counter."""
        usage = db.query(UsageLimit).filter(UsageLimit.user_id == user.id).first()
        if not usage:
            usage = UsageLimit(user_id=user.id, resume_count=1)
            db.add(usage)
        else:
            usage.resume_count += 1
        db.commit()
    
    @staticmethod
    def can_use_feature(user: User, feature: str) -> bool:
        """
        Check if user's plan allows a specific feature.
        Features: pdf_no_watermark, summary, project_gen, advanced_tone, multiple_resumes
        """
        feature_matrix = {
            PlanTier.FREE: [],
            PlanTier.PRO: ["pdf_no_watermark", "summary", "project_gen", "multiple_resumes", "basic_tone"],
            PlanTier.ULTIMATE: ["pdf_no_watermark", "summary", "project_gen", "multiple_resumes", "basic_tone", "advanced_tone", "priority_processing"]
        }
        
        allowed_features = feature_matrix.get(user.plan, [])
        return feature in allowed_features


def upgrade_user_plan(user_id: int, new_plan: PlanTier, expires_at: datetime, db: Session) -> User:
    """
    PAYMENT INTEGRATION POINT
    Upgrade user to new plan. Called after successful payment.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.plan = new_plan
    user.plan_expires_at = expires_at
    db.commit()
    db.refresh(user)
    return user


def downgrade_user_plan(user_id: int, db: Session) -> User:
    """
    PAYMENT INTEGRATION POINT
    Downgrade user to FREE plan. Called on subscription cancellation.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.plan = PlanTier.FREE
    user.plan_expires_at = None
    db.commit()
    db.refresh(user)
    return user
