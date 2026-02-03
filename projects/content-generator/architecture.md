# Content Generator - Architecture

## System Overview

Content Generator is a multi-stage AI pipeline that transforms YouTube transcripts into production-ready content. The architecture emphasizes reliability, cost-efficiency, and operational visibility.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Content Generator Pipeline                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   YouTube    │───▶│  Transcript  │───▶│     AI       │                  │
│  │    Sync      │    │    Queue     │    │   Analysis   │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │  PostgreSQL  │    │    Retry     │    │   OpenAI     │                  │
│  │   Staging    │    │    Logic     │    │   Service    │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│         │                                       │                           │
│         ▼                                       ▼                           │
│  ┌──────────────┐                       ┌──────────────┐                   │
│  │    Draft     │◀──────────────────────│  Validation  │                   │
│  │   Service    │                       │    Chain     │                   │
│  └──────────────┘                       └──────────────┘                   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Staging    │───▶│   Review     │───▶│  Publisher   │                  │
│  │   Service    │    │   Workflow   │    │   Service    │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│                                                 │                           │
│                                                 ▼                           │
│                                          ┌──────────────┐                   │
│                                          │  Firestore   │                   │
│                                          │    + GCS     │                   │
│                                          └──────────────┘                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. YouTube Sync Service

**Responsibility:** Fetches videos, metadata, and transcripts from YouTube channels/playlists.

**Key Features:**
- Channel and playlist synchronization
- Video metadata extraction
- Transcript fetching via youtube-transcript-api
- Rate limit handling with Retry-After support

```python
# Workflow
fetch_channel_videos() → store_video_metadata() → queue_transcript_import()
```

### 2. Transcript Queue Service

**Responsibility:** Manages transcript import with retry scheduling.

**Key Features:**
- Queue-based processing
- Exponential backoff with jitter
- Max retry limits
- Status tracking (pending, processing, completed, failed)

**Retry Formula:**
```python
delay = base_delay * (2 ** retry_count) * (1 ± 0.1)  # With jitter
max_delay = 300  # 5 minutes cap
```

### 3. Prompt Builder Service

**Responsibility:** Assembles layered prompts for AI generation.

**Key Features:**
- Template-based system (Markdown files)
- Variable interpolation (`{{variable_name}}`)
- Content-type specific prompts
- Context injection (taxonomy, difficulty, instance)

**Prompt Layers:**
1. **System Prompts** - Instructions from templates
2. **User Prompts** - Content requests with metadata
3. **Context Injection** - Taxonomy, content type, difficulty

### 4. OpenAI Service

**Responsibility:** Handles OpenAI API calls with structured outputs.

**Key Features:**
- JSON schema enforcement via `response_format`
- Configurable model selection
- Token usage tracking
- Cost estimation
- Retry with exponential backoff

**Structured Output Configuration:**
```python
response_format={
    "type": "json_schema",
    "json_schema": {
        "name": schema_name,
        "schema": schema,
        "strict": False
    }
}
```

### 5. Content Validator Service

**Responsibility:** Multi-layer validation for content quality.

**5-Layer Validation Chain:**

| Layer | Timing | Purpose | Implementation |
|-------|--------|---------|----------------|
| 1. Taxonomy | Pre-API | Fail-fast | `taxonomy_validator.py` |
| 2. Schema | During | Structure | OpenAI `json_schema` |
| 3. Content | Post | Quality | `content_validator_service.py` |
| 4. Pydantic | Pre-save | Types | Pydantic models |
| 5. Publisher | Pre-publish | Firestore | `publisher/content_validator.py` |

**Validation Checks:**
- Placeholder text detection (regex patterns)
- Minimum content length (1000+ chars for descriptions)
- Required field validation
- Structure validation (sections, modules, lessons)
- Educational language enforcement

### 6. Draft Services

**Responsibility:** Manages content drafts in PostgreSQL.

**Content Types:**
- `ArticleDraftService`
- `CourseDraftService`
- `QuizDraftService`
- `AudioDraftService`
- `VideoDraftService`

**Draft Lifecycle:**
```
create() → update() → mark_ready_to_stage() → stage_to_content()
```

### 7. Staging Service

**Responsibility:** Manages content review workflow.

**Status Workflow:**
```
Draft → Staged (draft) → Approved → Published
```

### 8. Publisher Service

**Responsibility:** Publishes approved content to Firestore and GCS.

**Publishing Pipeline:**
1. Validate content (5th layer)
2. Upload thumbnail to GCS
3. Write content document to Firestore
4. Upload transcript (non-blocking)
5. Update status to 'published'

## Data Flow

### Content Generation Flow

```
1. YouTube Sync
   └── fetch_and_store_videos() → video_metadata table

2. Transcript Import
   └── queue_transcript_import() → transcript_queue table
   └── process_queue() → transcript_text field

3. AI Analysis
   └── build_analysis_prompt() → OpenAI API
   └── validate_response() → analysis_data (JSONB)

4. Content Generation
   └── build_*_prompt() → OpenAI API
   └── validate_*() → Post-processing
   └── create_draft() → *_drafts table

5. Staging
   └── mark_ready_to_stage() → stage_to_content()
   └── staged_content table (status: 'draft')

6. Review & Approval
   └── User review → approve_content()
   └── (status: 'approved')

7. Publishing
   └── publish_content() → Firestore + GCS
   └── (status: 'published')
```

## Database Schema

### PostgreSQL (Staging)

```
video_metadata
├── id (UUID)
├── youtube_id (VARCHAR)
├── title, description
├── transcript_text (TEXT)
├── analysis_data (JSONB)
└── processing_status

transcript_queue
├── id (UUID)
├── video_id (FK)
├── status (pending, processing, completed, failed)
├── retry_count
├── next_retry_at
└── error_message

article_drafts / course_drafts / quiz_drafts
├── id (UUID)
├── instance_id
├── content (JSONB)
├── status
└── created_at, updated_at

staged_content
├── id (UUID)
├── instance_id
├── content_type
├── content (JSONB)
├── status (draft, approved, published)
└── timestamps

content_operations
├── id (UUID)
├── content_id (FK)
├── operation_type (publish, delete)
├── status (pending, in_progress, completed, failed)
├── started_at, completed_at
└── error_message
```

### Firestore (Production)

Published content writes to Nandi Platform's Firestore:
- `content/{contentId}` - Content documents
- `instances/{instanceId}/transcripts/{transcriptId}` - Transcript metadata

### Google Cloud Storage

Media files uploaded to instance-specific paths:
```
{instanceId}/content/{filename}
{instanceId}/thumbnails/{filename}
{instanceId}/transcripts/{filename}
```

## Retry & Error Handling

### OpenAI Service Retry

```python
def generate_with_retry(prompt, schema):
    for attempt in range(max_attempts):
        try:
            return call_openai(prompt, schema)
        except RateLimitError:
            delay = base_delay * (2 ** attempt)
            sleep(delay)
        except APITimeoutError:
            delay = base_delay * (2 ** attempt)
            sleep(delay)
        except JSONDecodeError:
            # Add stricter prompt and retry
            prompt = add_json_enforcement(prompt)
```

### Transcript Queue Retry

```python
def schedule_retry(queue_item):
    retry_count = queue_item.retry_count + 1
    if retry_count > max_retries:
        mark_failed(queue_item)
        return
    
    delay = base_delay * (2 ** retry_count)
    delay *= random.uniform(0.9, 1.1)  # Jitter
    delay = min(delay, 300)  # Cap at 5 minutes
    
    queue_item.next_retry_at = now() + delay
    queue_item.retry_count = retry_count
```

## Operational Metrics

### Token Usage Tracking

```python
class OpenAIService:
    total_tokens_used: int = 0
    total_requests: int = 0
    failed_requests: int = 0
    
    def get_usage_stats(self):
        return {
            "total_tokens_used": self.total_tokens_used,
            "total_requests": self.total_requests,
            "success_rate": (total - failed) / total,
            "estimated_cost": self._calculate_cost()
        }
```

### Health Monitoring

```python
class HealthMonitoringService:
    def get_health_status(self):
        return {
            "success_rate_24h": calculate_rate(24h),
            "success_rate_7d": calculate_rate(7d),
            "success_rate_30d": calculate_rate(30d),
            "error_counts": get_error_counts(),
            "status": "healthy" | "degraded" | "unhealthy"
        }
```

## Design Patterns

### Singleton Services

Services use singleton pattern for shared state:
- `OpenAIService` - Token tracking across requests
- `HealthMonitoringService` - Centralized metrics

### Strategy Pattern

Cleanup strategies for different content types:
- `DefaultCleanupStrategy`
- `PageCleanupStrategy`
- `EmbedCleanupStrategy`

### Factory Pattern

Draft service factory for content type selection:
```python
def get_draft_service(content_type):
    services = {
        "article": ArticleDraftService,
        "course": CourseDraftService,
        "quiz": QuizDraftService,
    }
    return services[content_type]()
```

## Security Considerations

- API keys stored in environment variables
- No sensitive data in logs
- Sanitized error messages
- Rate limiting respected
- Fail-fast on invalid input

## Performance Optimizations

- **Fail-fast validation**: Taxonomy check before API calls
- **Token limits**: Content-type specific max tokens
- **Queue-based processing**: Handles rate limits gracefully
- **Batch operations**: Bulk publishing for approved content
- **Connection pooling**: PostgreSQL connection management
