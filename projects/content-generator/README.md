# Content Generator

An AI-powered content creation platform that generates articles, courses, quizzes, audio, and video content from prompts, with a complete text-to-audio-to-video pipeline and publishing to Firebase/GCS.

**🔗 Quick Links:** [Architecture](./architecture.md) | [Features](./features.md) | [Tech Stack](./tech-stack.md) | [Code Samples](./code-samples/) | [Case Studies](./case-studies/)

## Overview

Content Generator is a comprehensive AI content platform with multiple generation pathways:

1. **Prompt-Based Generation**: Create articles, courses, quizzes, and audio scripts directly from text prompts
2. **YouTube Integration**: Sync channels, import transcripts, analyze content
3. **Audio Pipeline**: Convert text to speech using OpenAI TTS or ElevenLabs
4. **Video Pipeline**: Convert audio to video with waveform visualization and burned-in subtitles
5. **Publishing**: Upload to GCS and publish to Firestore with multi-tenant support

## Production Status

**Status:** Production-ready  
**Integration:** Powers content generation for [Nandi Platform](../nandi-platform/)  
**Workflow:** Prompt/YouTube → AI Generation → Audio → Video → Review → Publish

## Project Statistics

| Metric | Value |
|--------|-------|
| **Total Commits** | 150+ |
| **Python Files** | 198+ |
| **Lines of Code** | ~15,000+ (Python) |
| **Development Period** | Nov 2025 - Feb 2026 |
| **Services** | 25+ core services |
| **Content Types** | 5 (Article, Course, Quiz, Audio, Video) |
| **TTS Providers** | 2 (OpenAI TTS, ElevenLabs) |
| **Validation Layers** | 5-layer validation chain |

## Key Achievements

- ✅ **Multi-Pathway Content Generation**: Create content from prompts or YouTube transcripts
- ✅ **Text-to-Audio Pipeline**: OpenAI TTS and ElevenLabs voice synthesis
- ✅ **Audio-to-Video Pipeline**: Waveform visualization with burned-in subtitles
- ✅ **Structured AI Outputs**: OpenAI JSON schema enforcement for consistent content
- ✅ **5-Layer Validation Chain**: Pre-API, schema, content, Pydantic, publish-time validation
- ✅ **Multi-Tenant Publishing**: Instance-specific paths in GCS and Firestore
- ✅ **Cost Tracking & Metrics**: Token usage, success rates, health monitoring

## Technologies Used

### AI & Content Generation
- **OpenAI GPT-4o/GPT-4o-mini** - Content generation with structured outputs
- **OpenAI DALL·E** - Hero image generation
- **Prompt Templates** - Layered prompt engineering system

### Audio Pipeline
- **OpenAI TTS** - Text-to-speech (alloy, echo, fable, onyx, nova, shimmer voices)
- **ElevenLabs** - Premium voice synthesis with custom voices
- **Audio Processing** - Duration calculation, format validation, segment combination

### Video Pipeline
- **MoviePy** - Video composition and editing
- **librosa** - Audio analysis for waveform visualization
- **matplotlib** - Waveform rendering
- **FFmpeg** - Video encoding with optimized settings
- **Subtitle Service** - SRT generation, burned-in subtitles

### Backend & Data
- **Python 3.11+** - Core language
- **FastAPI** - API framework
- **PostgreSQL** - Staging database for drafts
- **Pydantic** - Data validation and schemas

### Cloud & Publishing
- **Firebase Admin SDK** - Firestore document publishing
- **Google Cloud Storage** - Media file storage (audio, video, images, transcripts)
- **YouTube Data API v3** - Channel sync and transcript import

## Architecture Highlights

### Complete Content Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTENT GENERATION PATHWAYS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PATHWAY 1: From Prompt                                         │
│  ─────────────────────                                          │
│  User Prompt → OpenAI → Structured Content → Draft              │
│                                                                 │
│  PATHWAY 2: From YouTube                                        │
│  ────────────────────────                                       │
│  YouTube Sync → Transcript → AI Analysis → Content → Draft      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       AUDIO PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Text/Script → Voice Service → Audio File (.mp3)                │
│                    │                                            │
│                    ├── OpenAI TTS (alloy, echo, fable, etc.)   │
│                    └── ElevenLabs (custom voices)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       VIDEO PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Audio → Video Generator → Subtitles → Video File (.mp4)        │
│              │                │                                 │
│              │                └── YouTube-style burned-in       │
│              │                                                  │
│              └── Waveform visualization (animated)              │
│                  Real-time sync with audio                      │
│                  Customizable colors/styling                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STAGING & PUBLISHING                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Draft → Stage → Review → Approve → Publish                     │
│                              │                                  │
│                              ├── GCS: Audio, Video, Images      │
│                              │       Instance-specific paths    │
│                              │                                  │
│                              └── Firestore: Content documents   │
│                                  Multi-tenant isolation         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Content Types Supported

| Type | Generation | Audio | Video | Output |
|------|------------|-------|-------|--------|
| **Article** | ✅ From prompt/transcript | — | — | Firestore page |
| **Course** | ✅ Modules, lessons, objectives | — | — | Firestore course |
| **Quiz** | ✅ Multiple choice, T/F, short answer | — | — | Firestore quiz |
| **Audio** | ✅ Script with segments | ✅ TTS | — | GCS audio + Firestore |
| **Video** | ✅ From audio | ✅ Required | ✅ Waveform + subtitles | GCS video + Firestore |

### Audio Formats & Voices

**OpenAI TTS:**
- Voices: alloy, echo, fable, onyx, nova, shimmer
- Speed control: 0.25x - 4.0x
- Models: tts-1, tts-1-hd

**ElevenLabs:**
- Custom voice library
- Stability and similarity boost controls
- Speed control: 0.5x - 2.0x

### Video Generation

- **Waveform Style**: Animated audio visualization synced to playback
- **Subtitles**: YouTube-style with background boxes
- **Resolutions**: 1080p, 720p, 480p
- **Encoding**: FFmpeg with optimized settings

## Features

### Fully Implemented ✅
- Article generation from prompts
- Course structure generation (modules, lessons)
- Quiz generation (multiple types, difficulties)
- Audio script generation (podcast, narration, meditation, etc.)
- OpenAI TTS voice synthesis
- ElevenLabs voice synthesis
- Audio-to-video conversion
- Waveform visualization
- Burned-in subtitle generation
- YouTube channel/playlist sync
- Transcript import and analysis
- Hero image generation (DALL·E)
- Multi-layer validation chain
- GCS media upload (instance-specific paths)
- Firestore content publishing
- PostgreSQL staging workflow
- Cost tracking and metrics

## Cost Efficiency

**AI Generation:**
| Model | Cost (per 1M tokens) | Use Case |
|-------|---------------------|----------|
| `gpt-4o-mini` | ~$0.375 | Default, cost-effective |
| `gpt-4o` | ~$10 | Higher quality |

**Voice Synthesis:**
| Provider | Cost | Use Case |
|----------|------|----------|
| OpenAI TTS | ~$15/1M chars | Standard voices |
| ElevenLabs | ~$0.30/1K chars | Premium/custom voices |

## Documentation

- [Architecture](./architecture.md) - Full pipeline flow and component details
- [Features](./features.md) - Detailed feature breakdown
- [Tech Stack](./tech-stack.md) - Technology choices and rationale

## Case Studies

See [case-studies/](./case-studies/) for detailed deep-dives on:
- Multi-layer validation implementation
- Retry logic with exponential backoff
- Audio/video pipeline architecture

## Code Samples

Sanitized code examples available in:
- [code-samples/](./code-samples/) - Service implementations, validators, prompts

## My Role & Contributions

As the developer of this project, I was responsible for:

- **Pipeline Architecture**: Designed end-to-end content generation with multiple pathways
- **AI Integration**: Implemented OpenAI structured outputs and DALL·E image generation
- **Audio Pipeline**: Built TTS integration with OpenAI and ElevenLabs
- **Video Pipeline**: Implemented waveform visualization and subtitle burning
- **Validation System**: Built 5-layer validation chain with fail-fast patterns
- **Publishing**: Integrated GCS storage and Firestore publishing
- **Multi-Tenant**: Designed instance-specific paths and isolation

## Technical Challenges Solved

1. **Multi-Pathway Generation**: Unified architecture for prompt-based and YouTube-based content
2. **TTS Provider Abstraction**: Single interface for OpenAI TTS and ElevenLabs
3. **Real-Time Waveform Sync**: librosa analysis synced with MoviePy composition
4. **Subtitle Timing**: Industry-standard timing (2.5 words/sec) with word wrapping
5. **Multi-Tenant Storage**: Instance-specific GCS paths for complete isolation
6. **Content Quality**: 5-layer validation ensures consistent, high-quality output

## Results

- ✅ Generates production-ready content in minutes (vs hours manually)
- ✅ Supports 5 content types with full lifecycle management
- ✅ Audio generation with 2 TTS providers and multiple voices
- ✅ Video generation with animated waveform and subtitles
- ✅ Multi-tenant publishing to GCS and Firestore
- ✅ 5-layer validation ensures consistent quality

---

**Note:** This is a showcase of my work. The actual production codebase remains private. All code samples have been sanitized to remove sensitive information.
