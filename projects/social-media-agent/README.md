# Social Media Agent

An AI-powered automation tool that converts book content into platform-ready social media videos for TikTok, Instagram Reels, YouTube Shorts, and X (Twitter).

**🔗 Quick Links:** [Architecture](./architecture.md) | [Features](./features.md) | [Code Samples](./code-samples/) | [Case Studies](./case-studies/)

## Overview

Social Media Agent automates the entire workflow of creating short-form video content from book chapters. Using RAG (Retrieval Augmented Generation), AI script generation, voice synthesis, and video assembly, it transforms hours of manual work into a 3-minute automated process.

## Project Statistics

| Metric | Value |
|--------|-------|
| **Total Commits** | 5+ |
| **Python Files** | 23+ |
| **Lines of Code** | ~1,000+ (Python) |
| **Services** | 6+ core services |
| **Dependencies** | 15+ Python packages |

## Key Features

- **RAG-Powered Content Discovery**: Finds relevant book passages using vector search
- **AI Script Generation**: Creates 40-second scripts with Claude/GPT-4
- **Voice Synthesis**: Generates natural voice-overs with ElevenLabs
- **Video Assembly**: Automatically creates videos with captions using MoviePy
- **Multi-Platform Formatting**: Generates platform-specific variants
- **Quote Management**: Track and manage book quotes for social media
- **Gradio Web UI**: User-friendly interface for the complete workflow

## Technologies Used

### AI & LLM
- **LangChain** - RAG framework
- **Anthropic Claude** / **OpenAI GPT-4** - Script generation
- **ChromaDB** - Vector database for book content
- **ElevenLabs** - Voice synthesis

### Video & Media
- **MoviePy** - Video assembly and editing
- **Pillow** - Image processing

### UI & Framework
- **Gradio** - Web interface
- **Python 3.9+** - Core language

## Architecture

### Core Components

1. **Ingestion Service** - Loads book chapters into ChromaDB vector database
2. **Script Generator** - RAG system to find relevant passages and generate scripts
3. **Voice Generator** - ElevenLabs/OpenAI TTS integration
4. **Video Creator** - MoviePy-based video assembly with captions
5. **Platform Formatter** - Creates platform-specific video variants
6. **Quote Manager** - Manages and tracks book quotes

### Workflow

```
Book Chapters → ChromaDB (Vector DB) → RAG Search → AI Script Generation 
→ Voice Synthesis → Video Assembly → Platform Formatting → Download ZIP
```

## Use Cases

- ✅ Respond to trending topics in your niche
- ✅ Create content series from book chapters
- ✅ Repurpose book wisdom for social media
- ✅ Build thought leadership on multiple platforms
- ✅ Generate daily content in minutes, not hours

## Cost Efficiency

**Per Video:**
- Claude API: ~$0.01-0.02
- ElevenLabs: ~$0.05-0.10
- Total: ~$0.06-0.12 per video

**Monthly** (5 videos/day):
- ~150 videos/month
- Total: ~$9-18/month

## Technical Highlights

### RAG Implementation
- Vector embeddings of book content
- Semantic search for relevant passages
- Context-aware script generation

### Video Processing
- Automated caption generation
- Platform-specific aspect ratios
- Background music integration
- Text overlay and styling

### Architecture Patterns
- Service-oriented design
- Centralized configuration
- Custom exception handling
- Structured logging
- Input validation

## Documentation

- [Architecture](./architecture.md) - System design and architecture
- [Features](./features.md) - Detailed feature breakdown
- [Tech Stack](./tech-stack.md) - Technology details

## Code Samples

Sanitized code examples available in:
- [code-samples/](./code-samples/) - Service implementations, utilities

## My Role & Contributions

As the developer of this project, I was responsible for:

- **Architecture Design**: Designed the RAG-based content discovery system
- **AI Integration**: Integrated multiple AI services (Claude, ElevenLabs)
- **Video Processing**: Implemented automated video assembly pipeline
- **UI Development**: Built Gradio-based web interface
- **Code Refactoring**: Improved architecture with centralized config and error handling

## Technical Challenges Solved

1. **RAG Implementation**: Built efficient vector search for book content
2. **Multi-Platform Formatting**: Automated aspect ratio and format conversion
3. **Video Assembly**: Automated caption generation and video composition
4. **Cost Optimization**: Efficient API usage to minimize costs
5. **Error Handling**: Robust error handling for external API calls

## Results

- ✅ 3-minute video generation (vs 15-20 minutes manually)
- ✅ Multi-platform output in single workflow
- ✅ Cost-effective at ~$0.10 per video
- ✅ Scalable architecture for content creators

---

**Note:** This is a showcase of my work. The actual production codebase remains private. All code samples have been sanitized to remove sensitive information.
