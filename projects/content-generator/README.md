# Content Generator

An AI-powered content generation pipeline that transforms YouTube transcripts into production-ready articles, courses, quizzes, and audio/video content using multi-step LLM orchestration.

**🔗 Quick Links:** [Architecture](./architecture.md) | [Features](./features.md) | [Tech Stack](./tech-stack.md) | [Code Samples](./code-samples/) | [Case Studies](./case-studies/)

## Overview

Content Generator is a comprehensive AI content pipeline that orchestrates multiple services end-to-end: YouTube synchronization, transcript processing, AI analysis with structured outputs, multi-layer validation, and publishing to Firestore/GCS. Built with production-grade patterns including retry logic, cost tracking, and operational metrics.

## Production Status

**Status:** Production-ready  
**Integration:** Powers content generation for [Nandi Platform](../nandi-platform/)  
**Workflow:** YouTube Sync → AI Analysis → Review → Publish

## Project Statistics

| Metric | Value |
|--------|-------|
| **Total Commits** | 150+ |
| **Python Files** | 198+ |
| **Lines of Code** | ~15,000+ (Python) |
| **Development Period** | Nov 2025 - Feb 2026 |
| **Services** | 25+ core services |
| **Content Types** | 5 (Article, Course, Quiz, Audio, Video) |
| **Validation Layers** | 5-layer validation chain |

## Key Achievements

- ✅ **Multi-Step LLM Pipeline**: End-to-end orchestration from YouTube to Firestore
- ✅ **Structured Outputs**: OpenAI JSON schema enforcement for consistent outputs
- ✅ **5-Layer Validation Chain**: Pre-API, schema, content, Pydantic, publish-time validation
- ✅ **Retry with Exponential Backoff**: Rate limit handling, jitter, queue-based retries
- ✅ **Cost Tracking & Metrics**: Token usage, success rates, health monitoring
- ✅ **Production Integration**: Publishes directly to Nandi Platform's Firestore/GCS

## Technologies Used

### AI & LLM
- **OpenAI GPT-4o/GPT-4o-mini** - Content generation with structured outputs
- **OpenAI DALL·E** - Hero image generation
- **OpenAI TTS / ElevenLabs** - Voice synthesis
- **Prompt Templates** - Layered prompt engineering system

### Backend & Services
- **Python 3.11+** - Core language
- **FastAPI** - API framework
- **PostgreSQL** - Staging database for drafts
- **Pydantic** - Data validation and schemas

### Integration & Publishing
- **Firebase Admin SDK** - Firestore writes
- **Google Cloud Storage** - Media file uploads
- **YouTube Data API v3** - Video sync and transcript fetching

### Patterns & Architecture
- **Multi-layer Validation** - 5-stage validation pipeline
- **Exponential Backoff** - Retry logic with jitter
- **Queue-based Processing** - Transcript queue with retry scheduling
- **Operation Tracking** - Audit trail with status workflow

## Architecture Highlights

### Multi-Step Pipeline

```
YouTube API → fetch_and_store_videos() → PostgreSQL
    ↓
Transcript Queue → import_transcript_for_video() → transcript_text
    ↓
AnalysisPromptBuilder.build_analysis_prompt() → OpenAI API
    ↓
ContentValidatorService.validate_*() → Post-processing
    ↓
BaseDraftService.create() → PostgreSQL drafts
    ↓
stage_to_content() → StagedContent (status: 'draft')
    ↓
approve_content() → (status: 'approved')
    ↓
Publisher.publish_content() → Firestore + GCS
```

### 5-Layer Validation Chain

| Layer | When | Purpose |
|-------|------|---------|
| **1. Taxonomy Validation** | Before API call | Fail-fast to save API costs |
| **2. OpenAI Schema** | During generation | JSON structure enforcement |
| **3. Content Validation** | Post-generation | Placeholder detection, length checks |
| **4. Pydantic Validation** | Pre-save | Type safety, required fields |
| **5. Publisher Validation** | Pre-publish | Firestore-ready verification |

### Prompt Engineering

- **Template-based System**: Markdown templates with variable interpolation
- **Layered Prompts**: System prompts, user prompts, context injection
- **Content-Type Specific**: Article, course, quiz, audio, video templates
- **Educational Language Enforcement**: Rejects narrative style outputs

## Features

### Fully Implemented ✅
- YouTube channel/playlist synchronization
- Transcript queue with retry scheduling
- AI analysis with structured outputs
- Article, course, quiz generation
- Audio/video content generation
- Multi-layer validation chain
- PostgreSQL staging workflow
- Firestore/GCS publishing
- Operation tracking and audit trail
- Health monitoring (24h, 7d, 30d metrics)
- Cost tracking and estimation

### Content Types Supported
- **Articles** - Long-form content with sections
- **Courses** - Modules, lessons, learning objectives
- **Quizzes** - Multiple choice questions with explanations
- **Audio** - Voice-generated content with scripts
- **Video** - Video content with subtitles

## Cost Efficiency

**Model Configuration:**
| Model | Cost (per 1M tokens) | Use Case |
|-------|---------------------|----------|
| `gpt-4o-mini` | ~$0.375 | Default, cost-effective |
| `gpt-4o` | ~$10 | Higher quality |
| `gpt-4-turbo` | ~$15 | Maximum capability |

**Cost Optimization Strategies:**
- Fail-fast validation before API calls
- Token limits per content type
- Default to cost-effective model (gpt-4o-mini)
- Structured outputs reduce retries

## Documentation

- [Architecture](./architecture.md) - System design and pipeline flow
- [Features](./features.md) - Detailed feature breakdown
- [Tech Stack](./tech-stack.md) - Technology choices and rationale

## Case Studies

See [case-studies/](./case-studies/) for detailed deep-dives on:
- Multi-layer validation implementation
- Retry logic with exponential backoff
- Prompt engineering patterns
- Cost optimization strategies

## Code Samples

Sanitized code examples available in:
- [code-samples/](./code-samples/) - Service implementations, validators, prompts

## My Role & Contributions

As the developer of this project, I was responsible for:

- **Pipeline Architecture**: Designed end-to-end content generation pipeline
- **AI Integration**: Implemented OpenAI structured outputs with schema enforcement
- **Validation System**: Built 5-layer validation chain with fail-fast patterns
- **Retry Logic**: Implemented exponential backoff with jitter and queue-based retries
- **Operational Metrics**: Built token tracking, cost estimation, health monitoring
- **Integration**: Connected pipeline to Nandi Platform's Firestore/GCS

## Technical Challenges Solved

1. **Structured Output Reliability**: OpenAI JSON schema enforcement for consistent outputs
2. **Rate Limit Handling**: Exponential backoff with jitter and Retry-After header support
3. **Cost Optimization**: Fail-fast validation saves 30%+ on unnecessary API calls
4. **Content Quality**: Multi-layer validation catches placeholders, enforces minimums
5. **Transcript Processing**: Queue-based system handles YouTube API rate limits
6. **Operational Visibility**: Health monitoring with 24h/7d/30d success rate tracking

## Results

- ✅ Generates production-ready content in minutes (vs hours manually)
- ✅ 5-layer validation ensures consistent quality
- ✅ Cost-effective at ~$0.002 per article with gpt-4o-mini
- ✅ Fail-fast patterns save ~30% on API costs
- ✅ Health monitoring enables proactive issue detection

---

**Note:** This is a showcase of my work. The actual production codebase remains private. All code samples have been sanitized to remove sensitive information.
