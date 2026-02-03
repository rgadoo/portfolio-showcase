# Content Generator - Architecture

## System Overview

Content Generator is a comprehensive AI content platform with multiple generation pathways, audio/video processing, and multi-tenant publishing to Firebase and GCS.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Content Generator Platform                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     CONTENT GENERATION LAYER                         │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │   │
│  │   │   Article    │    │    Course    │    │     Quiz     │        │   │
│  │   │  Generator   │    │  Generator   │    │  Generator   │        │   │
│  │   └──────────────┘    └──────────────┘    └──────────────┘        │   │
│  │                                                                     │   │
│  │   ┌──────────────┐    ┌──────────────┐                             │   │
│  │   │    Audio     │    │   YouTube    │                             │   │
│  │   │  Generator   │    │    Sync      │                             │   │
│  │   └──────────────┘    └──────────────┘                             │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        AUDIO PIPELINE                                │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │   │
│  │   │    Voice     │    │   OpenAI     │    │  ElevenLabs  │        │   │
│  │   │   Service    │───▶│     TTS      │    │    Voice     │        │   │
│  │   └──────────────┘    └──────────────┘    └──────────────┘        │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        VIDEO PIPELINE                                │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │   │
│  │   │   Waveform   │    │   Subtitle   │    │    Video     │        │   │
│  │   │  Generator   │    │   Service    │    │   Encoder    │        │   │
│  │   └──────────────┘    └──────────────┘    └──────────────┘        │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     PUBLISHING LAYER                                 │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │   │
│  │   │     GCS      │    │  Firestore   │    │   Operation  │        │   │
│  │   │   Storage    │    │  Publisher   │    │   Tracking   │        │   │
│  │   └──────────────┘    └──────────────┘    └──────────────┘        │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Content Generation Layer

### Article Generation Service

**Responsibility:** Generate structured articles from prompts or transcripts.

**Features:**
- AI-powered content generation with OpenAI
- Structured JSON output (title, sections, paragraphs)
- Optional FAQ generation
- Hero image generation via DALL·E
- Taxonomy validation (pillar, category, tags)
- SEO metadata generation

**Workflow:**
```
Prompt → PromptBuilder → OpenAI API → Validation → PostProcessing → ArticleDraft
```

### Course Generation Service

**Responsibility:** Generate complete course structures with modules and lessons.

**Features:**
- Multi-module course structure
- Lessons with objectives, notes, resources
- Instructor info management
- Difficulty levels (beginner, intermediate, advanced)
- Enrollment types (open, admin-only, invite-only, paid)
- Duration calculation

**Schema:**
```python
Course
├── title, description, difficulty
├── instructor: {name, bio, image}
├── modules[]
│   ├── title, description, objectives[]
│   └── lessons[]
│       ├── title, description
│       ├── content, notes, resources[]
│       └── duration, order
└── settings: {enrollment, pricing}
```

### Quiz Generation Service

**Responsibility:** Generate quizzes with multiple question types.

**Features:**
- Question types: multiple-choice, true/false, short answer
- Configurable difficulty (easy, medium, hard)
- Question count control
- Settings: passing score, time limit, shuffle, review mode
- Answer explanations

**Schema:**
```python
Quiz
├── title, description, difficulty
├── questions[]
│   ├── question, type
│   ├── options[] (for multiple choice)
│   ├── correct_answer
│   └── explanation
└── settings: {passing_score, time_limit, shuffle}
```

### Audio Generation Service

**Responsibility:** Generate audio scripts and synthesize speech.

**Features:**
- Script generation with AI (podcast, narration, dialogue, meditation, tutorial)
- Segments with pause timing, emphasis, tone hints
- Voice recommendations per provider
- Duration estimation
- Target audience customization

**Script Schema:**
```python
AudioScript
├── title, format (podcast, narration, meditation, etc.)
├── segments[]
│   ├── text, speaker (optional)
│   ├── pause_before, pause_after
│   ├── emphasis, tone_hint
│   └── duration_estimate
└── voice_settings: {provider, voice_id, speed}
```

### YouTube Sync Service

**Responsibility:** Synchronize YouTube channels and import transcripts.

**Features:**
- Channel and playlist synchronization
- Video metadata extraction
- Transcript fetching and storage
- Rate limit handling with Retry-After support
- Quota tracking

---

## Audio Pipeline

### Voice Service

**Responsibility:** Abstract TTS providers behind a unified interface.

**Providers:**

| Provider | Voices | Speed Range | Features |
|----------|--------|-------------|----------|
| **OpenAI TTS** | alloy, echo, fable, onyx, nova, shimmer | 0.25x - 4.0x | tts-1, tts-1-hd models |
| **ElevenLabs** | Custom voice library | 0.5x - 2.0x | Stability, similarity boost |

**Implementation:**
```python
class VoiceService:
    def generate_audio(self, text: str, settings: VoiceSettings) -> bytes:
        if settings.provider == "openai":
            return self._generate_openai(text, settings)
        elif settings.provider == "elevenlabs":
            return self._generate_elevenlabs(text, settings)
    
    def _generate_openai(self, text, settings):
        response = openai.audio.speech.create(
            model=settings.model,  # tts-1 or tts-1-hd
            voice=settings.voice,  # alloy, echo, fable, etc.
            input=text,
            speed=settings.speed   # 0.25 to 4.0
        )
        return response.content
    
    def _generate_elevenlabs(self, text, settings):
        audio = elevenlabs.generate(
            text=text,
            voice=settings.voice_id,
            model="eleven_multilingual_v2"
        )
        return audio
```

**Audio Processing:**
- Format validation (MP3, WAV)
- Duration calculation
- Segment combination for long content
- Preview generation for testing

---

## Video Pipeline

### Video Generation Service

**Responsibility:** Convert audio content to video with visualization.

**Workflow:**
```
AudioDraft → promote_to_video() → VideoDraft
    ↓
Generate video with style (waveform, static, slides)
    ↓
Add subtitles (burned-in)
    ↓
Encode with FFmpeg
    ↓
Upload to GCS
```

### Waveform Generator

**Responsibility:** Create animated audio visualization synced to playback.

**Implementation:**
```python
class WaveformGenerator:
    def generate(self, audio_path: str, output_path: str, subtitles: list):
        # Load audio and analyze with librosa
        y, sr = librosa.load(audio_path)
        
        # Calculate waveform for each frame
        frames = []
        for frame_time in frame_times:
            waveform_slice = self._get_waveform_at_time(y, sr, frame_time)
            frame = self._render_frame(waveform_slice, frame_time, subtitles)
            frames.append(frame)
        
        # Compose video with MoviePy
        video = ImageSequenceClip(frames, fps=30)
        audio = AudioFileClip(audio_path)
        final = video.set_audio(audio)
        final.write_videofile(output_path, codec='libx264')
```

**Features:**
- Real-time waveform sync with audio
- Customizable colors and styling
- 30 FPS smooth animation
- Matplotlib rendering

### Subtitle Service

**Responsibility:** Generate and burn subtitles into video.

**Features:**
- Generate subtitles from script segments or transcript
- Industry-standard timing (2.5 words/second)
- Text formatting: 42 chars/line, max 2 lines
- SRT file generation
- YouTube-style burned-in subtitles with background boxes

**Implementation:**
```python
class SubtitleService:
    WORDS_PER_SECOND = 2.5
    MAX_CHARS_PER_LINE = 42
    MAX_LINES = 2
    
    def generate_subtitles(self, script_segments: list) -> list:
        subtitles = []
        current_time = 0.0
        
        for segment in script_segments:
            words = segment.text.split()
            duration = len(words) / self.WORDS_PER_SECOND
            
            subtitles.append({
                "start": current_time,
                "end": current_time + duration,
                "text": self._wrap_text(segment.text)
            })
            
            current_time += duration + segment.pause_after
        
        return subtitles
    
    def burn_subtitles(self, video_clip, subtitles):
        """Add YouTube-style subtitles with background boxes."""
        subtitle_clips = []
        for sub in subtitles:
            txt_clip = TextClip(
                sub["text"],
                fontsize=48,
                color='white',
                bg_color='rgba(0,0,0,0.7)',
                method='caption'
            ).set_position(('center', 'bottom'))
            .set_start(sub["start"])
            .set_end(sub["end"])
            subtitle_clips.append(txt_clip)
        
        return CompositeVideoClip([video_clip] + subtitle_clips)
```

### Video Encoding

**Resolution Profiles:**
| Profile | Resolution | Bitrate |
|---------|------------|---------|
| 1080p | 1920x1080 | 8 Mbps |
| 720p | 1280x720 | 5 Mbps |
| 480p | 854x480 | 2.5 Mbps |

**FFmpeg Settings:**
- Codec: libx264
- Audio: AAC 192kbps
- Preset: medium (balance speed/quality)

---

## Publishing Layer

### GCS Storage Service

**Responsibility:** Upload media files with multi-tenant path isolation.

**Path Structure:**
```
{bucket}/
├── {instanceId}/
│   ├── audio/
│   │   └── {pillar}/{category}/{filename}.mp3
│   ├── video/
│   │   └── {pillar}/{category}/{filename}.mp4
│   ├── images/
│   │   ├── pages/{slug}/{filename}.jpg
│   │   └── thumbnails/{pillar}/{category}/{slug}.jpg
│   ├── transcripts/
│   │   └── {contentId}.txt
│   └── resources/
│       └── {filename}
```

**Features:**
- Automatic MIME type detection
- Public URL generation
- Cache control headers (max-age=31536000 for media)
- File existence checking
- Copy/delete operations

### Firestore Publisher

**Responsibility:** Publish content documents to Firestore.

**Content Type Mapping:**
| Generator | Firestore `contentType` |
|-----------|------------------------|
| Article | `page` |
| Course | `course` |
| Quiz | `quiz` |
| Audio | `audio` |
| Video | `video` |

**Document Structure:**
```python
{
    "id": "generated-uuid",
    "instanceId": "tenant-id",
    "contentType": "audio",
    "title": "...",
    "description": "...",
    "pillar": "pillar-id",
    "category": "category-id",
    "tags": ["tag1", "tag2"],
    "mediaPath": "gs://bucket/instance/audio/...",
    "thumbnailPath": "gs://bucket/instance/images/...",
    "duration": 180,  # seconds
    "published": true,
    "createdAt": timestamp,
    "updatedAt": timestamp
}
```

---

## Staging Workflow

### 3-Stage Content Lifecycle

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   DRAFT     │─────▶│   STAGED    │─────▶│  PUBLISHED  │
│ (PostgreSQL)│      │ (PostgreSQL)│      │ (Firestore) │
└─────────────┘      └─────────────┘      └─────────────┘
     │                     │                     │
     │                     │                     │
     ▼                     ▼                     ▼
 Local files          Local files           GCS + Firestore
 Work in progress     Ready for review      Live content
```

**Draft Stage:**
- Content stored in PostgreSQL
- Media files stored locally
- Can be edited, regenerated, deleted
- Status: `draft`

**Staged Stage:**
- Moved from draft to staging table
- Ready for review
- Can be approved or rejected
- Status: `staged`, `approved`, `rejected`

**Published Stage:**
- Media uploaded to GCS
- Content document created in Firestore
- Live and accessible
- Status: `published`

---

## Validation Architecture

### 5-Layer Validation Chain

```
Request
   │
   ▼
┌─────────────────────────────────────┐
│ Layer 1: Taxonomy Validation        │  Pre-API (fail-fast)
│ - Pillar exists                     │
│ - Category exists under pillar      │
│ - Tags exist in instance            │
└─────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────┐
│ Layer 2: OpenAI Schema Validation   │  During generation
│ - JSON schema enforcement           │
│ - Required fields                   │
│ - Type checking                     │
└─────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────┐
│ Layer 3: Content Quality Validation │  Post-generation
│ - Placeholder detection             │
│ - Minimum lengths                   │
│ - Structure validation              │
│ - Educational language check        │
└─────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────┐
│ Layer 4: Pydantic Validation        │  Pre-save
│ - Type coercion                     │
│ - Field constraints                 │
│ - Custom validators                 │
└─────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────┐
│ Layer 5: Publisher Validation       │  Pre-publish
│ - Firestore-ready format            │
│ - Required fields for production    │
│ - Final sanity checks               │
└─────────────────────────────────────┘
   │
   ▼
Published
```

---

## Data Flow: Complete Example

### Text → Audio → Video → Publish

```
1. USER INPUT
   └─> "Create a 3-minute meditation audio about breath awareness"

2. AI GENERATION (Audio Generation Service)
   └─> OpenAI API with audio script schema
   └─> Output: AudioScript with segments, timing, voice settings

3. VOICE SYNTHESIS (Voice Service)
   └─> Select provider (OpenAI TTS or ElevenLabs)
   └─> Generate audio file (.mp3)
   └─> Validate: format, duration, file size

4. VIDEO GENERATION (Video Generation Service)
   └─> Promote audio draft to video draft
   └─> Generate subtitles from script segments
   └─> Create waveform visualization (librosa + matplotlib)
   └─> Compose video with MoviePy
   └─> Burn in subtitles
   └─> Encode with FFmpeg (.mp4)

5. STAGING (Draft → Staged)
   └─> Save to staged_content table
   └─> Status: 'staged'
   └─> Media files: local storage

6. REVIEW (Manual)
   └─> Preview in web UI
   └─> Approve → Status: 'approved'

7. PUBLISHING (Publisher Service)
   └─> Upload audio to GCS: {instance}/audio/{pillar}/{category}/...
   └─> Upload video to GCS: {instance}/video/{pillar}/{category}/...
   └─> Upload thumbnail to GCS
   └─> Create Firestore document (contentType: 'video')
   └─> Update status: 'published'

8. LIVE
   └─> Available on Nandi Platform
   └─> Accessible via content player
```

---

## Design Patterns

### Strategy Pattern (Video Styles)

```python
class VideoStyleGenerator(ABC):
    @abstractmethod
    def generate(self, audio_path: str, output_path: str) -> None:
        pass

class WaveformGenerator(VideoStyleGenerator):
    def generate(self, audio_path, output_path):
        # Animated waveform visualization
        pass

class StaticBackgroundGenerator(VideoStyleGenerator):
    def generate(self, audio_path, output_path):
        # Static image with audio
        pass

class SlideshowGenerator(VideoStyleGenerator):
    def generate(self, audio_path, output_path):
        # Multiple images as slides
        pass
```

### Service Layer Pattern

```
┌─────────────────┐
│   API Layer     │  FastAPI routes
└────────┬────────┘
         │
┌────────▼────────┐
│  Service Layer  │  Business logic
│  - Generation   │
│  - Voice        │
│  - Video        │
│  - Publishing   │
└────────┬────────┘
         │
┌────────▼────────┐
│   Data Layer    │  PostgreSQL, Firestore, GCS
└─────────────────┘
```

### Factory Pattern (Draft Services)

```python
def get_draft_service(content_type: str) -> BaseDraftService:
    services = {
        "article": ArticleDraftService,
        "course": CourseDraftService,
        "quiz": QuizDraftService,
        "audio": AudioDraftService,
        "video": VideoDraftService,
    }
    return services[content_type]()
```

---

## Security & Multi-Tenancy

### Instance Isolation

- All content scoped by `instanceId`
- GCS paths prefixed with instance ID
- Firestore queries filter by instance
- Validation ensures instance exists

### API Security

- API keys in environment variables
- No sensitive data in logs
- Rate limiting respected
- Fail-fast on invalid input

---

## Performance Optimizations

1. **Fail-Fast Validation**: Taxonomy check before expensive API calls
2. **Streaming Audio**: Large audio files processed in chunks
3. **Frame Caching**: Video frames cached during generation
4. **Connection Pooling**: PostgreSQL connection management
5. **Async Processing**: Background tasks for long operations
