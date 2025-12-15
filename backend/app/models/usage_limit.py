"""
Usage limits tracking model for tier enforcement.
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.db.base_class import Base


class UsageLimit(Base):
    __tablename__ = "usage_limits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # AI Usage Tracking
    ai_calls_used = Column(Integer, default=0)
    ai_calls_reset_date = Column(Date, default=date.today)
    
    # Resume Count
    resume_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="usage_limits")
