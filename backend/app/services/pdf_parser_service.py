"""
PDF Parser Service - Extract and parse resume content from PDF files.
"""
import re
import io
from typing import Dict, List, Optional, Tuple
from fastapi import HTTPException, UploadFile
import PyPDF2
from app.core.security import sanitize_input


class PDFParserService:
    """Service for parsing resume PDFs and extracting structured content."""
    
    # Common resume section keywords
    SECTION_KEYWORDS = {
        "contact": ["contact", "personal", "information", "details"],
        "summary": ["summary", "objective", "profile", "about"],
        "education": ["education", "academic", "qualification", "degree"],
        "experience": ["experience", "work", "employment", "internship"],
        "projects": ["projects", "work samples", "portfolio"],
        "skills": ["skills", "technical", "competencies", "expertise"],
        "achievements": ["achievements", "awards", "certifications", "honors"],
        "extra": ["extra", "curricular", "activities", "volunteer"]
    }
    
    @staticmethod
    async def validate_pdf(file: UploadFile) -> None:
        """
        Validate uploaded PDF file.
        
        Args:
            file: Uploaded file object
            
        Raises:
            HTTPException: If validation fails
        """
        # Check file extension
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        
        # Check file size (max 5MB)
        content = await file.read()
        file_size = len(content)
        await file.seek(0)  # Reset file pointer
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=400,
                detail="File size must not exceed 5MB"
            )
        
        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )
    
    @staticmethod
    async def extract_text_from_pdf(file: UploadFile) -> str:
        """
        Extract raw text from PDF file.
        
        Args:
            file: Uploaded PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            HTTPException: If PDF parsing fails
        """
        try:
            # Read file content
            content = await file.read()
            await file.seek(0)  # Reset for potential reuse
            
            # Create PDF reader
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            
            # Extract text from all pages
            extracted_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text() + "\n"
            
            # Clean and validate
            extracted_text = extracted_text.strip()
            
            if not extracted_text or len(extracted_text) < 100:
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract sufficient text from PDF. The file may be image-based or corrupted."
                )
            
            return extracted_text
        
        except PyPDF2.errors.PdfReadError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid or corrupted PDF file: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF: {str(e)}"
            )
    
    @staticmethod
    def _identify_section(line: str) -> Optional[str]:
        """
        Identify which section a line belongs to based on keywords.
        
        Args:
            line: Line of text to analyze
            
        Returns:
            Section name or None
        """
        line_lower = line.lower().strip()
        
        # Check if line is a section header (typically short and contains keywords)
        if len(line) < 50:  # Section headers are usually short
            for section, keywords in PDFParserService.SECTION_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in line_lower:
                        return section
        
        return None
    
    @staticmethod
    def parse_resume_structure(text: str) -> Dict:
        """
        Parse extracted text into structured resume sections.
        
        Args:
            text: Raw extracted text from PDF
            
        Returns:
            Dictionary with parsed resume sections
        """
        lines = text.split('\n')
        
        parsed_data = {
            "contact": [],
            "summary": [],
            "education": [],
            "experience": [],
            "projects": [],
            "skills": [],
            "achievements": [],
            "extra": [],
            "unclassified": []
        }
        
        current_section = "unclassified"
        
        # Email and phone patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            detected_section = PDFParserService._identify_section(line)
            if detected_section:
                current_section = detected_section
                continue
            
            # Extract contact information
            if re.search(email_pattern, line):
                parsed_data["contact"].append(line)
                continue
            
            if re.search(phone_pattern, line):
                parsed_data["contact"].append(line)
                continue
            
            # Add line to current section
            parsed_data[current_section].append(line)
        
        # Clean up: join lines in each section
        for section in parsed_data:
            if parsed_data[section]:
                parsed_data[section] = '\n'.join(parsed_data[section])
            else:
                parsed_data[section] = ""
        
        return parsed_data
    
    @staticmethod
    def extract_key_metrics(text: str) -> Dict:
        """
        Extract key metrics from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with extracted metrics
        """
        metrics = {
            "word_count": len(text.split()),
            "bullet_points": text.count('•') + text.count('-'),
            "quantifiable_achievements": 0,
            "action_verbs": 0,
            "has_email": False,
            "has_phone": False,
            "has_linkedin": False
        }
        
        # Count numbers (potential quantifiable achievements)
        number_pattern = r'\b\d+%?|\d+\+|\$\d+'
        metrics["quantifiable_achievements"] = len(re.findall(number_pattern, text))
        
        # Common action verbs in resumes
        action_verbs = [
            "developed", "created", "implemented", "designed", "built", "managed",
            "led", "achieved", "improved", "increased", "reduced", "optimized",
            "analyzed", "coordinated", "executed", "launched", "delivered"
        ]
        
        text_lower = text.lower()
        for verb in action_verbs:
            if verb in text_lower:
                metrics["action_verbs"] += 1
        
        # Check for contact information
        metrics["has_email"] = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        metrics["has_phone"] = bool(re.search(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}', text))
        metrics["has_linkedin"] = "linkedin" in text_lower
        
        return metrics
    
    @staticmethod
    async def process_resume_pdf(file: UploadFile) -> Tuple[str, Dict, Dict]:
        """
        Complete PDF processing pipeline.
        
        Args:
            file: Uploaded PDF file
            
        Returns:
            Tuple of (extracted_text, parsed_structure, metrics)
        """
        # Validate PDF
        await PDFParserService.validate_pdf(file)
        
        # Extract text
        extracted_text = await PDFParserService.extract_text_from_pdf(file)
        
        # Parse structure
        parsed_structure = PDFParserService.parse_resume_structure(extracted_text)
        
        # Extract metrics
        metrics = PDFParserService.extract_key_metrics(extracted_text)
        
        return extracted_text, parsed_structure, metrics
