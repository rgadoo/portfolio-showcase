# Case Study: Google Cloud Run Deployment

## Challenge

Deploy a Flask application with audio processing capabilities (requiring significant memory and CPU) to a scalable cloud platform. The application needs to handle large audio files, maintain database connections, and scale based on demand.

## Solution

Deployed to Google Cloud Run with Cloud SQL for database, providing auto-scaling, managed infrastructure, and efficient resource allocation.

## Architecture

### Deployment Components

```
┌─────────────────────────────────────────┐
│         Google Cloud Run                 │
│  ┌───────────────────────────────────┐  │
│  │    Flask Application Container    │  │
│  │  - Python 3.11                    │  │
│  │  - Flask 3.0                       │  │
│  │  - Whisper Models                  │  │
│  │  - 4-8GB Memory                    │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Cloud SQL (PostgreSQL)          │
│  - PostgreSQL 15                        │
│  - db-f1-micro tier                     │
│  - Private IP connection                │
└─────────────────────────────────────────┘
```

### Cloud Run Configuration

**Container Specifications**:
- **Memory**: 4-8GB (for Whisper models)
- **CPU**: 2-4 vCPUs
- **Concurrency**: 1-10 requests per instance
- **Timeout**: 3600 seconds (for long transcriptions)
- **Min Instances**: 0 (scale to zero)
- **Max Instances**: 10 (auto-scale)

### Cloud SQL Configuration

**Database Instance**:
- **Version**: PostgreSQL 15
- **Tier**: db-f1-micro (development) / db-n1-standard (production)
- **Region**: us-central1
- **Connection**: Cloud SQL Proxy

## Implementation Details

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "main.py", "--port", "8080"]
```

### Cloud Run Deployment

```bash
gcloud run deploy mahabir-audio-processing \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 8Gi \
    --cpu 4 \
    --timeout 3600 \
    --add-cloudsql-instances PROJECT_ID:REGION:INSTANCE_NAME \
    --set-env-vars DATABASE_URL="postgresql://USER:PASSWORD@/DB_NAME?host=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME"
```

### Database Connection

**Cloud SQL Proxy Integration**:
- Automatic connection via Unix socket
- Secure private IP connection
- No public IP needed
- Connection pooling support

**Connection String**:
```
postgresql://user:password@/database?host=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME
```

### Environment Configuration

**Required Variables**:
- `DATABASE_URL`: Cloud SQL connection string
- `OPENAI_API_KEY`: OpenAI API key (optional)
- `OUTPUT_FOLDER`: Output directory path
- `MEDIA_FOLDER`: Media file directory

**Secrets Management**:
- Google Secret Manager (recommended)
- Environment variables (for non-sensitive config)
- Cloud SQL credentials (managed by GCP)

## Key Features

### Auto-Scaling

- **Scale to Zero**: No cost when idle
- **Automatic Scaling**: Based on request volume
- **Cold Start**: ~10-30 seconds for first request
- **Warm Instances**: Keep instances warm for faster response

### Resource Management

**Memory Allocation**:
- Base: 4GB (for base Whisper model)
- Recommended: 8GB (for large models)
- Configurable per deployment

**CPU Allocation**:
- Base: 2 vCPUs
- Recommended: 4 vCPUs (for faster processing)
- Burstable performance

### Database Connection

**Connection Pooling**:
- Reuse connections across requests
- Automatic reconnection on failure
- Connection limit management
- Transaction support

### File Storage

**Options**:
1. **Local Storage**: Temporary files in container (ephemeral)
2. **Cloud Storage**: Persistent file storage (recommended)
3. **Database**: Small files in database

**Recommendation**: Use Cloud Storage for media files, local storage for temporary processing files.

## Technical Challenges Solved

### Challenge 1: Memory Requirements

**Problem**: Whisper models require significant memory (1-2GB for large model)

**Solution**:
- Allocate sufficient memory (8GB)
- Model loading strategy (lazy loading)
- Memory cleanup after use
- Configurable model size

### Challenge 2: Long-Running Tasks

**Problem**: Transcription can take 10-60 minutes for long files

**Solution**:
- Increase timeout (3600 seconds)
- Async processing support
- Progress tracking
- Background job queue (optional)

### Challenge 3: Database Connections

**Problem**: Cloud SQL connection management

**Solution**:
- Cloud SQL Proxy integration
- Connection pooling
- Automatic reconnection
- Transaction management

### Challenge 4: Cold Starts

**Problem**: First request after scale-to-zero is slow

**Solution**:
- Keep minimum instances (if needed)
- Optimize container startup
- Lazy model loading
- Health check endpoints

## Deployment Workflow

### Initial Deployment

1. **Build Container**: Docker build
2. **Push to Registry**: Container Registry / Artifact Registry
3. **Deploy to Cloud Run**: gcloud run deploy
4. **Configure Database**: Cloud SQL connection
5. **Set Environment Variables**: Configuration
6. **Run Migrations**: Database schema setup

### Updates

**Fast Updates** (30 seconds):
```bash
# Update memory only
gcloud run services update mahabir-audio-processing \
    --region us-central1 \
    --memory 8Gi
```

**Full Deployment** (3-5 minutes):
```bash
# Code changes
gcloud run deploy mahabir-audio-processing \
    --source . \
    --region us-central1
```

## Monitoring & Logging

### Cloud Run Logs

```bash
# View logs
gcloud logs tail --service=mahabir-audio-processing

# Filter logs
gcloud logs read "resource.type=cloud_run_revision" \
    --filter="resource.labels.service_name=mahabir-audio-processing"
```

### Metrics

- Request count
- Request latency
- Error rate
- Memory usage
- CPU usage
- Instance count

### Alerts

- High error rate
- Memory exhaustion
- Database connection failures
- Long processing times

## Cost Optimization

### Resource Allocation

- **Right-size Memory**: Allocate only what's needed
- **Scale to Zero**: No cost when idle
- **Efficient Processing**: Optimize transcription speed
- **Connection Pooling**: Reduce database connections

### Cost Breakdown (Example)

- **Cloud Run**: ~$0.10 per 1M requests + compute time
- **Cloud SQL**: ~$10-50/month (depending on tier)
- **Storage**: ~$0.02/GB/month
- **Total**: ~$20-100/month (depending on usage)

## Results

### Performance

- **Response Time**: < 1 second (warm instances)
- **Cold Start**: 10-30 seconds
- **Throughput**: Handles concurrent requests
- **Scalability**: Auto-scales to 10+ instances

### Reliability

- **Uptime**: 99.9%+ (Cloud Run SLA)
- **Auto-Recovery**: Automatic instance restart
- **Database**: Managed backups
- **Monitoring**: Comprehensive logging

### Cost Efficiency

- **Pay-per-use**: Only pay for actual usage
- **Scale to Zero**: No cost when idle
- **Right-sized**: Optimized resource allocation
- **Managed**: Reduced operational overhead

## Lessons Learned

1. **Memory is Critical**: Allocate sufficient memory for Whisper
2. **Connection Pooling**: Essential for database performance
3. **Async Processing**: Needed for long-running tasks
4. **Monitoring**: Comprehensive logging is essential
5. **Cost Optimization**: Right-size resources carefully

## Future Enhancements

- Cloud Build CI/CD pipeline
- Cloud Storage integration
- Cloud Functions for async tasks
- Cloud Scheduler for batch jobs
- Advanced monitoring and alerting

---

**Status**: Production-ready  
**Impact**: Scalable, cost-effective deployment with auto-scaling
