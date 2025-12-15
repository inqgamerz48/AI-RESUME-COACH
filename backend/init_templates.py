"""
Template Initialization Script
Loads 50+ resume templates into the database
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.template import ResumeTemplate
from app.services.template_data import RESUME_TEMPLATES


def init_templates():
    """Initialize resume templates in database"""
    print("🎨 Initializing Resume Templates...")
    
    db = SessionLocal()
    
    try:
        # Check if templates already exist
        existing_count = db.query(ResumeTemplate).count()
        
        if existing_count > 0:
            print(f"⚠️  Found {existing_count} existing templates")
            response = input("Do you want to reload all templates? (y/n): ")
            if response.lower() != 'y':
                print("❌ Cancelled")
                return
            
            # Delete existing templates
            db.query(ResumeTemplate).delete()
            db.commit()
            print("🗑️  Deleted existing templates")
        
        # Insert new templates
        count = 0
        for template_data in RESUME_TEMPLATES:
            template = ResumeTemplate(**template_data)
            db.add(template)
            count += 1
        
        db.commit()
        print(f"✅ Successfully loaded {count} templates!")
        
        # Print summary by industry
        from sqlalchemy import func
        print("\n📊 Templates by Industry:")
        industries = db.query(
            ResumeTemplate.industry,
            func.count(ResumeTemplate.id)
        ).group_by(ResumeTemplate.industry).all()
        
        for industry, count in industries:
            print(f"   {industry}: {count} templates")
        
        print("\n📊 Templates by Tier:")
        tiers = db.query(
            ResumeTemplate.tier_required,
            func.count(ResumeTemplate.id)
        ).group_by(ResumeTemplate.tier_required).all()
        
        for tier, count in tiers:
            print(f"   {tier}: {count} templates")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_templates()
