"""
Resume storage model.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Resume Data
    title = Column(String, default="My Resume")
    template_id = Column(Integer, ForeignKey("resume_templates.id"), default=1)  # References template table
    
    # Resume Content (stored as JSON)
    content = Column(JSON, nullable=False)  # Full resume structure
    
    # Metadata
    is_active = Column(Integer, default=1)  # Soft delete
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
