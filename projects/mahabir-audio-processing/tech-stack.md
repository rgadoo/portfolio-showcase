# Tech Stack

Complete technology stack used in Mahabir Audio Processing.

## Core Language

- **Python 3.11+** - Primary programming language

## Web Framework

- **Flask 3.0.0** - Web application framework
- **Jinja2** - Template engine (included with Flask)
- **Werkzeug** - WSGI utilities (included with Flask)

## Database

- **PostgreSQL 15+** - Relational database
- **psycopg[binary,pool] 3.2.9** - PostgreSQL adapter with connection pooling

## AI & Machine Learning

### Speech-to-Text
- **openai-whisper 20250625** - OpenAI Whisper for transcription
- **whisperx** - Enhanced Whisper with speaker diarization
- **faster-whisper** - Optimized Whisper implementation
- **pyannote.audio** - Speaker diarization
- **torch 2.0.0+** - PyTorch for ML models
- **torchaudio 0.13.0+** - Audio processing

### Text Processing
- **transformers 4.21.0+** - Hugging Face transformers
- **tiktoken** - Token counting (if needed)

## Cloud Services

- **google-cloud-storage 2.10.0** - Google Cloud Storage client
- **Google Cloud Run** - Container hosting
- **Cloud SQL** - Managed PostgreSQL

## Utilities

- **python-dotenv 1.0.1** - Environment variable management
- **watchdog 3.0.0** - File system monitoring
- **requests 2.31.0** - HTTP library
- **numpy** - Numerical computing

## Development Tools

### Code Quality
- Python type hints
- Modular service architecture
- Comprehensive error handling
- Structured logging

### Project Structure

```
mahabir-audio-processing/
├── web/                    # Flask web application
│   ├── app.py             # Main Flask app
│   ├── transcription_routes.py
│   ├── entry_routes.py
│   └── templates/        # Jinja2 templates
├── services/              # Business logic
│   ├── transcription_service.py
│   ├── correction_service.py
│   ├── local_processor.py
│   ├── openai_client.py
│   └── sanskrit/         # Sanskrit correction
├── database/             # Database layer
│   ├── models.py         # Data models
│   ├── db_operations.py  # Database manager
│   └── managers/        # Specialized managers
├── scripts/              # Utility scripts
└── config.py            # Configuration
```

## External Services

### AI Services
- **OpenAI Whisper** - Local transcription (on server)
- **OpenAI GPT** - Text correction (API, optional)
- **WhisperX** - Enhanced transcription features

### Infrastructure
- **Google Cloud Run** - Application hosting
- **Cloud SQL** - Database hosting
- **Cloud Storage** - Media file storage (optional)

## Configuration

### Environment Variables
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DATABASE_URL` - Full database URL (Cloud Run)
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `OUTPUT_FOLDER` - Output directory
- `MEDIA_FOLDER` - Media file directory

### Configuration Files
- `.env` - Environment variables
- `config.py` - Application configuration

## Deployment

### Local Development
- Python virtual environment
- Local PostgreSQL or Cloud SQL Proxy
- Flask development server

### Production Deployment
- Docker containerization
- Google Cloud Run
- Cloud SQL database
- Environment-based configuration

## Performance

### Optimization
- Connection pooling for database
- Thread-safe model loading
- Batch processing for API calls
- Efficient memory management
- Model cleanup after use

### Scalability
- Cloud Run auto-scaling
- Connection pooling
- Async processing capabilities
- Resource-efficient design

## Security

### Best Practices
- Environment variables for secrets
- Parameterized SQL queries
- Input validation
- Secure file operations
- Error message sanitization

---

**Last Updated:** December 2024
