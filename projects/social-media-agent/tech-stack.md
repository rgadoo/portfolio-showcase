# Tech Stack

Complete technology stack used in the Social Media Agent.

## Core Language

- **Python 3.9+** - Primary programming language

## AI & Machine Learning

### LLM & RAG
- **LangChain 0.1.0** - RAG framework and orchestration
- **LangChain Community 0.0.13** - Community integrations
- **LangChain Anthropic 0.1.1** - Anthropic Claude integration
- **Anthropic 0.18.1** - Claude API client
- **OpenAI 1.12.0** - GPT-4 API client (alternative)

### Vector Database
- **ChromaDB 0.4.22** - Vector database for embeddings

### Voice Synthesis
- **ElevenLabs 0.2.27** - Voice generation API

## Video & Media Processing

- **MoviePy 1.0.3** - Video editing and assembly
- **Pillow 10.2.0** - Image processing

## User Interface

- **Gradio 4.19.2** - Web UI framework

## Utilities

- **python-dotenv 1.0.1** - Environment variable management
- **tiktoken 0.6.0** - Token counting for LLMs

## Architecture Patterns

### Service-Oriented Architecture

```
src/
├── core/           # Configuration, exceptions, logging
├── services/       # Business logic services
├── models/         # Data models
├── ui/            # User interface
└── utils/         # Utility functions
```

### Key Design Patterns

- **Service Layer**: Business logic separation
- **Configuration Management**: Centralized config
- **Error Handling**: Custom exceptions
- **Logging**: Structured logging
- **Validation**: Input validation

## Development Tools

### Code Quality
- Python type hints
- Modular structure
- Error handling
- Logging framework

### Project Structure

```
social-media-agent/
├── src/
│   ├── core/          # Core configuration and utilities
│   ├── services/      # Service implementations
│   ├── models/        # Data models
│   ├── ui/           # Gradio interface
│   └── utils/        # Helper functions
├── data/
│   ├── books/        # Source book content
│   ├── chroma_db/    # Vector database
│   └── output/       # Generated videos
├── assets/           # Video backgrounds, fonts
└── tests/           # Test files
```

## External Services

### AI Services
- **Anthropic Claude** - Script generation
- **OpenAI GPT-4** - Alternative script generation
- **ElevenLabs** - Voice synthesis

### Storage
- **Local File System** - Book files, videos, database
- **ChromaDB** - Vector database storage

## Configuration

### Environment Variables
- `ANTHROPIC_API_KEY` - Claude API key
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `ELEVENLABS_API_KEY` - ElevenLabs API key

### Configuration Files
- `.env` - Environment variables
- `src/core/config.py` - Centralized configuration

## Deployment

### Local Development
- Python virtual environment
- Local file storage
- Gradio web server

### Future Deployment Options
- Cloud deployment (AWS, GCP, Azure)
- Docker containerization
- API service
- Serverless functions

## Performance

### Optimization
- Efficient vector search
- Caching strategies
- Resource management
- API call optimization

### Scalability
- Modular architecture
- Service separation
- Configurable processing

## Security

### Best Practices
- Environment variables for secrets
- Input validation
- Error handling
- Secure file operations

---

**Last Updated:** December 2024
