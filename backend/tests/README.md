# Resume Analyzer Tests

## Quick Start

```bash
# Run all tests
cd backend
source venv/bin/activate
pytest

# Run with coverage
pytest --cov=app

# Run only unit tests
pytest -m unit

# Run specific test file
pytest tests/test_pdf_parser_service.py
```

## Test Files

### `test_pdf_parser_service.py` (14 tests)
Tests the PDF parsing functionality:
- File validation (PDF format, size limits)
- Text extraction from PDFs
- Resume section identification
- Metrics extraction (action verbs, achievements, contact info)

### `test_resume_analyzer_service.py` (17 tests)
Tests the resume analysis logic:
- Content quality scoring
- ATS optimization checks
- Structure analysis
- Fresher-specific validations
- AI enhancement generation
- Overall scoring calculation

### `test_resume_analyzer_endpoints.py` (Integration)
Tests the API endpoints:
- Authentication & authorization
- File upload handling
- Tier-based access control
- Rate limiting
- Error handling

## Test Coverage

Target: 70% minimum (enforced)  
Current: Services at 100% coverage

## Writing Tests

Example unit test:
```python
@pytest.mark.unit
def test_your_feature():
    # Arrange
    input_data = {"key": "value"}
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected_value
```

Example async test:
```python
@pytest.mark.asyncio
async def test_async_feature():
    result = await async_function()
    assert result is not None
```

## See Also

- Full Testing Guide: `/docs/TESTING_GUIDE.md`
- Performance Guide: `/docs/PERFORMANCE_OPTIMIZATION.md`
- Feature Spec: `/RESUME_ANALYZER_FEATURE.md`
