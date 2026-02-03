# Technical Expertise: Skills Mapped to Implementations

This document maps professional skills and claims to concrete implementations across production systems in this portfolio.

**Production Systems Referenced:**
- **[Nandi Platform](./projects/nandi-platform/)** — Multi-tenant SaaS content platform (Next.js, Firebase, GCP)
- **[Content Generator](./projects/content-generator/)** — AI-powered content generation pipeline (Python, FastAPI, PostgreSQL, OpenAI)

---

## AI Engineering & LLM Workflows

### Multi-Step Pipelines Orchestrating LLMs with External Services

**Skill:** Building end-to-end AI pipelines that orchestrate LLMs with external services

**Evidence (Content Generator):**

| Pipeline Stage | Implementation | Location |
|----------------|----------------|----------|
| YouTube Sync | Fetches videos, metadata, transcripts from YouTube Data API v3 | `services/youtube_sync_service.py` |
| PostgreSQL Staging | Stores drafts, staged content with status tracking | `services/draft_services/` |
| AI Analysis | Builds prompts, calls OpenAI, validates outputs | `services/openai_service.py` |
| Review Workflow | Draft → Staged → Approved status transitions | `services/staged_content_service.py` |
| Publishing | Validates, uploads to GCS, writes to Firestore | `services/publisher/` |

**Pipeline Flow:**
```
YouTube API → fetch_and_store_videos() → PostgreSQL
    ↓
Transcript Queue → import_transcript_for_video() → transcript_text
    ↓
AnalysisPromptBuilder → OpenAI API → Structured Output
    ↓
ContentValidatorService → Post-processing → PostgreSQL drafts
    ↓
stage_to_content() → approve_content() → Publisher → Firestore + GCS
```

📖 [Full Architecture Documentation](./projects/content-generator/architecture.md)

---

### Prompt-Layered Generation

**Skill:** Designing layered prompt systems for consistent AI outputs

**Evidence (Content Generator):**

| Layer | Purpose | Implementation |
|-------|---------|----------------|
| System Prompts | Instructions from templates | `ARTICLE_GENERATION_PROMPT.md`, `COURSE_GENERATION_PROMPT.md` |
| User Prompts | Content requests with metadata | `services/prompt_builder_service.py` |
| Context Injection | Instance taxonomy, content type, difficulty | `PromptBuilderService.build_*_prompt()` |
| Variable Interpolation | `{{variable_name}}` replacement | Template system |

**Template Structure:**
- `ARTICLE_GENERATION_PROMPT.md` — Article-specific instructions
- `COURSE_GENERATION_PROMPT.md` — Course structure requirements
- `QUIZ_GENERATION_PROMPT.md` — Question format specs

---

### Structured Outputs

**Skill:** Implementing reliable structured outputs from LLMs

**Evidence (Content Generator):**

**OpenAI Structured Outputs Configuration:**
```python
response_format={
    "type": "json_schema",
    "json_schema": {
        "name": schema_name,
        "schema": schema,
        "strict": False  # Allows optional fields
    }
}
```

**Schema Definitions:**
- `ARTICLE_SCHEMA` — Title, sections, content blocks
- `COURSE_SCHEMA` — Modules, lessons, learning objectives
- `QUIZ_SCHEMA` — Questions, options, correct answers
- `AUDIO_SCHEMA` — Script, voice settings, duration

📖 [Code Samples](./projects/content-generator/code-samples/)

---

### Multi-Layer Validation Chains

**Skill:** Building validation systems that ensure AI output quality

**Evidence (Content Generator):**

| Validation Layer | Timing | Purpose | Implementation |
|------------------|--------|---------|----------------|
| **1. Taxonomy** | Pre-API | Fail-fast, save costs | `services/taxonomy_validator.py` |
| **2. OpenAI Schema** | During | JSON structure enforcement | `response_format` with `json_schema` |
| **3. Content Validation** | Post | Placeholder detection, length checks | `services/content_validator_service.py` |
| **4. Pydantic** | Pre-save | Type safety, required fields | Pydantic models |
| **5. Publisher** | Pre-publish | Firestore-ready verification | `services/publisher/content_validator.py` |

**Quality Checks:**
- Placeholder text detection (regex patterns)
- Minimum content length (1000+ chars for descriptions)
- Educational language enforcement (rejects narrative style)
- Structure validation (sections, modules, lessons)

📖 [Case Study: Multi-Layer Validation](./projects/content-generator/case-studies/multi-layer-validation.md)

---

### Retry Logic with Exponential Backoff

**Skill:** Implementing robust retry logic for external API calls

**Evidence (Content Generator):**

**OpenAI Service Retry:**
```python
retry_delay = base_delay * (2 ** attempt)  # Exponential backoff
# Handles: RateLimitError, APITimeoutError, JSON parsing errors
```

**Transcript Queue Retry:**
```python
delay = base_delay * (2 ** retry_count) * (1 ± 0.1)  # With jitter
# Respects YouTube API Retry-After header
# Max delay cap: 300 seconds
```

**Fallback Mechanisms:**
- Video transcript fallback if script unavailable
- Channel ID fallback via search API
- Playlist fallback via search API

📖 [Case Study: Retry with Exponential Backoff](./projects/content-generator/case-studies/retry-exponential-backoff.md)

---

### Configurable Model Selection with Cost Tracking

**Skill:** Managing AI model costs and selection

**Evidence (Content Generator):**

**Supported Models:**
| Model | Cost (per 1M tokens) | Use Case |
|-------|---------------------|----------|
| `gpt-4o-mini` | ~$0.375 | Default, cost-effective |
| `gpt-4o` | ~$10 | Higher quality |
| `gpt-4-turbo` | ~$15 | Maximum capability |

**Cost Tracking:**
```python
def get_usage_stats():
    return {
        "total_tokens_used": self.total_tokens_used,
        "total_requests": self.total_requests,
        "failed_requests": self.failed_requests,
        "success_rate": success_rate,
        "estimated_cost": cost_estimate
    }
```

---

### Operational Metrics

**Skill:** Building observability into AI systems

**Evidence (Content Generator):**

**Token Usage Tracking:**
- `total_tokens_used` — Cumulative token count
- `total_requests` — Request counter
- `failed_requests` — Failure counter
- Prompt vs completion tokens tracked separately

**Health Monitoring:**
- Success rates: 24h, 7d, 30d windows
- Error counts by type
- Health status: `healthy`, `degraded`, `unhealthy`

**Operation Tracking:**
- Operation types: `publish`, `delete`
- Status: `pending`, `in_progress`, `completed`, `failed`
- Timestamps: `started_at`, `completed_at`

---

## Platform Engineering

### Multi-Tenant SaaS Architecture

**Skill:** Designing and implementing multi-tenant systems with isolation

**Evidence (Nandi Platform):**

#### Middleware Layer Isolation

| Domain Type | Routing | Example |
|-------------|---------|---------|
| Platform domain | Platform mode | `satjana.com` → marketing/signup |
| Subdomain | Instance mode | `*.satjana.com` → extract instanceId |
| Custom domain | Instance mode | Lookup from Firestore |
| Localhost | Dev mode | Uses env var |

**Implementation:**
- Middleware sets `x-instance-id` header based on hostname
- `getTenantId()` reads header automatically
- Fail-fast in production (no default tenant fallback)

#### Database Layer Isolation

**Firestore Collections (all scoped by `instanceId`):**
| Collection | Tenant Scoping |
|------------|----------------|
| `content` | `instanceId` field on every document |
| `pillars` | `instances/{instanceId}/pillars/{pillarId}` |
| `categories` | `instances/{instanceId}/categories/{categoryId}` |
| `transcripts` | `instanceId` field |

#### Storage Layer Isolation

**GCS Path Structure:**
```
{instanceId}/content/{filename}
{instanceId}/transcripts/{filename}
{instanceId}/thumbnails/{filename}
```

📖 [Case Study: Multi-Tenant Architecture](./projects/nandi-platform/case-studies/multi-tenant-architecture.md)

---

### Authentication with RBAC and Granular Permissions

**Skill:** Implementing secure authentication with role-based access control

**Evidence (Nandi Platform):**

#### Authentication Methods (Firebase Auth)
- Email/Password — Standard signup/login
- Google OAuth — Social login
- Magic Links — Passwordless email authentication

#### Role Hierarchy

| Role | Capabilities |
|------|-------------|
| `user` | Browse content, save favorites |
| `creator` | Submit content for review |
| `admin` | Manage content, review submissions, manage taxonomy |
| `super_admin` | Full platform access, manage instances |

#### Granular Permissions
```typescript
'content:read' | 'content:write' | 'content:publish' |
'taxonomy:write' | 'users:write' | 'submissions:approve' | 'instance:write'
```

#### API Route Protection
```typescript
withAuth({ requiredRole: 'admin' })
withAuth({ requiredPermission: 'content:publish' })
withAdmin()  // Convenience wrapper
```

---

### Content Workflow Automation

**Skill:** Building automated content workflows with status tracking

**Evidence (Content Generator):**

#### Status Workflow
```
Draft (PostgreSQL)
    ↓ mark_ready_to_stage()
Staged Content (status: 'draft')
    ↓ User Review
Staged Content (status: 'approved')
    ↓ Publisher.publish_content()
Published (Firestore + GCS)
```

#### Operation Tracking
| Field | Purpose |
|-------|---------|
| `operation_type` | `publish`, `delete` |
| `status` | `pending`, `in_progress`, `completed`, `failed` |
| `started_at` | Operation start timestamp |
| `completed_at` | Operation end timestamp |

---

### Defense-in-Depth Security

**Skill:** Implementing multiple security layers

**Evidence (Nandi Platform):**

| Security Layer | Implementation |
|----------------|----------------|
| **Middleware** | Tenant routing, header injection |
| **Firestore Rules** | Tenant boundary enforcement |
| **API Validation** | `validateInstanceAccess()` |
| **Bootstrap Protection** | `BOOTSTRAP_SECRET_TOKEN` for super admin |
| **Security Headers** | CSP, HSTS, X-Frame-Options |
| **Rate Limiting** | On public endpoints |

**Fail-Fast Patterns:**
- No default tenant fallback in production
- Taxonomy validation before expensive API calls
- Early termination on invalid tenant context

---

### Cloud Deployments on GCP with CI/CD

**Skill:** Deploying containerized applications with automated pipelines

**Evidence (Nandi Platform):**

#### Infrastructure
| Component | Service |
|-----------|---------|
| Compute | Google Cloud Run |
| Database | Firestore |
| Storage | Google Cloud Storage |
| Auth | Firebase Authentication |
| CI/CD | Cloud Build |
| Secrets | Secret Manager |

#### Cloud Run Configuration
| Setting | Value |
|---------|-------|
| Memory | 1Gi |
| CPU | 2 |
| Timeout | 300s |
| Max instances | 10 (prod), 5 (dev) |

📖 [Infrastructure Documentation](./projects/nandi-platform/infrastructure.md)

---

### Data Modeling (Postgres and Document Stores)

**Skill:** Designing data models for both relational and document databases

**Evidence:**

#### Firestore (Document Store) — Nandi Platform

| Collection | Key Fields |
|------------|------------|
| `content` | `instanceId`, `contentType`, `title`, `description`, `pillar`, `category` |
| `instances` | `id`, `name`, `domain`, `branding`, `contentTypes`, `status` |
| `users/{userId}/memberships/{instanceId}` | `role`, `status`, `joinedAt` |
| `transcripts` | `instanceId`, `gcsPath`, `transcriptLength`, `language` |

#### PostgreSQL — Content Generator

| Table | Purpose |
|-------|---------|
| `video_metadata` | YouTube video sync data |
| `transcript_queue` | Transcript processing queue |
| `article_drafts` | Article content drafts |
| `staged_content` | Review-ready content |
| `content_operations` | Operation tracking |

---

### Audio Pipeline

**Skill:** Building text-to-speech pipelines with multiple providers

**Evidence (Content Generator):**

| Component | Implementation |
|-----------|----------------|
| Voice Service | Unified interface for TTS providers |
| OpenAI TTS | 6 voices (alloy, echo, fable, onyx, nova, shimmer), speed 0.25x-4.0x |
| ElevenLabs | Custom voices, stability/similarity controls, speed 0.5x-2.0x |
| Audio Processing | Duration calculation, format validation, segment combination |

**Workflow:**
```
Text/Script → Voice Service → TTS Provider → Audio File (.mp3)
                   │
                   ├── OpenAI TTS (tts-1, tts-1-hd models)
                   └── ElevenLabs (eleven_multilingual_v2)
```

---

### Video Pipeline

**Skill:** Building audio-to-video conversion with visualization

**Evidence (Content Generator):**

| Component | Implementation |
|-----------|----------------|
| Waveform Generator | librosa analysis + matplotlib rendering + MoviePy composition |
| Subtitle Service | YouTube-style burned-in captions, 2.5 words/sec timing |
| Video Encoding | FFmpeg with optimized settings, 1080p/720p/480p |
| Real-Time Sync | Waveform animation synced to audio playback |

**Workflow:**
```
Audio File → librosa Analysis → Waveform Frames → MoviePy Composition
                                      ↓
                              Subtitle Generation (from script)
                                      ↓
                              Burn-in Subtitles → FFmpeg Encode → Video (.mp4)
```

📖 [Architecture Documentation](./projects/content-generator/architecture.md)

---

## Summary Table

| Capability | Nandi Platform | Content Generator |
|------------|----------------|-------------------|
| Multi-step AI pipelines | — | ✅ |
| Prompt engineering | — | ✅ |
| Structured outputs | — | ✅ |
| Multi-layer validation | — | ✅ |
| Retry/backoff logic | — | ✅ |
| Model selection & cost tracking | — | ✅ |
| Operational metrics | — | ✅ |
| Text-to-Speech (OpenAI, ElevenLabs) | — | ✅ |
| Audio-to-Video conversion | — | ✅ |
| Waveform visualization | — | ✅ |
| Subtitle generation & burning | — | ✅ |
| Multi-tenant architecture | ✅ | — |
| Authentication & RBAC | ✅ | — |
| Admin tooling | ✅ | — |
| Cloud deployment (GCP) | ✅ | ✅ |
| Firestore (document store) | ✅ | ✅ |
| PostgreSQL | — | ✅ |
| GCS media storage | ✅ | ✅ |
| Defense-in-depth security | ✅ | — |
| Content workflow automation | ✅ | ✅ |

---

## Related Documentation

- [Nandi Platform Architecture](./projects/nandi-platform/architecture.md)
- [Content Generator Architecture](./projects/content-generator/architecture.md)
- [Multi-Layer Validation Case Study](./projects/content-generator/case-studies/multi-layer-validation.md)
- [Retry Logic Case Study](./projects/content-generator/case-studies/retry-exponential-backoff.md)
- [Multi-Tenant Architecture Case Study](./projects/nandi-platform/case-studies/multi-tenant-architecture.md)

---

*Last updated: February 2026*
