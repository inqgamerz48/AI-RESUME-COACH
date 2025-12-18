"""
Resume Analyzer API endpoints with tier enforcement.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.user import User
from app.models.resume_analysis import ResumeAnalysis
from app.models.resume import Resume
from app.schemas.schemas import ResumeAnalysisResponse, EnhanceResumeRequest
from app.services.tier_service import TierService
from app.services.pdf_parser_service import PDFParserService
from app.services.resume_analyzer_service import ResumeAnalyzerService
from app.services.pdf_service import PDFService
from app.api.dependencies import get_current_user
import os
import shutil


router = APIRouter()


@router.post("/resume/analyze", response_model=dict, status_code=status.HTTP_200_OK)
async def analyze_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and analyze a resume PDF.
    
    Tier Limits:
    - FREE: 1 analysis/month
    - PRO: 5 analyses/month
    - ULTIMATE: Unlimited
    
    Returns:
    - Analysis ID
    - Overall score
    - Category scores
    - List of suggestions
    """
    # Check tier-based analysis limits
    analysis_limits = {
        "FREE": 1,
        "PRO": 5,
        "ULTIMATE": 999999
    }
    
    limit = analysis_limits.get(current_user.plan, 1)
    
    # Count analyses in current month
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    analyses_this_month = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.user_id == current_user.id,
        ResumeAnalysis.created_at >= month_start,
        ResumeAnalysis.is_active == 1
    ).count()
    
    if analyses_this_month >= limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Monthly analysis limit reached. Your plan allows {limit} analysis/analyses per month. Upgrade to analyze more resumes."
        )
    
    try:
        # Process PDF
        extracted_text, parsed_structure, metrics = await PDFParserService.process_resume_pdf(file)
        
        # Save uploaded file temporarily (optional - for 24 hours)
        upload_dir = "uploads/resumes"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"user_{current_user.id}_{datetime.utcnow().timestamp()}.pdf")
        
        await file.seek(0)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Perform AI analysis
        analysis_results = await ResumeAnalyzerService.analyze_resume(
            parsed_structure,
            metrics,
            current_user.plan
        )
        
        # Create analysis record
        analysis = ResumeAnalysis(
            user_id=current_user.id,
            original_filename=file.filename,
            original_file_path=file_path,
            extracted_text=extracted_text[:10000],  # Limit stored text
            parsed_content=parsed_structure,
            overall_score=analysis_results["overall_score"],
            ats_score=analysis_results["category_scores"]["ats_optimization"],
            content_score=analysis_results["category_scores"]["content_quality"],
            structure_score=analysis_results["category_scores"]["structure"],
            suggestions=analysis_results["suggestions"],
            status="completed"
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return {
            "analysis_id": analysis.id,
            "filename": file.filename,
            "overall_score": analysis_results["overall_score"],
            "category_scores": analysis_results["category_scores"],
            "suggestions": analysis_results["suggestions"],
            "total_suggestions": analysis_results["total_suggestions"],
            "critical_issues": analysis_results["critical_issues"],
            "metrics": analysis_results["metrics"],
            "created_at": analysis.created_at.isoformat(),
            "tier_info": {
                "current_plan": current_user.plan,
                "analyses_used": analyses_this_month + 1,
                "analyses_limit": limit
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing resume: {str(e)}"
        )


@router.post("/resume/enhance/{analysis_id}", status_code=status.HTTP_200_OK)
async def enhance_resume(
    analysis_id: int,
    accepted_suggestions: List[int],  # List of suggestion indices to accept
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate enhanced resume based on accepted suggestions.
    
    Args:
        analysis_id: ID of the resume analysis
        accepted_suggestions: List of suggestion indices user wants to apply
        
    Returns:
        Enhanced resume ID and details
    """
    try:
        # Get analysis record
        analysis = db.query(ResumeAnalysis).filter(
            ResumeAnalysis.id == analysis_id,
            ResumeAnalysis.user_id == current_user.id,
            ResumeAnalysis.is_active == 1
        ).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        if analysis.status != "completed":
            raise HTTPException(status_code=400, detail="Analysis is not completed")
        
        # Validate accepted suggestions
        suggestions = analysis.suggestions
        if not isinstance(suggestions, list):
            raise HTTPException(status_code=400, detail="Invalid suggestions format")
        
        # Mark accepted suggestions - safely handle parsed_content
        enhanced_content = dict(analysis.parsed_content) if analysis.parsed_content else {}
        accepted_changes = []
        
        for idx in accepted_suggestions:
            if 0 <= idx < len(suggestions):
                suggestion = suggestions[idx]
                suggestion["accepted"] = True
                accepted_changes.append(suggestion)
                
                # Apply enhancement to content
                section = suggestion["section"]
                if suggestion.get("enhanced_text") and section in enhanced_content:
                    # Replace original text with enhanced text
                    if suggestion.get("original_text"):
                        enhanced_content[section] = str(enhanced_content.get(section, "")).replace(
                            suggestion["original_text"],
                            suggestion["enhanced_text"]
                        )
                    else:
                        # If no original text, append enhancement
                        if enhanced_content.get(section):
                            enhanced_content[section] += "\n" + suggestion["enhanced_text"]
                        else:
                            enhanced_content[section] = suggestion["enhanced_text"]
        
        # Check resume creation limit
        can_proceed, info = TierService.check_resume_limit(current_user, db)
        if not can_proceed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=info
            )
        
        # Create enhanced resume
        enhanced_resume = Resume(
            user_id=current_user.id,
            title=f"Enhanced - {analysis.original_filename}",
            template_id=None,  # No template required for analyzer-generated resumes
            content={
                "personal_info": {
                    "contact": enhanced_content.get("contact", "")
                },
                "summary": enhanced_content.get("summary", ""),
                "education": enhanced_content.get("education", ""),
                "skills": enhanced_content.get("skills", "").split(",") if enhanced_content.get("skills") else [],
                "projects": enhanced_content.get("projects", ""),
                "experience": enhanced_content.get("experience", ""),
                "achievements": enhanced_content.get("achievements", "")
            }
        )
        
        db.add(enhanced_resume)
        db.commit()
        db.refresh(enhanced_resume)
        
        # Update analysis record
        analysis.enhanced_resume_id = enhanced_resume.id
        analysis.accepted_suggestions = accepted_suggestions
        analysis.status = "enhanced"
        analysis.suggestions = suggestions  # Save updated suggestions with accepted flags
        db.commit()
        
        # Increment resume count
        TierService.increment_resume_count(current_user, db)
        
        return {
            "enhanced_resume_id": enhanced_resume.id,
            "analysis_id": analysis.id,
            "accepted_changes": len(accepted_changes),
            "total_suggestions": len(suggestions),
            "message": "Resume enhanced successfully",
            "download_url": f"/api/v1/resume/{enhanced_resume.id}/pdf"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.error(f"Enhancement error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error enhancing resume: {str(e)}"
        )


@router.get("/resume/analysis-history", response_model=List[dict])
def get_analysis_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's resume analysis history.
    
    Tier Limits:
    - FREE: Last 1 analysis
    - PRO: Last 10 analyses
    - ULTIMATE: All analyses
    """
    history_limits = {
        "FREE": 1,
        "PRO": 10,
        "ULTIMATE": 999999
    }
    
    limit = history_limits.get(current_user.plan, 1)
    
    analyses = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.user_id == current_user.id,
        ResumeAnalysis.is_active == 1
    ).order_by(ResumeAnalysis.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": analysis.id,
            "filename": analysis.original_filename,
            "overall_score": analysis.overall_score,
            "ats_score": analysis.ats_score,
            "content_score": analysis.content_score,
            "structure_score": analysis.structure_score,
            "total_suggestions": len(analysis.suggestions) if analysis.suggestions else 0,
            "status": analysis.status,
            "enhanced_resume_id": analysis.enhanced_resume_id,
            "created_at": analysis.created_at.isoformat()
        }
        for analysis in analyses
    ]


@router.get("/resume/analysis/{analysis_id}", response_model=dict)
def get_analysis_details(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed analysis results for a specific analysis.
    """
    analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.id == analysis_id,
        ResumeAnalysis.user_id == current_user.id,
        ResumeAnalysis.is_active == 1
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "id": analysis.id,
        "filename": analysis.original_filename,
        "overall_score": analysis.overall_score,
        "category_scores": {
            "ats_optimization": analysis.ats_score,
            "content_quality": analysis.content_score,
            "structure": analysis.structure_score
        },
        "suggestions": analysis.suggestions,
        "parsed_content": analysis.parsed_content,
        "status": analysis.status,
        "enhanced_resume_id": analysis.enhanced_resume_id,
        "created_at": analysis.created_at.isoformat()
    }


@router.delete("/resume/analysis/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a resume analysis (soft delete).
    """
    analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.id == analysis_id,
        ResumeAnalysis.user_id == current_user.id,
        ResumeAnalysis.is_active == 1
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Soft delete
    analysis.is_active = 0
    db.commit()
    
    # Clean up temporary file if exists
    if analysis.original_file_path and os.path.exists(analysis.original_file_path):
        try:
            os.remove(analysis.original_file_path)
        except Exception as e:
            import logging
            logging.warning(f"Failed to delete analysis file {analysis.original_file_path}: {str(e)}")
    
    return None
