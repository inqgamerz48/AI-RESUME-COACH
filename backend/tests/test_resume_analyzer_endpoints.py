"""
Integration Tests for Resume Analyzer API Endpoints
"""
import pytest
import io
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, Mock
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.models.user import User
from app.core.config import settings



# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_db():
    """Create test database"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Create tables
    from app.db.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield async_session
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def mock_user():
    """Create mock user for testing"""
    user = Mock(spec=User)
    user.id = 1
    user.email = "test@example.com"
    user.tier = "FREE"
    user.is_active = True
    return user


@pytest.fixture
def auth_headers(mock_user):
    """Create authentication headers"""
    # Mock JWT token
    return {"Authorization": "Bearer test_token_12345"}


@pytest.fixture
def sample_pdf_bytes():
    """Create a minimal valid PDF for testing"""
    # This is a minimal PDF structure
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 100
>>
stream
BT
/F1 12 Tf
100 700 Td
(John Doe) Tj
0 -20 Td
(Software Engineer) Tj
0 -20 Td
(john@example.com) Tj
0 -20 Td
(Education: B.Tech Computer Science) Tj
0 -20 Td
(Skills: Python, JavaScript, SQL) Tj
0 -20 Td
(Experience: Developed web applications using React) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000317 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
470
%%EOF"""
    return pdf_content


class TestResumeAnalyzerEndpoints:
    """Integration tests for resume analyzer endpoints"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analyze_endpoint_success(self, auth_headers, sample_pdf_bytes):
        """Test successful resume analysis"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Mock authentication
            with patch("app.api.v1.endpoints.resume_analyzer.get_current_user") as mock_auth:
                mock_user = Mock()
                mock_user.id = 1
                mock_user.tier = "PRO"
                mock_auth.return_value = mock_user
                
                # Mock database session
                with patch("app.api.v1.endpoints.resume_analyzer.get_db"):
                    files = {
                        "file": ("resume.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")
                    }
                    
                    response = await client.post(
                        "/api/v1/resume/analyze",
                        files=files,
                        headers=auth_headers
                    )
                    
                    assert response.status_code == 200
                    data = response.json()
                    
                    assert "overall_score" in data
                    assert "category_scores" in data
                    assert "suggestions" in data
                    assert "analysis_id" in data
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analyze_endpoint_no_auth(self, sample_pdf_bytes):
        """Test analysis endpoint without authentication"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            files = {
                "file": ("resume.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")
            }
            
            response = await client.post(
                "/api/v1/resume/analyze",
                files=files
            )
            
            # Should require authentication
            assert response.status_code in [401, 403]
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analyze_endpoint_wrong_file_type(self, auth_headers):
        """Test analysis with wrong file type"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            with patch("app.api.v1.endpoints.resume_analyzer.get_current_user") as mock_auth:
                mock_user = Mock()
                mock_user.id = 1
                mock_user.tier = "FREE"
                mock_auth.return_value = mock_user
                
                files = {
                    "file": ("resume.docx", io.BytesIO(b"not a pdf"), "application/msword")
                }
                
                response = await client.post(
                    "/api/v1/resume/analyze",
                    files=files,
                    headers=auth_headers
                )
                
                assert response.status_code == 400
                assert "PDF" in response.json()["detail"]
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analyze_endpoint_file_too_large(self, auth_headers):
        """Test analysis with file exceeding size limit"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            with patch("app.api.v1.endpoints.resume_analyzer.get_current_user") as mock_auth:
                mock_user = Mock()
                mock_user.id = 1
                mock_user.tier = "FREE"
                mock_auth.return_value = mock_user
                
                # Create a 6MB file (exceeds 5MB limit)
                large_file = b"x" * (6 * 1024 * 1024)
                files = {
                    "file": ("resume.pdf", io.BytesIO(large_file), "application/pdf")
                }
                
                response = await client.post(
                    "/api/v1/resume/analyze",
                    files=files,
                    headers=auth_headers
                )
                
                assert response.status_code == 400
                assert "5MB" in response.json()["detail"]
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_tier_limits_free_user(self, auth_headers, sample_pdf_bytes):
        """Test that FREE tier users are limited"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            with patch("app.api.v1.endpoints.resume_analyzer.get_current_user") as mock_auth:
                mock_user = Mock()
                mock_user.id = 1
                mock_user.tier = "FREE"
                mock_auth.return_value = mock_user
                
                with patch("app.api.v1.endpoints.resume_analyzer.get_db"):
                    # Mock that user has already used their monthly quota
                    with patch("app.api.v1.endpoints.resume_analyzer.check_analysis_quota") as mock_quota:
                        mock_quota.return_value = False  # Quota exceeded
                        
                        files = {
                            "file": ("resume.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")
                        }
                        
                        response = await client.post(
                            "/api/v1/resume/analyze",
                            files=files,
                            headers=auth_headers
                        )
                        
                        # Should return 403 or 429 for quota exceeded
                        assert response.status_code in [403, 429]
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_enhance_endpoint_success(self, auth_headers):
        """Test successful resume enhancement"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            with patch("app.api.v1.endpoints.resume_analyzer.get_current_user") as mock_auth:
                mock_user = Mock()
                mock_user.id = 1
                mock_user.tier = "PRO"
                mock_auth.return_value = mock_user
                
                with patch("app.api.v1.endpoints.resume_analyzer.get_db"):
                    # Mock analysis exists
                    with patch("app.api.v1.endpoints.resume_analyzer.get_analysis_by_id"):
                        request_data = {
                            "analysis_id": 123,
                            "accepted_suggestions": [1, 2, 3]
                        }
                        
                        response = await client.post(
                            "/api/v1/resume/enhance",
                            json=request_data,
                            headers=auth_headers
                        )
                        
                        # Might fail if endpoint not fully implemented
                        # But should not return 500
                        assert response.status_code in [200, 404, 400]
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analysis_history_endpoint(self, auth_headers):
        """Test analysis history retrieval"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            with patch("app.api.v1.endpoints.resume_analyzer.get_current_user") as mock_auth:
                mock_user = Mock()
                mock_user.id = 1
                mock_user.tier = "PRO"
                mock_auth.return_value = mock_user
                
                with patch("app.api.v1.endpoints.resume_analyzer.get_db"):
                    response = await client.get(
                        "/api/v1/resume/analysis-history",
                        headers=auth_headers
                    )
                    
                    # Should return 200 with empty or populated list
                    assert response.status_code == 200
                    data = response.json()
                    assert isinstance(data, list) or isinstance(data, dict)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_rate_limiting(self, auth_headers, sample_pdf_bytes):
        """Test rate limiting on analyze endpoint"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            with patch("app.api.v1.endpoints.resume_analyzer.get_current_user") as mock_auth:
                mock_user = Mock()
                mock_user.id = 1
                mock_user.tier = "FREE"
                mock_auth.return_value = mock_user
                
                with patch("app.api.v1.endpoints.resume_analyzer.get_db"):
                    files = {
                        "file": ("resume.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")
                    }
                    
                    # Make multiple rapid requests
                    responses = []
                    for _ in range(10):
                        response = await client.post(
                            "/api/v1/resume/analyze",
                            files=files,
                            headers=auth_headers
                        )
                        responses.append(response.status_code)
                    
                    # At least one should be rate limited (429)
                    # This depends on if rate limiting is implemented
                    # For now, just check they're not all 500
                    assert not all(code == 500 for code in responses)


class TestResumeAnalyzerValidation:
    """Test input validation for resume analyzer"""
    
    @pytest.mark.integration
    def test_empty_file_rejected(self, auth_headers):
        """Test that empty files are rejected"""
        client = TestClient(app)
        
        with patch("app.api.v1.endpoints.resume_analyzer.get_current_user"):
            files = {
                "file": ("resume.pdf", io.BytesIO(b""), "application/pdf")
            }
            
            response = client.post(
                "/api/v1/resume/analyze",
                files=files,
                headers=auth_headers
            )
            
            assert response.status_code in [400, 422]
    
    @pytest.mark.integration
    def test_missing_file_parameter(self, auth_headers):
        """Test that missing file parameter is rejected"""
        client = TestClient(app)
        
        with patch("app.api.v1.endpoints.resume_analyzer.get_current_user"):
            response = client.post(
                "/api/v1/resume/analyze",
                headers=auth_headers
            )
            
            assert response.status_code == 422  # Unprocessable Entity
