"""
Unit Tests for PDF Parser Service
"""
import pytest
import io
from unittest.mock import Mock, AsyncMock, patch
from fastapi import HTTPException, UploadFile
import PyPDF2

from app.services.pdf_parser_service import PDFParserService


class TestPDFParserService:
    """Test suite for PDFParserService"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_pdf_success(self):
        """Test successful PDF validation"""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "resume.pdf"
        mock_file.read = AsyncMock(return_value=b"PDF content" * 100)
        mock_file.seek = AsyncMock()
        
        # Should not raise exception
        await PDFParserService.validate_pdf(mock_file)
        mock_file.seek.assert_called_once_with(0)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_pdf_wrong_extension(self):
        """Test PDF validation fails with wrong extension"""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "resume.docx"
        
        with pytest.raises(HTTPException) as exc_info:
            await PDFParserService.validate_pdf(mock_file)
        
        assert exc_info.value.status_code == 400
        assert "Only PDF files are allowed" in exc_info.value.detail
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_pdf_too_large(self):
        """Test PDF validation fails when file is too large"""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "resume.pdf"
        # 6MB file (exceeds 5MB limit)
        mock_file.read = AsyncMock(return_value=b"x" * (6 * 1024 * 1024))
        mock_file.seek = AsyncMock()
        
        with pytest.raises(HTTPException) as exc_info:
            await PDFParserService.validate_pdf(mock_file)
        
        assert exc_info.value.status_code == 400
        assert "must not exceed 5MB" in exc_info.value.detail
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_validate_pdf_empty_file(self):
        """Test PDF validation fails when file is empty"""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "resume.pdf"
        mock_file.read = AsyncMock(return_value=b"")
        mock_file.seek = AsyncMock()
        
        with pytest.raises(HTTPException) as exc_info:
            await PDFParserService.validate_pdf(mock_file)
        
        assert exc_info.value.status_code == 400
        assert "File is empty" in exc_info.value.detail
    
    @pytest.mark.unit
    def test_identify_section_education(self):
        """Test section identification for education"""
        assert PDFParserService._identify_section("Education") == "education"
        assert PDFParserService._identify_section("ACADEMIC BACKGROUND") == "education"
        assert PDFParserService._identify_section("Qualifications") == "education"
    
    @pytest.mark.unit
    def test_identify_section_experience(self):
        """Test section identification for experience"""
        assert PDFParserService._identify_section("Work Experience") == "experience"
        assert PDFParserService._identify_section("EMPLOYMENT") == "experience"
        assert PDFParserService._identify_section("Internship") == "experience"
    
    @pytest.mark.unit
    def test_identify_section_no_match(self):
        """Test section identification returns None for no match"""
        assert PDFParserService._identify_section("This is a very long line that is not a section header") is None
        assert PDFParserService._identify_section("Random text") is None
    
    @pytest.mark.unit
    def test_parse_resume_structure_basic(self):
        """Test basic resume structure parsing"""
        text = """John Doe
john.doe@email.com
+1-234-567-8900

Education
B.Tech Computer Science
XYZ University

Skills
Python, JavaScript, SQL
"""
        result = PDFParserService.parse_resume_structure(text)
        
        assert "john.doe@email.com" in result["contact"]
        assert "+1-234-567-8900" in result["contact"]
        assert "B.Tech" in result["education"]
        assert "Python" in result["skills"]
    
    @pytest.mark.unit
    def test_extract_key_metrics_basic(self):
        """Test key metrics extraction"""
        text = """Email: test@example.com
Phone: 123-456-7890
LinkedIn: linkedin.com/in/johndoe

Developed web application
Improved performance by 30%
Led team of 5 developers
Increased user engagement by 50%
"""
        metrics = PDFParserService.extract_key_metrics(text)
        
        assert metrics["has_email"] is True
        assert metrics["has_phone"] is True
        assert metrics["has_linkedin"] is True
        assert metrics["action_verbs"] >= 3  # developed, improved, led, increased
        assert metrics["quantifiable_achievements"] >= 2  # 30%, 50%, 5
    
    @pytest.mark.unit
    def test_extract_key_metrics_missing_contact(self):
        """Test metrics extraction with missing contact info"""
        text = "Just some random resume content without contact details"
        metrics = PDFParserService.extract_key_metrics(text)
        
        assert metrics["has_email"] is False
        assert metrics["has_phone"] is False
        assert metrics["has_linkedin"] is False
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_extract_text_from_pdf_insufficient_text(self):
        """Test extraction fails when PDF has insufficient text"""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.read = AsyncMock(return_value=b"Short")
        mock_file.seek = AsyncMock()
        
        # Mock PyPDF2 to return very short text
        with patch('PyPDF2.PdfReader') as mock_reader:
            mock_page = Mock()
            mock_page.extract_text.return_value = "Hi"
            mock_reader.return_value.pages = [mock_page]
            
            with pytest.raises(HTTPException) as exc_info:
                await PDFParserService.extract_text_from_pdf(mock_file)
            
            # Can be 400 or 500 depending on the error type
            assert exc_info.value.status_code in [400, 500]
            assert "Could not extract sufficient text" in exc_info.value.detail or "Error processing PDF" in exc_info.value.detail
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_extract_text_from_pdf_corrupted(self):
        """Test extraction fails with corrupted PDF"""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.read = AsyncMock(return_value=b"Not a valid PDF")
        mock_file.seek = AsyncMock()
        
        with pytest.raises(HTTPException) as exc_info:
            await PDFParserService.extract_text_from_pdf(mock_file)
        
        assert exc_info.value.status_code == 400
        assert "Invalid or corrupted PDF" in exc_info.value.detail
    
    @pytest.mark.unit
    def test_word_count_metric(self):
        """Test word count calculation"""
        text = "This is a sample resume with ten words here now"
        metrics = PDFParserService.extract_key_metrics(text)
        assert metrics["word_count"] == 10
    
    @pytest.mark.unit
    def test_bullet_points_metric(self):
        """Test bullet point counting"""
        text = """
• First achievement
• Second achievement  
- Third point
- Fourth point
"""
        metrics = PDFParserService.extract_key_metrics(text)
        assert metrics["bullet_points"] == 4
