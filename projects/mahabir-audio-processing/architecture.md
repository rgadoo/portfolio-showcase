# Architecture

This document describes the architecture of Mahabir Audio Processing - a Flask-based web application for transcribing and correcting spiritual audio lectures.

## System Overview

The application follows a service-oriented architecture with a clear separation between web interface, business logic, and data persistence layers.

## Architecture Principles

1. **Service-Oriented Design**: Modular services for each workflow step
2. **Two-Stage Processing**: Local correction + optional AI enhancement
3. **Manager Pattern**: Specialized database managers for each entity
4. **Async Processing**: Background processing for long-running tasks
5. **Cost Optimization**: Efficient API usage with pre-filtering

## System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Flask Web Interface                  │
│              (User Interface Layer)                     │
│  - Routes: transcription, entry management             │
│  - Templates: Bootstrap-based responsive UI             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Service Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │Transcription│  │  Correction  │  │    Media    │ │
│  │   Service   │  │   Service    │  │   Service   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │    Local     │  │   OpenAI     │                    │
│  │  Processor   │  │   Client     │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Database Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Transcript  │  │  Processed   │  │ Correction  │ │
│  │   Manager    │  │   Entry      │  │  Pattern    │ │
│  │              │  │   Manager    │  │  Manager    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                         │
│  - raw_transcripts                                       │
│  - processed_entries                                     │
│  - correction_patterns                                   │
│  - media_files                                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 External Services                        │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │   Whisper    │  │   OpenAI     │                    │
│  │   (Local)    │  │   (API)      │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

## Core Services

### 1. TranscriptionService

**Purpose**: Transcribe audio/video files using OpenAI Whisper

**Key Features**:
- Multiple model support (tiny, base, small, medium, large)
- Thread-safe model loading
- Memory management and cleanup
- SRT format generation
- Database integration

**Process**:
1. Load Whisper model (with thread safety)
2. Transcribe audio file
3. Format as SRT
4. Save to database
5. Trigger correction workflow

### 2. CorrectionService

**Purpose**: Orchestrate two-stage correction workflow

**Two-Stage Workflow**:

**Stage 1: Local Processing**
```python
def process_srt_file(self, file_id: int):
    # Parse SRT entries
    # Process locally with Sanskrit corrector
    # Mark entries needing OpenAI
    # Update database
```

**Stage 2: OpenAI Processing**
```python
def process_entries_with_openai(self, file_id: int, entry_ids: List[int]):
    # Get selected entries
    # Batch for API efficiency
    # Send to OpenAI
    # Update corrections
```

**Key Features**:
- Batch processing for efficiency
- Cost tracking and estimation
- Progress reporting
- Error recovery

### 3. LocalProcessor

**Purpose**: Local Sanskrit correction using dictionary

**Process**:
1. Load correction patterns from database
2. Apply corrections to text
3. Calculate confidence scores
4. Identify entries needing OpenAI

**Decision Logic**:
- Low confidence corrections → needs OpenAI
- Complex patterns → needs OpenAI
- High confidence → local correction sufficient

### 4. OpenAIClient

**Purpose**: OpenAI API integration for enhanced corrections

**Features**:
- Batch processing
- Context windows (surrounding entries)
- Cost estimation
- Retry logic
- Error handling

### 5. MediaService

**Purpose**: Manage audio/video files

**Features**:
- File type detection
- File system integration
- Database association
- Metadata extraction

## Database Architecture

### Manager Pattern

Each entity type has a specialized manager:

- **TranscriptManager** - Raw transcript operations
- **ProcessedEntryManager** - Entry processing operations
- **CorrectionPatternManager** - Pattern learning
- **MediaManager** - Media file operations
- **ReviewManager** - Human review tracking

### Database Schema

**Core Tables**:
- `raw_transcripts` - Uploaded SRT files
- `processed_entries` - Processed transcript entries
- `correction_patterns` - Learning patterns
- `media_files` - Associated media files
- `human_reviews` - Review tracking

### Connection Management

- Connection pooling
- Automatic reconnection
- Transaction management
- Error handling with rollback

## Web Application Architecture

### Flask Application Structure

```
web/
├── app.py                 # Main Flask app
├── transcription_routes.py  # Transcription endpoints
├── entry_routes.py        # Entry management
└── templates/            # Jinja2 templates
```

### Route Organization

- **Main Routes** (`app.py`): Home, upload, transcript detail, review
- **Transcription Routes** (`transcription_routes.py`): Audio transcription
- **Entry Routes** (`entry_routes.py`): Individual entry management

### Template Structure

- **Base Template**: Bootstrap-based responsive layout
- **Component Templates**: Reusable UI components
- **Page Templates**: Feature-specific pages

## Two-Stage Correction Workflow

### Workflow Diagram

```
Upload SRT/Media
    ↓
Transcribe (if audio)
    ↓
Parse SRT Entries
    ↓
Stage 1: Local Processing
    ├── Apply Sanskrit dictionary
    ├── Calculate confidence
    └── Mark entries needing OpenAI
    ↓
User Review
    ├── Review flagged entries
    └── Select entries for OpenAI
    ↓
Stage 2: OpenAI Processing (Optional)
    ├── Batch selected entries
    ├── Send to OpenAI API
    └── Update corrections
    ↓
Final Review & Export
```

### Cost Optimization

- **Pre-filtering**: Local processing reduces API calls
- **Batch Processing**: Efficient API usage
- **Selective Processing**: User chooses which entries need AI
- **Cost Tracking**: Real-time cost estimation

## Async Processing

### Background Processing

- Long-running transcription tasks
- Batch correction processing
- File upload handling
- Progress tracking

### Thread Safety

- Model loading with locks
- Database connection pooling
- Resource cleanup

## Deployment Architecture

### Google Cloud Platform

- **Cloud Run**: Containerized Flask app
- **Cloud SQL**: Managed PostgreSQL
- **Cloud Storage**: Media file storage (optional)

### Container Configuration

- Docker-based deployment
- Environment variable configuration
- Cloud SQL proxy integration
- Resource allocation (memory, CPU)

## Security

### Input Validation

- File type validation
- File size limits
- Path traversal prevention
- SQL injection prevention (parameterized queries)

### API Security

- Environment variable secrets
- Secure file serving
- Error message sanitization

## Performance Optimizations

### Database

- Connection pooling
- Indexed queries
- Batch operations
- Efficient JSON handling

### Memory Management

- Model cleanup after use
- Garbage collection
- Resource cleanup
- Efficient file handling

### Processing

- Batch operations
- Async processing
- Progress tracking
- Error recovery

## Future Enhancements

- Multi-language support
- Advanced speaker diarization
- Real-time transcription
- API for programmatic access
- Enhanced pattern learning

---

**Last Updated:** December 2024
