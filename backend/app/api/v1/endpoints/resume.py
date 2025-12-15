"""
Resume CRUD endpoints with tier enforcement.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume
from app.schemas.schemas import ResumeCreate, ResumeUpdate, ResumeResponse
from app.services.tier_service import TierService
from app.services.pdf_service import PDFService
from app.api.dependencies import get_current_user


router = APIRouter()


@router.post("/resume", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
def create_resume(
    resume_data: ResumeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new resume.
    Enforces tier-based resume count limits.
    """
    # Check resume limit
    can_proceed, info = TierService.check_resume_limit(current_user, db)
    if not can_proceed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=info)
    
    # Create resume
    resume = Resume(
        user_id=current_user.id,
        title=resume_data.title,
        template_id=resume_data.template_id,
        content={
            "personal_info": resume_data.personal_info.dict(),
            "summary": resume_data.summary,
            "education": [edu.dict() for edu in resume_data.education],
            "skills": resume_data.skills,
            "projects": [proj.dict() for proj in resume_data.projects]
        }
    )
    
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # Increment resume count
    TierService.increment_resume_count(current_user, db)
    
    return resume


@router.get("/resume", response_model=List[ResumeResponse])
def get_user_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all resumes for current user.
    """
    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id,
        Resume.is_active == 1
    ).all()
    
    return resumes


@router.get("/resume/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific resume.
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id,
        Resume.is_active == 1
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return resume


@router.put("/resume/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: int,
    resume_data: ResumeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a resume.
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id,
        Resume.is_active == 1
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Update fields
    if resume_data.title is not None:
        resume.title = resume_data.title
    if resume_data.template_id is not None:
        resume.template_id = resume_data.template_id
    if resume_data.content is not None:
        resume.content = resume_data.content
    
    db.commit()
    db.refresh(resume)
    
    return resume


@router.delete("/resume/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete a resume.
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id,
        Resume.is_active == 1
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume.is_active = 0
    db.commit()
    
    return None


@router.get("/resume/{resume_id}/pdf")
def export_resume_pdf(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export resume as PDF.
    FREE tier: WITH watermark
    PRO/ULTIMATE: NO watermark
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id,
        Resume.is_active == 1
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Generate PDF
    pdf_buffer = PDFService.generate_resume_pdf(resume.content, current_user.plan)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=resume_{resume_id}.pdf"
        }
    )
