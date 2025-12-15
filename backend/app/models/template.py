from sqlalchemy import Column, Integer, String, Text, Boolean, JSON
from app.db.base_class import Base


class ResumeTemplate(Base):
    """Resume Template Model"""
    __tablename__ = "resume_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Template categorization
    industry = Column(String(50))  # Tech, Finance, Healthcare, etc.
    position_type = Column(String(50))  # Entry-level, Mid-level, Senior, Executive
    category = Column(String(50))  # Modern, Classic, Creative, Minimal, etc.
    
    # Template settings (JSON)
    # Example: {"font": "Helvetica", "color_scheme": "blue", "layout": "two-column"}
    settings = Column(JSON)
    
    # Preview image URL
    preview_image = Column(String(255))
    
    # Template tier requirement
    tier_required = Column(String(20), default="FREE")  # FREE, PRO, ULTIMATE
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Popularity (for sorting)
    usage_count = Column(Integer, default=0)
