# Mahabir Audio Processing

A production-ready Flask web application for transcribing and processing spiritual audio lectures using OpenAI Whisper AI and specialized Sanskrit text correction.

**🔗 Quick Links:** [Architecture](./architecture.md) | [Features](./features.md) | [Code Samples](./code-samples/) | [Case Studies](./case-studies/)

## Overview

Mahabir Audio Processing automates the transcription and correction of spiritual audio/video content, specifically designed to handle Sanskrit terms that are commonly mistranscribed by standard speech-to-text systems. The application uses a two-stage correction workflow to efficiently process transcripts while maintaining high accuracy.

## Project Statistics

| Metric | Value |
|--------|-------|
| **Total Commits** | 22+ |
| **Python Files** | 38+ |
| **Lines of Code** | ~1,035+ (Python) |
| **Services** | 8+ core services |
| **Database Tables** | 5+ PostgreSQL tables |
| **Web Routes** | 15+ Flask routes |

## Key Features

- **AI-Powered Transcription**: Automatic transcription using OpenAI Whisper/WhisperX
- **Two-Stage Correction**: Local Sanskrit correction + optional OpenAI enhancement
- **Web Interface**: User-friendly Flask web application for transcript management
- **Media Player Integration**: Synchronized audio/video playback with transcripts
- **Batch Processing**: Efficient handling of large audio files
- **Pattern Learning**: Database-driven correction pattern learning
- **Human Review Workflow**: Quality control interface for corrections
- **Cloud Deployment**: Production-ready deployment on Google Cloud Run

## Technologies Used

### Backend
- **Python 3.11+** - Core language
- **Flask 3.0** - Web framework
- **PostgreSQL 15** - Database (Cloud SQL in production)
- **OpenAI Whisper** - Audio transcription
- **WhisperX** - Enhanced transcription with speaker diarization

### Infrastructure
- **Google Cloud Run** - Containerized deployment
- **Cloud SQL** - Managed PostgreSQL database
- **Cloud Storage** - Media file storage (optional)

### AI/ML
- **OpenAI Whisper** - Speech-to-text transcription
- **WhisperX** - Enhanced transcription features
- **OpenAI GPT** - Text correction enhancement (optional)

## Architecture Highlights

### Two-Stage Correction Workflow

1. **Stage 1: Local Processing**
   - Sanskrit dictionary-based corrections
   - Pattern matching and replacement
   - Identifies entries needing AI processing

2. **Stage 2: OpenAI Enhancement** (Optional)
   - User-selected entries sent to OpenAI
   - Context-aware corrections
   - Cost-optimized batch processing

### Service-Oriented Design

- **TranscriptionService** - Whisper integration
- **CorrectionService** - Two-stage workflow orchestration
- **LocalProcessor** - Sanskrit correction engine
- **OpenAIClient** - API integration
- **MediaService** - File management

### Database Architecture

- **Manager Pattern** - Specialized managers for each entity
- **Connection Pooling** - Efficient database connections
- **Pattern Learning** - Correction pattern storage and retrieval

## Features

### Transcription
- Multiple Whisper model support (tiny → large)
- Automatic language detection
- SRT format output
- Batch processing capabilities

### Correction
- Sanskrit term dictionary
- Pattern learning system
- Confidence scoring
- Human review interface

### Web Interface
- Transcript management dashboard
- Media player with synchronization
- Review and approval workflow
- Export functionality

## Production Status

**Status:** Production-ready  
**Deployment:** Google Cloud Run  
**Database:** Cloud SQL (PostgreSQL)

## Documentation

- [Architecture](./architecture.md) - System design and architecture
- [Features](./features.md) - Detailed feature breakdown
- [Tech Stack](./tech-stack.md) - Technology details

## Code Samples

Sanitized code examples available in:
- [code-samples/](./code-samples/) - Service implementations, database patterns

## Case Studies

See [case-studies/](./case-studies/) for detailed deep-dives on:
- Two-stage correction workflow
- Whisper integration
- Cloud deployment architecture

## My Role & Contributions

As the developer of this project, I was responsible for:

- **Architecture Design**: Designed the two-stage correction workflow
- **AI Integration**: Integrated OpenAI Whisper and WhisperX
- **Database Design**: PostgreSQL schema with manager pattern
- **Web Development**: Flask application with responsive UI
- **Cloud Deployment**: Google Cloud Run and Cloud SQL setup
- **Workflow Orchestration**: Complex multi-stage processing pipeline

## Technical Challenges Solved

1. **Sanskrit Correction**: Built specialized correction system for Sanskrit terms
2. **Cost Optimization**: Two-stage workflow reduces OpenAI API costs
3. **Memory Management**: Efficient Whisper model loading and cleanup
4. **Async Processing**: Background processing for large files
5. **Database Design**: Manager pattern for clean database operations

## Results

- ✅ Accurate transcription of spiritual content
- ✅ Efficient Sanskrit term correction
- ✅ Cost-optimized processing workflow
- ✅ Scalable cloud deployment
- ✅ User-friendly web interface

---

**Note:** This is a showcase of my work. The actual production codebase remains private. All code samples have been sanitized to remove sensitive information.
