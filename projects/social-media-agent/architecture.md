# Architecture

This document describes the architecture of the Social Media Agent - an AI-powered automation tool for creating social media videos from book content.

## System Overview

The Social Media Agent uses a service-oriented architecture with RAG (Retrieval Augmented Generation) to transform book content into platform-ready social media videos.

## Architecture Principles

1. **Service-Oriented Design**: Modular services for each workflow step
2. **RAG-Based Content Discovery**: Vector search for relevant book passages
3. **AI Integration**: Multiple AI services for script and voice generation
4. **Pipeline Architecture**: Sequential processing through workflow stages
5. **Error Handling**: Robust error handling for external API calls

## System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Gradio Web UI                        │
│              (User Interface Layer)                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Script     │  │    Voice     │  │    Video     │ │
│  │  Generator   │  │  Generator   │  │   Creator    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │  Platform    │  │    Quote    │                    │
│  │  Formatter   │  │   Manager   │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  ChromaDB    │  │   Book       │  │   Output    │ │
│  │  (Vector DB) │  │   Files      │  │   Videos    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 External Services                        │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │   Claude/    │  │  ElevenLabs  │                    │
│  │   GPT-4      │  │   (Voice)    │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

## Core Services

### 1. Ingestion Service

**Purpose**: Load book chapters into ChromaDB vector database

**Process**:
1. Read book chapter files (.txt or .md)
2. Split into chunks
3. Generate embeddings
4. Store in ChromaDB collection

**Key Features**:
- Text chunking for optimal retrieval
- Embedding generation
- Persistent vector storage

### 2. Script Generator

**Purpose**: Generate 40-second video scripts from book content

**Process**:
1. User enters topic/trend
2. RAG search finds relevant book passages
3. LLM generates script from passages
4. Returns formatted script

**Key Features**:
- Vector similarity search
- Context-aware script generation
- Support for Claude and GPT-4

### 3. Voice Generator

**Purpose**: Generate voice-over audio from script

**Process**:
1. Take generated script
2. Call ElevenLabs API
3. Generate voice-over audio
4. Save audio file

**Key Features**:
- Natural voice synthesis
- Configurable voice settings
- Audio file management

### 4. Video Creator

**Purpose**: Assemble video with captions

**Process**:
1. Load background image/video
2. Add voice-over audio
3. Generate and overlay captions
4. Apply styling and effects
5. Export video file

**Key Features**:
- Automated caption generation
- Text overlay and styling
- Background integration
- Video composition

### 5. Platform Formatter

**Purpose**: Create platform-specific video variants

**Process**:
1. Take base video
2. Adjust aspect ratio per platform
3. Optimize for platform requirements
4. Generate platform-specific files

**Key Features**:
- TikTok format (9:16)
- Instagram Reels format (9:16)
- YouTube Shorts format (9:16)
- X/Twitter format (16:9)

### 6. Quote Manager

**Purpose**: Manage and track book quotes

**Features**:
- Browse quotes by chapter and theme
- View quote variations
- Mark themes as posted
- Track posting progress

## Data Flow

### Video Generation Workflow

```
1. User Input (Topic/Trend)
   ↓
2. RAG Search (ChromaDB)
   ↓
3. Script Generation (Claude/GPT-4)
   ↓
4. Voice Generation (ElevenLabs)
   ↓
5. Video Assembly (MoviePy)
   ↓
6. Platform Formatting
   ↓
7. Output ZIP Package
```

### RAG Process

```
Book Content → Chunking → Embeddings → ChromaDB
                                      ↓
User Query → Embedding → Similarity Search → Relevant Passages
                                      ↓
                              Context + Query → LLM → Script
```

## Technology Stack

### Core Framework
- **Python 3.9+** - Programming language
- **Gradio** - Web UI framework

### AI & ML
- **LangChain** - RAG framework
- **ChromaDB** - Vector database
- **Anthropic Claude** - Script generation
- **OpenAI GPT-4** - Alternative script generation
- **ElevenLabs** - Voice synthesis

### Video Processing
- **MoviePy** - Video editing and assembly
- **Pillow** - Image processing

### Utilities
- **python-dotenv** - Environment variable management
- **tiktoken** - Token counting

## Configuration Management

### Centralized Configuration

All configuration is managed through `src/core/config.py`:

- **APIConfig** - API keys and credentials
- **PathConfig** - File and directory paths
- **IngestionConfig** - Book ingestion settings
- **ScriptConfig** - Script generation settings
- **VoiceConfig** - Voice generation settings
- **VideoConfig** - Video creation settings
- **PlatformConfig** - Platform specifications

### Environment Variables

- `ANTHROPIC_API_KEY` - Claude API key
- `OPENAI_API_KEY` - OpenAI API key (alternative)
- `ELEVENLABS_API_KEY` - ElevenLabs API key

## Error Handling

### Custom Exceptions

- `SocialMediaAgentError` - Base exception
- `ConfigurationError` - Configuration issues
- `APIError` - External API failures
- `IngestionError` - Data ingestion errors
- `GenerationError` - Content generation errors

### Error Recovery

- Graceful degradation
- User-friendly error messages
- Logging for debugging

## Logging

### Structured Logging

- Centralized logging configuration
- Log levels (DEBUG, INFO, WARNING, ERROR)
- File and console output
- Timestamp and context information

## Performance Considerations

### Optimization Strategies

1. **Vector Search**: Efficient similarity search in ChromaDB
2. **Caching**: Cache embeddings and generated content
3. **Async Operations**: Parallel processing where possible
4. **Resource Management**: Efficient memory usage

### Cost Optimization

- Efficient API usage
- Token optimization
- Batch processing where applicable

## Security

### API Key Management

- Environment variables for secrets
- No hardcoded credentials
- Secure key storage

### Input Validation

- Validate user inputs
- Sanitize file paths
- Check API responses

## Future Enhancements

- Multi-language support
- Custom voice cloning
- Advanced video effects
- Batch processing
- Cloud deployment
- API for programmatic access

---

**Last Updated:** December 2024
