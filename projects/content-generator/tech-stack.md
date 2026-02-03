# Content Generator - Tech Stack

## Overview

Content Generator is built with Python and integrates multiple AI services, audio/video processing libraries, and cloud infrastructure for production-grade content creation.

---

## Core Language

### Python 3.11+

**Why Python:**
- Rich AI/ML ecosystem
- Excellent audio/video processing libraries
- Strong typing with Pydantic
- FastAPI for high-performance APIs

**Key Libraries:**
- `pydantic` - Data validation and settings
- `httpx` - Async HTTP client
- `python-dotenv` - Environment configuration

---

## AI & Content Generation

### OpenAI API

**Models Used:**
| Model | Use Case | Cost |
|-------|----------|------|
| `gpt-4o-mini` | Default content generation | ~$0.375/1M tokens |
| `gpt-4o` | High-quality content | ~$10/1M tokens |

**Features Used:**
- **Chat Completions** - Text generation with structured outputs
- **Structured Outputs** - JSON schema enforcement
- **DALL·E 3** - Hero image generation
- **TTS** - Text-to-speech (alloy, echo, fable, onyx, nova, shimmer)

**Structured Output Configuration:**
```python
response_format={
    "type": "json_schema",
    "json_schema": {
        "name": "article_schema",
        "schema": ARTICLE_SCHEMA,
        "strict": False
    }
}
```

### ElevenLabs

**Use Case:** Premium voice synthesis with custom voices

**Features:**
- Custom voice library
- Stability and similarity boost controls
- Speed control (0.5x - 2.0x)
- Multilingual support (eleven_multilingual_v2)

**Why ElevenLabs:**
- Higher quality voices than OpenAI TTS
- Custom voice cloning capability
- Better for meditation/narration content

**Implementation:**
```python
from elevenlabs import generate, set_api_key

audio = generate(
    text=script_text,
    voice=voice_id,
    model="eleven_multilingual_v2"
)
```

---

## Audio Processing

### OpenAI TTS

**Voices Available:**
| Voice | Character |
|-------|-----------|
| `alloy` | Neutral, versatile |
| `echo` | Warm, conversational |
| `fable` | Expressive, storytelling |
| `onyx` | Deep, authoritative |
| `nova` | Friendly, upbeat |
| `shimmer` | Soft, calming |

**Models:**
- `tts-1` - Standard quality, faster
- `tts-1-hd` - High definition, better quality

**Speed Control:** 0.25x to 4.0x

### librosa

**Use Case:** Audio analysis for waveform visualization

**Features Used:**
- Audio loading and sampling
- Waveform extraction
- Time-domain analysis
- Sample rate handling

**Implementation:**
```python
import librosa

# Load audio file
y, sr = librosa.load(audio_path, sr=22050)

# Get waveform slice at specific time
def get_waveform_at_time(y, sr, time, window_size=0.1):
    start_sample = int(time * sr)
    end_sample = int((time + window_size) * sr)
    return y[start_sample:end_sample]
```

---

## Video Processing

### MoviePy

**Use Case:** Video composition, editing, and encoding

**Features Used:**
- Image sequence to video conversion
- Audio track attachment
- Text overlay (subtitles)
- Video concatenation
- Export with codec settings

**Implementation:**
```python
from moviepy.editor import (
    ImageSequenceClip, 
    AudioFileClip, 
    TextClip, 
    CompositeVideoClip
)

# Create video from frames
video = ImageSequenceClip(frames, fps=30)

# Attach audio
audio = AudioFileClip(audio_path)
video = video.set_audio(audio)

# Add subtitles
subtitle_clip = TextClip(
    text,
    fontsize=48,
    color='white',
    bg_color='rgba(0,0,0,0.7)'
).set_position(('center', 'bottom'))

final = CompositeVideoClip([video, subtitle_clip])
final.write_videofile(output_path, codec='libx264')
```

### matplotlib

**Use Case:** Waveform rendering for video frames

**Features Used:**
- Figure creation with custom size
- Line plots for waveform
- Custom styling (colors, backgrounds)
- Save to numpy array for MoviePy

**Implementation:**
```python
import matplotlib.pyplot as plt
import numpy as np

def render_waveform_frame(waveform_data, width=1920, height=1080):
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.plot(waveform_data, color='#00ff88', linewidth=2)
    ax.set_facecolor('#1a1a2e')
    ax.axis('off')
    
    # Convert to numpy array
    fig.canvas.draw()
    frame = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return frame
```

### FFmpeg

**Use Case:** Video encoding with optimized settings

**Settings:**
```python
# MoviePy uses FFmpeg under the hood
video.write_videofile(
    output_path,
    codec='libx264',
    audio_codec='aac',
    audio_bitrate='192k',
    preset='medium',
    ffmpeg_params=['-crf', '23']
)
```

**Resolution Profiles:**
| Profile | Resolution | Video Bitrate |
|---------|------------|---------------|
| 1080p | 1920x1080 | ~8 Mbps |
| 720p | 1280x720 | ~5 Mbps |
| 480p | 854x480 | ~2.5 Mbps |

---

## Backend Framework

### FastAPI

**Why FastAPI:**
- High performance (Starlette + Pydantic)
- Automatic OpenAPI documentation
- Native async support
- Type hints integration

**Key Features Used:**
- Dependency injection
- Request validation
- Background tasks (for long audio/video processing)
- File uploads

---

## Database

### PostgreSQL

**Use Case:** Staging database for drafts, queues, operations

**Key Tables:**
| Table | Purpose |
|-------|---------|
| `video_metadata` | YouTube video sync data |
| `transcript_queue` | Processing queue with retry |
| `article_drafts` | Article content drafts |
| `course_drafts` | Course content drafts |
| `quiz_drafts` | Quiz content drafts |
| `audio_drafts` | Audio content drafts |
| `video_drafts` | Video content drafts |
| `staged_content` | Review-ready content |
| `content_operations` | Operation tracking |

**Why PostgreSQL:**
- JSONB support for flexible content storage
- Robust transaction support
- Excellent performance

---

## Cloud Integration

### Google Cloud Storage (GCS)

**Use Case:** Media file storage with multi-tenant paths

**Path Structure:**
```
{bucket}/
└── {instanceId}/
    ├── audio/{pillar}/{category}/{filename}.mp3
    ├── video/{pillar}/{category}/{filename}.mp4
    ├── images/pages/{slug}/{filename}.jpg
    ├── images/thumbnails/{pillar}/{category}/{slug}.jpg
    └── transcripts/{contentId}.txt
```

**Implementation:**
```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

def upload_media(instance_id, content_type, pillar, category, filename, data):
    path = f"{instance_id}/{content_type}/{pillar}/{category}/{filename}"
    blob = bucket.blob(path)
    blob.upload_from_string(data, content_type=get_mime_type(filename))
    return blob.public_url
```

### Firebase Admin SDK

**Use Case:** Publishing content documents to Firestore

**Operations:**
- Document creation with auto-ID
- Batch writes
- Transaction support

**Implementation:**
```python
import firebase_admin
from firebase_admin import credentials, firestore

db = firestore.client()

def publish_content(instance_id, content):
    doc_ref = db.collection('content').document()
    doc_ref.set({
        'id': doc_ref.id,
        'instanceId': instance_id,
        'contentType': content['type'],
        'title': content['title'],
        # ... other fields
        'createdAt': firestore.SERVER_TIMESTAMP,
        'published': True
    })
    return doc_ref.id
```

### YouTube Data API v3

**Use Case:** Channel sync and transcript fetching

**Endpoints Used:**
- `channels.list` - Channel information
- `playlistItems.list` - Playlist videos
- `videos.list` - Video details

**Transcript Fetching:**
```python
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript(video_id)
full_text = ' '.join([entry['text'] for entry in transcript])
```

---

## Data Validation

### Pydantic

**Use Case:** Data validation, schemas, settings management

**Content Schemas:**
```python
class ArticleSection(BaseModel):
    heading: str = Field(min_length=5)
    content: str = Field(min_length=100)

class AudioSegment(BaseModel):
    text: str
    pause_before: float = 0.0
    pause_after: float = 0.5
    emphasis: Optional[str] = None
    tone_hint: Optional[str] = None

class VideoSettings(BaseModel):
    resolution: Literal["1080p", "720p", "480p"] = "1080p"
    style: Literal["waveform", "static", "slideshow"] = "waveform"
    subtitle_enabled: bool = True
```

---

## Architecture Patterns

### Strategy Pattern (Video Styles)

```python
class VideoStyleGenerator(ABC):
    @abstractmethod
    def generate(self, audio_path: str, output_path: str) -> None:
        pass

class WaveformGenerator(VideoStyleGenerator):
    """Animated waveform visualization"""
    pass

class StaticBackgroundGenerator(VideoStyleGenerator):
    """Static image with audio"""
    pass
```

### Factory Pattern (Draft Services)

```python
def get_draft_service(content_type: str) -> BaseDraftService:
    return {
        "article": ArticleDraftService,
        "course": CourseDraftService,
        "quiz": QuizDraftService,
        "audio": AudioDraftService,
        "video": VideoDraftService,
    }[content_type]()
```

### Service Layer Pattern

```
API Routes → Services → Data Access
              │
              ├── ArticleGenerationService
              ├── CourseGenerationService
              ├── QuizGenerationService
              ├── AudioGenerationService
              ├── VoiceService
              ├── VideoGenerationService
              ├── SubtitleService
              ├── GCSStorageService
              └── FirestorePublisher
```

---

## Development Tools

### Code Quality
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `mypy` - Type checking

### Testing
- `pytest` - Test framework
- `pytest-asyncio` - Async test support

---

## Tech Stack Summary

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI |
| **AI/LLM** | OpenAI (GPT-4o, DALL·E, TTS) |
| **Voice** | OpenAI TTS, ElevenLabs |
| **Audio** | librosa |
| **Video** | MoviePy, matplotlib, FFmpeg |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic |
| **Cloud Storage** | Google Cloud Storage |
| **Publishing** | Firebase Admin SDK (Firestore) |
| **YouTube** | YouTube Data API v3 |
