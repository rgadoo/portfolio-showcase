# Content Generator - Tech Stack

## Overview

Content Generator is built with Python and integrates multiple AI services and cloud infrastructure for production-grade content generation.

---

## Core Language

### Python 3.11+

**Why Python:**
- Rich AI/ML ecosystem
- Excellent API client libraries
- Strong typing with Pydantic
- FastAPI for high-performance APIs

**Key Libraries:**
- `pydantic` - Data validation and settings
- `httpx` - Async HTTP client
- `python-dotenv` - Environment configuration

---

## AI & LLM

### OpenAI API

**Models Used:**
| Model | Use Case | Cost |
|-------|----------|------|
| `gpt-4o-mini` | Default generation | ~$0.375/1M tokens |
| `gpt-4o` | High-quality content | ~$10/1M tokens |
| `gpt-4-turbo` | Maximum capability | ~$15/1M tokens |

**Features Used:**
- **Chat Completions** - Text generation
- **Structured Outputs** - JSON schema enforcement
- **DALL·E 3** - Hero image generation
- **TTS** - Text-to-speech

**Why OpenAI:**
- Best-in-class structured output support
- Consistent JSON schema enforcement
- Reliable API with good rate limits
- Cost-effective mini model option

### ElevenLabs (Optional)

**Use Case:** Premium voice synthesis

**Why ElevenLabs:**
- Natural-sounding voices
- Multiple voice options
- Good API reliability

---

## Backend Framework

### FastAPI

**Why FastAPI:**
- High performance (Starlette + Pydantic)
- Automatic OpenAPI documentation
- Native async support
- Type hints integration

**Key Features Used:**
- Dependency injection
- Request validation
- Background tasks
- Middleware support

---

## Database

### PostgreSQL

**Use Case:** Staging database for drafts, queues, operations

**Why PostgreSQL:**
- JSONB support for flexible content storage
- Robust transaction support
- Excellent performance
- Production-proven reliability

**Key Tables:**
- `video_metadata` - YouTube video data
- `transcript_queue` - Processing queue
- `*_drafts` - Content drafts by type
- `staged_content` - Review workflow
- `content_operations` - Audit trail

### Database Patterns

**Connection Pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10
)
```

**Manager Pattern:**
- `VideoMetadataManager`
- `TranscriptQueueManager`
- `DraftManager`
- `StagedContentManager`

---

## Data Validation

### Pydantic

**Why Pydantic:**
- Runtime type validation
- JSON schema generation
- Settings management
- Excellent error messages

**Usage:**
```python
class ArticleContent(BaseModel):
    title: str = Field(min_length=10)
    description: str = Field(min_length=100)
    sections: List[Section]
    
    @validator('title')
    def validate_title(cls, v):
        if '[placeholder]' in v.lower():
            raise ValueError('Contains placeholder')
        return v
```

### JSON Schema (OpenAI)

**Structured Output Configuration:**
```python
response_format={
    "type": "json_schema",
    "json_schema": {
        "name": "article_schema",
        "schema": ARTICLE_SCHEMA,
        "strict": False
    }
}
```

**Benefits:**
- Guaranteed JSON structure
- Reduced retries
- Consistent output format

---

## External Integrations

### YouTube Data API v3

**Use Case:** Video synchronization and transcript fetching

**Endpoints Used:**
- `channels.list` - Channel information
- `playlistItems.list` - Playlist videos
- `videos.list` - Video details

**Transcript Fetching:**
```python
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript(video_id)
```

### Firebase Admin SDK

**Use Case:** Publishing to Nandi Platform's Firestore

**Operations:**
- Document creation
- Batch writes
- Transaction support

**Configuration:**
```python
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)
db = firestore.client()
```

### Google Cloud Storage

**Use Case:** Media file storage

**Operations:**
- File upload with content type
- Instance-specific path management
- Public URL generation

**Configuration:**
```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)
blob = bucket.blob(f"{instance_id}/content/{filename}")
blob.upload_from_string(data, content_type=mime_type)
```

---

## Architecture Patterns

### Singleton Pattern

**Use Case:** Shared service state (token tracking, metrics)

```python
class OpenAIService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.total_tokens = 0
        return cls._instance
```

### Strategy Pattern

**Use Case:** Content-type specific cleanup strategies

```python
class CleanupStrategy(ABC):
    @abstractmethod
    def cleanup(self, content: dict) -> dict:
        pass

class ArticleCleanupStrategy(CleanupStrategy):
    def cleanup(self, content: dict) -> dict:
        # Article-specific cleanup
        return content
```

### Factory Pattern

**Use Case:** Draft service selection

```python
def get_draft_service(content_type: str) -> BaseDraftService:
    services = {
        "article": ArticleDraftService,
        "course": CourseDraftService,
        "quiz": QuizDraftService,
    }
    return services[content_type]()
```

### Queue Pattern

**Use Case:** Transcript processing with retry

```python
class TranscriptQueueService:
    def enqueue(self, video_id: str):
        # Add to queue with pending status
        
    def process_next(self):
        # Get next pending item
        # Process with retry on failure
        
    def schedule_retry(self, item, error):
        # Calculate backoff and reschedule
```

---

## Error Handling

### Retry with Exponential Backoff

```python
def retry_with_backoff(func, max_attempts=3, base_delay=1):
    for attempt in range(max_attempts):
        try:
            return func()
        except RateLimitError:
            delay = base_delay * (2 ** attempt)
            delay *= random.uniform(0.9, 1.1)  # Jitter
            time.sleep(delay)
    raise MaxRetriesExceeded()
```

### Custom Exceptions

```python
class ContentGeneratorError(Exception):
    """Base exception for content generator"""

class ValidationError(ContentGeneratorError):
    """Content validation failed"""

class GenerationError(ContentGeneratorError):
    """AI generation failed"""

class PublishingError(ContentGeneratorError):
    """Publishing to Firestore/GCS failed"""
```

---

## Configuration Management

### Environment Variables

```bash
# AI Services
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_RETRY_ATTEMPTS=3

# Database
DATABASE_URL=postgresql://...

# Firebase
FIREBASE_SERVICE_ACCOUNT_PATH=./service-account.json

# GCS
GCS_BUCKET=nandi-content

# Instance
DEFAULT_INSTANCE_ID=lightofvedanta
```

### Pydantic Settings

```python
class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_retry_attempts: int = 3
    database_url: str
    gcs_bucket: str
    
    class Config:
        env_file = ".env"
```

---

## Development Tools

### Code Quality
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `mypy` - Type checking

### Testing
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting

### Documentation
- Markdown templates for prompts
- OpenAPI via FastAPI
- Inline docstrings

---

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start server
uvicorn main:app --reload
```

### Production Considerations

- **Secrets:** Environment variables or Secret Manager
- **Database:** Managed PostgreSQL (Cloud SQL)
- **Scaling:** Horizontal scaling for queue processing
- **Monitoring:** Health endpoints, metrics export

---

## Tech Stack Summary

| Category | Technology |
|----------|------------|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic |
| **AI** | OpenAI (GPT-4o, DALL·E, TTS) |
| **Voice** | ElevenLabs (optional) |
| **Storage** | Google Cloud Storage |
| **Publishing** | Firebase Admin SDK |
| **YouTube** | YouTube Data API v3 |
