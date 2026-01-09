"""
Main correction service for Mahabir Audio Processing application.

This module coordinates the SRT parsing, local processing, OpenAI processing, and database operations.
It implements a two-stage approach where entries are first processed locally,
then selectively sent to OpenAI based on user review.
"""
import os
import sys
import time
from typing import Dict, List, Optional, Any, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BATCH_SIZE, MAX_BATCH_TOKENS, CONTEXT_WINDOW_SIZE
from database.models import RawTranscript, ProcessedEntry, CorrectionPattern
from database.db_operations import DatabaseManager
from services.srt_parser import SRTParser, SRTEntry
from services.openai_client import OpenAIClient
from services.local_processor import LocalProcessor


class CorrectionService:
    """Service for processing and correcting SRT files."""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """Initialize the correction service."""
        self.db_manager = db_manager or DatabaseManager()
        self.srt_parser = SRTParser()
        self.openai_client = OpenAIClient()
        self.local_processor = LocalProcessor()
    
    def process_srt_file(self, file_id: int) -> Tuple[bool, str]:
        """
        Main workflow for processing an SRT file using the two-stage approach.
        Stage 1: Process entries locally using SanskritCorrector
        Stage 2: Mark entries that need OpenAI processing for user review
        
        Args:
            file_id: ID of the raw transcript in the database
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Validate and prepare transcript
            transcript = self._validate_and_prepare_transcript(file_id)
            if not transcript:
                return False, f"Raw transcript with ID {file_id} not found"
            
            # Parse and batch entries
            batches = self._parse_and_batch_entries(transcript, file_id)
            if not batches:
                return False, "No valid SRT entries found in the file"
            
            # Process all batches locally
            total_entries, entries_needing_openai = self._process_all_batches_locally(file_id, batches)
            
            # Update final status
            self._update_processing_status(file_id, "processed")
            
            return True, f"Successfully processed {total_entries} entries locally. {entries_needing_openai} entries marked for OpenAI processing."
        
        except Exception as e:
            self._update_processing_status(file_id, "error")
            return False, f"Error processing SRT file: {str(e)}"
    
    def process_entries_with_openai(self, file_id: int, entry_ids: List[int]) -> Tuple[bool, str]:
        """
        Process selected entries with OpenAI after user review.
        
        Args:
            file_id: ID of the raw transcript
            entry_ids: List of entry IDs to process with OpenAI
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Update status to openai_processing
            self.db_manager.update_raw_transcript_status(file_id, "openai_processing")
            
            # Get the entries to process
            entries_to_process = []
            for entry_id in entry_ids:
                entry = self.db_manager.get_processed_entry(entry_id)
                if entry and not entry.openai_processed:
                    entries_to_process.append(entry)
            
            if not entries_to_process:
                self.db_manager.update_raw_transcript_status(file_id, "processed")
                return False, "No entries found that need OpenAI processing"
            
            # Convert ProcessedEntry objects to SRTEntry objects
            srt_entries = []
            for i, entry in enumerate(entries_to_process):
                srt_entry = SRTEntry(
                    index=i+1,
                    start_time=entry.timestamp_start,
                    end_time=entry.timestamp_end,
                    text=entry.original_text
                )
                srt_entries.append(srt_entry)
            
            # Create batches for processing
            batches = self.srt_parser.create_batches(
                srt_entries, 
                target_batch_size=BATCH_SIZE,
                max_tokens=MAX_BATCH_TOKENS
            )
            
            # Process each batch with OpenAI
            total_processed = 0
            total_cost = 0.0
            
            for batch_index, batch in enumerate(batches):
                try:
                    # Process batch with OpenAI
                    corrections = self.openai_client.correct_transcript_batch(batch)
                    
                    # Map corrections back to entries
                    updated_entries = self.openai_client.map_corrections_to_entries(
                        entries_to_process, corrections
                    )
                    
                    # Update database
                    self.db_manager.update_processed_entries_after_openai(updated_entries)
                    
                    # Track costs
                    batch_cost = sum(entry.api_cost for entry in updated_entries)
                    total_cost += batch_cost
                    total_processed += len(updated_entries)
                    
                except Exception as e:
                    print(f"Error processing batch {batch_index + 1}: {e}")
                    continue
            
            # Update final status
            self.db_manager.update_raw_transcript_status(file_id, "completed")
            
            return True, f"Successfully processed {total_processed} entries with OpenAI. Total cost: ${total_cost:.4f}"
        
        except Exception as e:
            self._update_processing_status(file_id, "error")
            return False, f"Error processing entries with OpenAI: {str(e)}"
    
    def _validate_and_prepare_transcript(self, file_id: int) -> Optional[RawTranscript]:
        """Validate transcript exists and is ready for processing."""
        transcript = self.db_manager.get_raw_transcript(file_id)
        if not transcript:
            return None
        
        # Update status to processing
        self.db_manager.update_raw_transcript_status(file_id, "processing")
        return transcript
    
    def _parse_and_batch_entries(self, transcript: RawTranscript, file_id: int) -> List[List[SRTEntry]]:
        """Parse SRT content and create batches."""
        entries = self.srt_parser.parse_srt_file(transcript.file_content)
        
        # Create batches for processing
        batches = self.srt_parser.create_batches(
            entries,
            target_batch_size=BATCH_SIZE,
            max_tokens=MAX_BATCH_TOKENS
        )
        
        return batches
    
    def _process_all_batches_locally(self, file_id: int, batches: List[List[SRTEntry]]) -> Tuple[int, int]:
        """Process all batches locally and return statistics."""
        total_entries = 0
        entries_needing_openai = 0
        
        for batch in batches:
            # Process batch locally
            processed_results = self.local_processor.process_entries(batch)
            
            # Save to database
            processed_entries = []
            for i, result in enumerate(processed_results):
                entry = ProcessedEntry(
                    raw_transcript_id=file_id,
                    timestamp_start=batch[i].start_time,
                    timestamp_end=batch[i].end_time,
                    original_text=batch[i].text,
                    corrected_text=result["corrected_text"],
                    corrections_made=result["corrections"],
                    confidence_score=result.get("confidence", 0.0),
                    needs_review=result.get("needs_review", False),
                    needs_openai=result.get("needs_openai", False)
                )
                processed_entries.append(entry)
            
            # Batch insert
            self.db_manager.batch_insert_processed_entries(processed_entries)
            
            total_entries += len(processed_entries)
            entries_needing_openai += sum(1 for e in processed_entries if e.needs_openai)
        
        return total_entries, entries_needing_openai
    
    def _update_processing_status(self, file_id: int, status: str) -> None:
        """Update transcript processing status."""
        self.db_manager.update_raw_transcript_status(file_id, status)
