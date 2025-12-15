import pytest
from datetime import datetime, timedelta, date
from unittest.mock import MagicMock
from app.services.tier_service import TierService, upgrade_user_plan, downgrade_user_plan
from app.models.user import User, PlanTier
from app.models.usage_limit import UsageLimit
from app.core.config import settings
from fastapi import HTTPException

# --- Fixtures ---

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def free_user():
    return User(id=1, email="free@example.com", plan=PlanTier.FREE, plan_expires_at=None)

@pytest.fixture
def pro_user():
    return User(id=2, email="pro@example.com", plan=PlanTier.PRO, plan_expires_at=datetime.utcnow() + timedelta(days=30))

@pytest.fixture
def ultimate_user():
    return User(id=3, email="ultimate@example.com", plan=PlanTier.ULTIMATE, plan_expires_at=datetime.utcnow() + timedelta(days=30))

@pytest.fixture
def expired_pro_user():
    return User(id=4, email="expired@example.com", plan=PlanTier.PRO, plan_expires_at=datetime.utcnow() - timedelta(days=1))

# --- Tests ---

def test_get_limits(free_user, pro_user, ultimate_user):
    assert TierService.get_ai_limit(PlanTier.FREE) == settings.FREE_AI_LIMIT
    assert TierService.get_ai_limit(PlanTier.PRO) == settings.PRO_AI_LIMIT
    assert TierService.get_ai_limit(PlanTier.ULTIMATE) == settings.ULTIMATE_AI_LIMIT
    
    assert TierService.get_resume_limit(PlanTier.FREE) == settings.FREE_RESUME_LIMIT
    assert TierService.get_resume_limit(PlanTier.PRO) == settings.PRO_RESUME_LIMIT
    assert TierService.get_resume_limit(PlanTier.ULTIMATE) == settings.ULTIMATE_RESUME_LIMIT

def test_check_plan_active(free_user, pro_user, expired_pro_user):
    assert TierService.check_plan_active(free_user) is True
    assert TierService.check_plan_active(pro_user) is True
    assert TierService.check_plan_active(expired_pro_user) is False
    
    # User with no expiry date but not FREE (edge case, should default active in logic or handle appropriately)
    # The logic says: if user.plan == FREE return True. if user.plan_expires_at is None return True.
    # So a PRO user with None expiry is considered Active (maybe unlimited trial).
    weird_user = User(id=5, plan=PlanTier.PRO, plan_expires_at=None)
    assert TierService.check_plan_active(weird_user) is True

def test_reset_ai_usage_if_needed(mock_db):
    old_date = date.today() - timedelta(days=1)
    usage = UsageLimit(user_id=1, ai_calls_used=10, ai_calls_reset_date=old_date)
    
    TierService.reset_ai_usage_if_needed(usage, mock_db)
    
    assert usage.ai_calls_used == 0
    assert usage.ai_calls_reset_date == date.today()
    mock_db.commit.assert_called_once()
    
    # Test no reset needed
    mock_db.reset_mock()
    usage.ai_calls_used = 5
    TierService.reset_ai_usage_if_needed(usage, mock_db)
    assert usage.ai_calls_used == 5 # Should not change
    mock_db.commit.assert_not_called()

def test_check_ai_limit_flow(mock_db, free_user, expired_pro_user):
    # 1. Expired plan
    can_proceed, info = TierService.check_ai_limit(expired_pro_user, mock_db)
    assert can_proceed is False
    assert info["error"] == "plan_expired"
    
    # 2. New Usage Record Creation
    # Mock query returning None first
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    can_proceed, info = TierService.check_ai_limit(free_user, mock_db)
    
    # Verify usage created
    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called
    
    # Since we mocked usage creation implicitly (the function creates it),
    # but our mock_db.query...first() returned None, the function proceeds to create `usage = UsageLimit(...)`
    # and continues. However, `usage` variable inside the function is a real object now.
    # The logic `if not usage: ... db.refresh(usage)` implies `usage` becomes a managed object.
    # In a unit test with mocks, we need to inspect what happened.
    # The function continues to `TierService.reset_ai_usage_if_needed` and `limit` check.
    # Since the new usage has ai_calls_used=0, it should pass.
    assert can_proceed is True
    
    # 3. Limit Reached
    usage_mock = MagicMock(spec=UsageLimit)
    usage_mock.ai_calls_used = settings.FREE_AI_LIMIT
    usage_mock.ai_calls_reset_date = date.today()
    mock_db.query.return_value.filter.return_value.first.return_value = usage_mock
    
    can_proceed, info = TierService.check_ai_limit(free_user, mock_db)
    assert can_proceed is False
    assert info["error"] == "limit_reached"
    
    # 4. Limit Not Reached
    usage_mock.ai_calls_used = settings.FREE_AI_LIMIT - 1
    can_proceed, info = TierService.check_ai_limit(free_user, mock_db)
    assert can_proceed is True
    assert info["remaining"] == 1

def test_increment_ai_usage(mock_db, free_user):
    usage_mock = MagicMock(spec=UsageLimit)
    usage_mock.ai_calls_used = 0
    mock_db.query.return_value.filter.return_value.first.return_value = usage_mock
    
    TierService.increment_ai_usage(free_user, mock_db)
    
    assert usage_mock.ai_calls_used == 1
    mock_db.commit.assert_called()

def test_can_use_feature(free_user, pro_user, ultimate_user):
    assert TierService.can_use_feature(free_user, "pdf_no_watermark") is False
    assert TierService.can_use_feature(pro_user, "pdf_no_watermark") is True
    assert TierService.can_use_feature(ultimate_user, "advanced_tone") is True
    assert TierService.can_use_feature(pro_user, "advanced_tone") is False
    
def test_upgrade_downgrade_user(mock_db, free_user):
    # Setup mock to return the user
    mock_db.query.return_value.filter.return_value.first.return_value = free_user
    
    # Upgrade
    expiry = datetime.utcnow() + timedelta(days=365)
    updated_user = upgrade_user_plan(free_user.id, PlanTier.PRO, expiry, mock_db)
    
    assert updated_user.plan == PlanTier.PRO
    assert updated_user.plan_expires_at == expiry
    mock_db.commit.assert_called()
    
    # Downgrade
    downgraded_user = downgrade_user_plan(free_user.id, mock_db)
    assert downgraded_user.plan == PlanTier.FREE
    assert downgraded_user.plan_expires_at is None
    
def test_user_not_found_upgrade_downgrade(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc:
        upgrade_user_plan(999, PlanTier.PRO, datetime.utcnow(), mock_db)
    assert exc.value.status_code == 404
    
    with pytest.raises(HTTPException) as exc:
        downgrade_user_plan(999, mock_db)
    assert exc.value.status_code == 404
