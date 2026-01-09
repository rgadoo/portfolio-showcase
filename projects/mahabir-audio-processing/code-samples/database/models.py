"""
Database models for Mahabir Audio Processing application.

Demonstrates data model structure with serialization methods.
"""
import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class RawTranscript:
    """Model for raw uploaded SRT files."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        filename: str = "",
        upload_timestamp: Optional[datetime] = None,
        file_content: str = "",
        processing_status: str = "pending"
    ):
        self.id = id
        self.filename = filename
        self.upload_timestamp = upload_timestamp or datetime.now()
        self.file_content = file_content
        self.processing_status = processing_status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "upload_timestamp": self.upload_timestamp.isoformat() if self.upload_timestamp else None,
            "file_content": self.file_content,
            "processing_status": self.processing_status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RawTranscript':
        """Create model from dictionary."""
        upload_timestamp = None
        if data.get("upload_timestamp"):
            if isinstance(data["upload_timestamp"], str):
                upload_timestamp = datetime.fromisoformat(data["upload_timestamp"])
            else:
                upload_timestamp = data["upload_timestamp"]
            
        return cls(
            id=data.get("id"),
            filename=data.get("filename", ""),
            upload_timestamp=upload_timestamp,
            file_content=data.get("file_content", ""),
            processing_status=data.get("processing_status", "pending")
        )


class ProcessedEntry:
    """Model for processed transcript entries."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        raw_transcript_id: Optional[int] = None,
        timestamp_start: str = "",
        timestamp_end: str = "",
        original_text: str = "",
        corrected_text: str = "",
        corrections_made: Optional[List[Dict[str, Any]]] = None,
        confidence_score: float = 0.0,
        needs_review: bool = False,
        api_cost: float = 0.0,
        created_at: Optional[datetime] = None,
        needs_openai: bool = False,
        openai_processed: bool = False
    ):
        self.id = id
        self.raw_transcript_id = raw_transcript_id
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.original_text = original_text
        self.corrected_text = corrected_text
        self.corrections_made = corrections_made or []
        self.confidence_score = confidence_score
        self.needs_review = needs_review
        self.api_cost = api_cost
        self.created_at = created_at or datetime.now()
        self.needs_openai = needs_openai
        self.openai_processed = openai_processed
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "raw_transcript_id": self.raw_transcript_id,
            "timestamp_start": self.timestamp_start,
            "timestamp_end": self.timestamp_end,
            "original_text": self.original_text,
            "corrected_text": self.corrected_text,
            "corrections_made": self.corrections_made,
            "confidence_score": self.confidence_score,
            "needs_review": self.needs_review,
            "api_cost": self.api_cost,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "needs_openai": self.needs_openai,
            "openai_processed": self.openai_processed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProcessedEntry':
        """Create model from dictionary."""
        created_at = None
        if data.get("created_at"):
            if isinstance(data["created_at"], str):
                created_at = datetime.fromisoformat(data["created_at"])
            else:
                created_at = data["created_at"]
        
        return cls(
            id=data.get("id"),
            raw_transcript_id=data.get("raw_transcript_id"),
            timestamp_start=data.get("timestamp_start", ""),
            timestamp_end=data.get("timestamp_end", ""),
            original_text=data.get("original_text", ""),
            corrected_text=data.get("corrected_text", ""),
            corrections_made=data.get("corrections_made", []),
            confidence_score=data.get("confidence_score", 0.0),
            needs_review=data.get("needs_review", False),
            api_cost=data.get("api_cost", 0.0),
            created_at=created_at,
            needs_openai=data.get("needs_openai", False),
            openai_processed=data.get("openai_processed", False)
        )


class CorrectionPattern:
    """Model for correction patterns."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        original_term: str = "",
        corrected_term: str = "",
        context: str = "",
        frequency: int = 1,
        confidence: float = 0.0,
        first_seen: Optional[datetime] = None,
        last_seen: Optional[datetime] = None
    ):
        self.id = id
        self.original_term = original_term
        self.corrected_term = corrected_term
        self.context = context
        self.frequency = frequency
        self.confidence = confidence
        self.first_seen = first_seen or datetime.now()
        self.last_seen = last_seen or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "original_term": self.original_term,
            "corrected_term": self.corrected_term,
            "context": self.context,
            "frequency": self.frequency,
            "confidence": self.confidence,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None
        }
