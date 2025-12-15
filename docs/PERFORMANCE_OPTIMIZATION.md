# Resume Analyzer - Performance Optimization Guide

## Overview
This guide outlines performance considerations and optimization strategies for the Resume Analyzer feature.

## Current Performance Metrics

### Target Benchmarks
- PDF Upload & Parsing: < 2 seconds
- AI Analysis & Scoring: < 5 seconds  
- Total Analysis Time: < 8 seconds
- Enhanced PDF Generation: < 3 seconds

## Optimization Areas

### 1. PDF Processing

#### Current Implementation
```python
# Synchronous PDF parsing
pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
```

#### Optimization Strategies

**A. Lazy Loading**
```python
# Only extract text from pages as needed
async def extract_text_lazy(file: UploadFile) -> AsyncGenerator:
    for page in pdf_reader.pages:
        yield page.extract_text()
```

**B. Parallel Page Processing**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def extract_text_parallel(pdf_reader):
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, page.extract_text)
            for page in pdf_reader.pages
        ]
        results = await asyncio.gather(*tasks)
    return '\\n'.join(results)
```

**C. Caching**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def parse_section(section_text: str) -> Dict:
    # Cache frequently analyzed sections
    pass
```

### 2. AI Service Optimization

#### Current Bottleneck
- Multiple sequential AI calls for enhancements
- Network latency to Hugging Face API

#### Optimization Strategies

**A. Batch AI Requests**
```python
async def batch_ai_enhance(suggestions: List[Dict]) -> List[Dict]:
    # Combine multiple enhancement requests into one
    combined_prompt = "\\n\\n".join([
        f"Section {i}: {s['original_text']}"
        for i, s in enumerate(suggestions)
    ])
    
    response = await AIService._call_huggingface_async(combined_prompt)
    # Split response back to individual suggestions
    return parse_batch_response(response)
```

**B. Async AI Calls**
```python
async def generate_ai_enhancements_async(suggestions: List[Dict]):
    tasks = [
        AIService._call_huggingface_async(build_prompt(s))
        for s in suggestions
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

**C. Response Streaming**
```python
async def stream_analysis_results(analysis_id: int):
    """Stream results as they become available"""
    yield {"status": "parsing", "progress": 20}
    yield {"status": "analyzing", "progress": 50}
    yield {"status": "complete", "progress": 100, "results": results}
```

### 3. Database Optimization

#### Current Queries
```python
# Potentially slow: Loading full analysis history
analyses = await db.query(ResumeAnalysis).filter_by(user_id=user.id).all()
```

#### Optimization Strategies

**A. Pagination**
```python
async def get_analysis_history(
    user_id: int,
    page: int = 1,
    page_size: int = 10
):
    offset = (page - 1) * page_size
    return await db.query(ResumeAnalysis)\\
        .filter_by(user_id=user_id)\\
        .limit(page_size)\\
        .offset(offset)\\
        .all()
```

**B. Select Specific Fields**
```python
# Instead of loading entire object
analyses = await db.query(
    ResumeAnalysis.id,
    ResumeAnalysis.created_at,
    ResumeAnalysis.overall_score
).filter_by(user_id=user_id).all()
```

**C. Indexing**
```python
# Add indexes to frequently queried fields
class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"
    
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
```

### 4. Caching Strategy

#### Response Caching
```python
from aiocache import cached

@cached(ttl=3600)  # Cache for 1 hour
async def get_common_suggestions(resume_type: str) -> List[Dict]:
    """Cache frequently used suggestion templates"""
    pass
```

#### Redis Integration (Future)
```python
import aioredis

redis = aioredis.from_url("redis://localhost")

async def cache_analysis(analysis_id: int, result: Dict):
    await redis.setex(
        f"analysis:{analysis_id}",
        3600,  # 1 hour TTL
        json.dumps(result)
    )
```

### 5. Frontend Optimization

#### A. Lazy Component Loading
```javascript
// Lazy load heavy components
const AnalysisResults = lazy(() => import('./components/AnalysisResults'));
const EnhancementSummary = lazy(() => import('./components/EnhancementSummary'));
```

#### B. Debounced File Upload
```javascript
const debouncedUpload = useCallback(
  debounce(async (file) => {
    await uploadResume(file);
  }, 500),
  []
);
```

#### C. Progress Indication
```javascript
// Show real-time progress during analysis
const [progress, setProgress] = useState(0);

useEffect(() => {
  const interval = setInterval(async () => {
    const status = await checkAnalysisStatus(analysisId);
    setProgress(status.progress);
  }, 1000);
  
  return () => clearInterval(interval);
}, [analysisId]);
```

### 6. File Upload Optimization

#### A. Chunked Upload (for large files)
```python
@app.post("/api/v1/resume/upload-chunk")
async def upload_chunk(
    chunk: UploadFile,
    chunk_number: int,
    total_chunks: int,
    upload_id: str
):
    # Store chunk
    await save_chunk(upload_id, chunk_number, chunk)
    
    # If last chunk, assemble file
    if chunk_number == total_chunks - 1:
        await assemble_file(upload_id)
```

#### B. Pre-validation
```python
@app.post("/api/v1/resume/validate")
async def validate_resume_metadata(
    filename: str,
    file_size: int
):
    """Validate before upload to save bandwidth"""
    if not filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files allowed")
    if file_size > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    return {"valid": True}
```

### 7. Memory Management

#### A. Stream Large PDFs
```python
async def process_large_pdf_stream(file: UploadFile):
    """Process PDF in chunks to avoid loading entire file in memory"""
    chunk_size = 1024 * 1024  # 1MB chunks
    
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        process_chunk(chunk)
```

#### B. Cleanup Temporary Files
```python
@app.on_event("startup")
async def start_cleanup_task():
    """Background task to clean up old uploaded files"""
    asyncio.create_task(cleanup_old_files())

async def cleanup_old_files():
    while True:
        # Delete files older than 24 hours
        cutoff = datetime.utcnow() - timedelta(hours=24)
        delete_files_before(cutoff)
        await asyncio.sleep(3600)  # Run every hour
```

## Monitoring & Profiling

### 1. Add Performance Logging
```python
import time
from functools import wraps

def track_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper

@track_performance
async def analyze_resume(...):
    pass
```

### 2. Prometheus Metrics (Future)
```python
from prometheus_client import Counter, Histogram

analysis_duration = Histogram(
    'resume_analysis_duration_seconds',
    'Time spent analyzing resume'
)

@analysis_duration.time()
async def analyze_resume(...):
    pass
```

### 3. APM Integration
```python
# New Relic, DataDog, or similar
import newrelic.agent

@newrelic.agent.function_trace()
async def analyze_resume(...):
    pass
```

## Load Testing

### Using Locust
```python
# locustfile.py
from locust import HttpUser, task, between

class ResumeAnalyzerUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def analyze_resume(self):
        files = {'file': open('test_resume.pdf', 'rb')}
        self.client.post(
            "/api/v1/resume/analyze",
            files=files,
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    def on_start(self):
        # Login and get token
        response = self.client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password"
        })
        self.token = response.json()["access_token"]
```

Run: `locust -f locustfile.py --headless --users 100 --spawn-rate 10`

## Recommended Implementation Priority

### Phase 1: Quick Wins (Week 1)
1. ✅ Add database indexes
2. ✅ Implement pagination for history
3. ✅ Add performance logging
4. ⏳ Enable response compression

### Phase 2: Medium Impact (Week 2)
1. ⏳ Implement caching for common suggestions
2. ⏳ Add progress indicators on frontend  
3. ⏳ Optimize AI batch requests
4. ⏳ Add file validation before upload

### Phase 3: Advanced (Week 3+)
1. ⏳ Redis caching layer
2. ⏳ Async AI processing
3. ⏳ CDN for static assets
4. ⏳ Load balancing setup

## Performance Testing Checklist

- [ ] Test with 1KB PDF
- [ ] Test with 5MB PDF (max size)
- [ ] Test with corrupted PDF
- [ ] Test with image-only PDF
- [ ] Test with 100 concurrent users
- [ ] Test analysis history with 1000+ records
- [ ] Test under rate limiting
- [ ] Profile memory usage
- [ ] Monitor database query time
- [ ] Check API response times

## Success Metrics

| Operation | Current | Target | Optimized |
|-----------|---------|--------|-----------|
| PDF Upload | ~1s | <2s | ⏳ TBD |
| Text Extraction | ~1s | <2s | ⏳ TBD |
| Analysis | ~3s | <5s | ⏳ TBD |
| AI Enhancement | ~5s | <3s | ⏳ TBD |
| Total E2E | ~10s | <8s | ⏳ TBD |

## Resources

- [FastAPI Performance](https://fastapi.tiangolo.com/async/)
- [SQLAlchemy Performance](https://docs.sqlalchemy.org/en/14/faq/performance.html)
- [Python Async Best Practices](https://realpython.com/async-io-python/)
- [Load Testing Guide](https://locust.io/)
