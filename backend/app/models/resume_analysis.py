"""
Resume Analysis model for storing analysis history and suggestions.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Original PDF Info
    original_filename = Column(String, nullable=False)
    original_file_path = Column(String, nullable=True)  # Temporary storage path
    
    # Extracted Content
    extracted_text = Column(Text, nullable=False)
    parsed_content = Column(JSON, nullable=True)  # Structured resume data
    
    # Analysis Results
    overall_score = Column(Float, default=0.0)  # 0-100 score
    ats_score = Column(Float, default=0.0)
    content_score = Column(Float, default=0.0)
    structure_score = Column(Float, default=0.0)
    
    # AI Suggestions (categorized)
    suggestions = Column(JSON, nullable=False)  # Array of suggestion objects
    """
    Suggestion structure:
    {
        "category": "content_quality|ats_optimization|structure|fresher_specific",
        "section": "summary|experience|education|skills|projects",
        "severity": "critical|high|medium|low",
        "issue": "Description of the issue",
        "suggestion": "Improvement suggestion",
        "original_text": "Text to be replaced",
        "enhanced_text": "Suggested replacement",
        "accepted": false|true
    }
    """
    
    # Enhanced Resume (if user accepted changes)
    enhanced_resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    accepted_suggestions = Column(JSON, nullable=True)  # IDs of accepted suggestions
    
    # Metadata
    status = Column(String, default="pending")  # pending|completed|enhanced|failed
    is_active = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resume_analyses")
    enhanced_resume = relationship("Resume", foreign_keys=[enhanced_resume_id])
