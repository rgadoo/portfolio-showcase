#!/usr/bin/env python3
"""
Centralized Configuration Management
All configuration values, constants, and settings
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class APIConfig:
    """API keys and credentials"""
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    elevenlabs_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ELEVENLABS_API_KEY"))
    anthropic_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    elevenlabs_voice_id: str = field(default_factory=lambda: os.getenv("ELEVENLABS_VOICE_ID", "default_voice_id"))


@dataclass
class PathConfig:
    """File and directory paths"""
    # Base paths
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = field(default_factory=lambda: Path("data"))
    
    # Data subdirectories
    books_dir: Path = field(default_factory=lambda: Path("data/books"))
    chroma_dir: Path = field(default_factory=lambda: Path("data/chroma_db"))
    output_dir: Path = field(default_factory=lambda: Path("data/output"))
    assets_dir: Path = field(default_factory=lambda: Path("assets"))
    logs_dir: Path = field(default_factory=lambda: Path("logs"))


@dataclass
class IngestionConfig:
    """Book ingestion settings"""
    chunk_size: int = 3000
    chunk_overlap: int = 300
    separators: List[str] = field(default_factory=lambda: ["\n\n", "\n", ". ", " ", ""])
    supported_formats: List[str] = field(default_factory=lambda: ["*.txt", "*.md"])
    collection_name: str = "book_content"


@dataclass
class ScriptConfig:
    """Script generation settings"""
    min_word_count: int = 100
    max_word_count: int = 120
    target_duration_seconds: int = 40
    default_n_results: int = 3
    
    # LLM settings
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    openai_model: str = "gpt-4-turbo-preview"
    max_tokens: int = 500


@dataclass
class VoiceConfig:
    """Voice generation settings"""
    default_service: str = "elevenlabs"
    
    # OpenAI TTS settings
    openai_model: str = "tts-1"
    openai_voice: str = "nova"
    openai_speed: float = 1.0
    
    # ElevenLabs settings
    elevenlabs_model: str = "eleven_multilingual_v2"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True


@dataclass
class VideoConfig:
    """Video creation settings"""
    # Dimensions
    width: int = 1080
    height: int = 1920  # 9:16 aspect ratio
    
    # Timing
    fps: int = 30
    default_duration: int = 40
    
    # Caption settings
    caption_font: str = "Arial-Bold"
    caption_font_size: int = 60
    caption_color: str = "white"
    caption_bg_color: str = "black"
    caption_bg_opacity: float = 0.7


@dataclass
class PlatformConfig:
    """Platform-specific video specifications"""
    platforms: dict = field(default_factory=lambda: {
        "tiktok": {"width": 1080, "height": 1920, "aspect_ratio": "9:16"},
        "instagram_reels": {"width": 1080, "height": 1920, "aspect_ratio": "9:16"},
        "youtube_shorts": {"width": 1080, "height": 1920, "aspect_ratio": "9:16"},
        "twitter": {"width": 1920, "height": 1080, "aspect_ratio": "16:9"},
    })


@dataclass
class UIConfig:
    """Gradio UI settings"""
    title: str = "Social Media Agent"
    description: str = "Convert book content to social media videos"
    theme: str = "default"
    share: bool = False
    server_port: int = 7860


class Config:
    """Main configuration class combining all configs"""
    
    def __init__(self):
        self.api = APIConfig()
        self.paths = PathConfig()
        self.ingestion = IngestionConfig()
        self.script = ScriptConfig()
        self.voice = VoiceConfig()
        self.video = VideoConfig()
        self.platform = PlatformConfig()
        self.ui = UIConfig()
        
        # Ensure directories exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.paths.data_dir,
            self.paths.books_dir,
            self.paths.chroma_dir,
            self.paths.output_dir,
            self.paths.assets_dir,
            self.paths.logs_dir,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate configuration"""
        errors = []
        
        # Check API keys
        if not self.api.anthropic_api_key and not self.api.openai_api_key:
            errors.append("At least one LLM API key (ANTHROPIC_API_KEY or OPENAI_API_KEY) is required")
        
        if not self.api.elevenlabs_api_key:
            errors.append("ELEVENLABS_API_KEY is required")
        
        # Check directories
        if not self.paths.books_dir.exists():
            errors.append(f"Books directory does not exist: {self.paths.books_dir}")
        
        return len(errors) == 0, errors


# Global configuration instance
config = Config()
