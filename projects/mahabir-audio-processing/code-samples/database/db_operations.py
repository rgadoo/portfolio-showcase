"""
Centralized database operations manager.

Demonstrates the manager pattern for database operations.
"""
from typing import Dict, List, Optional, Any

from database.managers.pooled_base_manager import PooledDatabaseManager
from database.managers.transcript_manager import TranscriptManager
from database.managers.processed_entry_manager import ProcessedEntryManager
from database.managers.review_manager import ReviewManager
from database.managers.correction_pattern_manager import CorrectionPatternManager
from database.managers.media_manager import MediaManager
from database.models import RawTranscript, ProcessedEntry, HumanReview, CorrectionPattern


class DatabaseManager(PooledDatabaseManager):
    """Centralized manager for all database operations."""
    
    def __init__(self):
        """Initialize the database manager with all sub-managers."""
        super().__init__()
        
        # Initialize all managers with pooled connections
        self.transcript_manager = TranscriptManager()
        self.processed_entry_manager = ProcessedEntryManager()
        self.review_manager = ReviewManager() 
        self.correction_pattern_manager = CorrectionPatternManager()
        self.media_manager = MediaManager()
    
    def initialize_database(self) -> bool:
        """Initialize the database by creating all tables.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        return self.create_tables()
    
    # Raw transcript management
    def insert_raw_transcript(self, transcript: RawTranscript) -> Optional[int]:
        """Insert a new raw transcript and return its ID."""
        return self.transcript_manager.insert_raw_transcript(transcript)
    
    def get_raw_transcript(self, transcript_id: int) -> Optional[RawTranscript]:
        """Get a raw transcript by ID."""
        return self.transcript_manager.get_raw_transcript(transcript_id)
    
    def get_all_raw_transcripts(self) -> List[RawTranscript]:
        """Get all raw transcripts."""
        return self.transcript_manager.get_all_raw_transcripts()
    
    def update_raw_transcript_status(self, transcript_id: int, status: str) -> bool:
        """Update a raw transcript's processing status."""
        return self.transcript_manager.update_transcript_status(transcript_id, status)
    
    def delete_raw_transcript(self, transcript_id: int) -> bool:
        """Delete a raw transcript by ID."""
        return self.transcript_manager.delete_raw_transcript(transcript_id)
    
    # Processed entry management
    def insert_processed_entry(self, entry: ProcessedEntry) -> Optional[int]:
        """Insert a new processed entry and return its ID."""
        return self.processed_entry_manager.insert_processed_entry(entry)
    
    def batch_insert_processed_entries(self, entries: List[ProcessedEntry]) -> List[Optional[int]]:
        """Insert multiple processed entries in a single transaction."""
        return self.processed_entry_manager.batch_insert_processed_entries(entries)
    
    def get_processed_entry(self, entry_id: int) -> Optional[ProcessedEntry]:
        """Get a processed entry by ID."""
        return self.processed_entry_manager.get_processed_entry(entry_id)
    
    def get_processed_entries(self, transcript_id: int) -> List[ProcessedEntry]:
        """Get all processed entries for a transcript."""
        return self.processed_entry_manager.get_processed_entries(transcript_id)
    
    def get_entries_needing_openai(self, transcript_id: int) -> List[ProcessedEntry]:
        """Get entries that need OpenAI processing."""
        return self.processed_entry_manager.get_entries_needing_openai(transcript_id)
    
    def update_processed_entries_after_openai(self, entries: List[ProcessedEntry]) -> bool:
        """Update processed entries after OpenAI processing."""
        return self.processed_entry_manager.update_processed_entries_after_openai(entries)
    
    # Review management
    def insert_human_review(self, review: HumanReview) -> Optional[int]:
        """Insert a human review."""
        return self.review_manager.insert_human_review(review)
    
    def get_human_reviews(self, entry_id: int) -> List[HumanReview]:
        """Get all reviews for an entry."""
        return self.review_manager.get_human_reviews(entry_id)
    
    # Correction pattern management
    def insert_or_update_correction_pattern(self, pattern: CorrectionPattern) -> Optional[int]:
        """Insert or update a correction pattern."""
        return self.correction_pattern_manager.insert_or_update_correction_pattern(pattern)
    
    def get_correction_patterns(self, limit: int = 100) -> List[CorrectionPattern]:
        """Get correction patterns."""
        return self.correction_pattern_manager.get_correction_patterns(limit)
    
    def get_correction_dictionary(self) -> Dict[str, str]:
        """Get correction dictionary for Sanskrit corrector."""
        return self.correction_pattern_manager.get_correction_dictionary()
    
    # Media management
    def add_media_file(self, transcript_id: int, file_path: str, 
                      media_type: str, duration: Optional[int] = None) -> Optional[int]:
        """Add a media file for a transcript."""
        return self.media_manager.add_media_file(transcript_id, file_path, media_type, duration)
    
    def get_media_files_for_transcript(self, transcript_id: int) -> List[Dict]:
        """Get all media files for a transcript."""
        return self.media_manager.get_media_files_for_transcript(transcript_id)
