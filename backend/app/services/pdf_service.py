"""
PDF Export Service
Generates ATS-safe PDF resumes with watermark for FREE tier.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from io import BytesIO
from typing import Dict
from app.models.user import PlanTier


class PDFService:
    """Service for generating ATS-safe PDF resumes."""
    
    @staticmethod
    def generate_resume_pdf(resume_data: Dict, user_plan: PlanTier) -> BytesIO:
        """
        Generate PDF resume.
        FREE tier: WITH watermark
        PRO/ULTIMATE tier: NO watermark
        """
        buffer = BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.black,
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        section_style = ParagraphStyle(
            'Section',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.black,
            spaceAfter=6,
            spaceBefore=12
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.black,
            spaceAfter=8
        )
        
        # Build content
        content = []
        
        # Header - Name
        name = resume_data.get("personal_info", {}).get("name", "Your Name")
        content.append(Paragraph(name.upper(), title_style))
        
        # Contact Info
        email = resume_data.get("personal_info", {}).get("email", "")
        phone = resume_data.get("personal_info", {}).get("phone", "")
        contact_text = f"{email} | {phone}"
        content.append(Paragraph(contact_text, body_style))
        content.append(Spacer(1, 0.2*inch))
        
        # Summary (if exists)
        summary = resume_data.get("summary", "")
        if summary:
            content.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
            content.append(Paragraph(summary, body_style))
            content.append(Spacer(1, 0.1*inch))
        
        # Education
        if "education" in resume_data and resume_data["education"]:
            content.append(Paragraph("EDUCATION", section_style))
            for edu in resume_data["education"]:
                edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')}<br/>{edu.get('year', '')}"
                content.append(Paragraph(edu_text, body_style))
        
        # Skills
        if "skills" in resume_data and resume_data["skills"]:
            content.append(Paragraph("SKILLS", section_style))
            skills_text = ", ".join(resume_data["skills"])
            content.append(Paragraph(skills_text, body_style))
        
        # Projects
        if "projects" in resume_data and resume_data["projects"]:
            content.append(Paragraph("PROJECTS", section_style))
            for project in resume_data["projects"]:
                proj_text = f"<b>{project.get('name', '')}</b><br/>{project.get('description', '')}"
                content.append(Paragraph(proj_text, body_style))
        
        # Watermark for FREE tier
        if user_plan == PlanTier.FREE:
            content.append(Spacer(1, 0.3*inch))
            watermark_style = ParagraphStyle(
                'Watermark',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            content.append(Paragraph("Created with AI Resume Coach - Upgrade to remove watermark", watermark_style))
        
        # Build PDF
        doc.build(content)
        buffer.seek(0)
        
        return buffer
