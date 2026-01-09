"""
OpenAI API client for transcript correction.

This module handles sending SRT entries to OpenAI for correction and processing the responses.
"""
import json
import os
import sys
import time
from typing import Dict, List, Optional, Any, Tuple

from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE
from services.srt_parser import SRTEntry


# Correction prompt template
CORRECTION_PROMPT = """
You are an expert in correcting transcripts of spiritual/philosophical lectures that mix English, Sanskrit, and Hindi terms.

IMPORTANT: ONLY correct Sanskrit and Hindi terms that have been mistranscribed. DO NOT change English words unless they are clearly mistranscribed Sanskrit/Hindi terms.

Common correction patterns:
- "christian" → "Krishna"
- "thomas" → "tamas" (when discussing gunas)
- "common" → "karma" (only when clearly referring to the spiritual concept)
- "bagavad" → "Bhagavad"
- "geeta" → "Gita"
- "arjun" → "Arjuna"
- "home" → "Om" (only when referring to the sacred sound)

Rules:
1. ONLY correct obvious mispronunciations of Sanskrit/Hindi spiritual terms
2. DO NOT change English words that are correctly used in English context
3. Preserve original meaning and context
4. Maintain exact timestamp format
5. Preserve punctuation and capitalization patterns
6. If unsure whether a word is English or Sanskrit, leave it as is

Input SRT entries:
{srt_entries}

Return JSON array with this exact structure:
[
  {{
    "timestamp": "HH:MM:SS,mmm --> HH:MM:SS,mmm",
    "original_text": "original text here",
    "corrected_text": "corrected text here",
    "corrections_made": [
      {{"original": "word", "corrected": "word", "confidence": 0.95}}
    ],
    "needs_review": boolean
  }}
]
"""


class OpenAIClient:
    """Client for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
    
    @staticmethod
    def format_entries_for_prompt(entries: List[SRTEntry]) -> str:
        """
        Format SRT entries for inclusion in the prompt.
        
        Args:
            entries: List of SRTEntry objects
            
        Returns:
            Formatted string for prompt
        """
        formatted = []
        for entry in entries:
            formatted.append(
                f"{entry.index}\n"
                f"{entry.start_time} --> {entry.end_time}\n"
                f"{entry.text}\n"
            )
        return "\n".join(formatted)
    
    def correct_transcript_batch(self, entries: List[SRTEntry], retry_count: int = 3) -> List[Dict[str, Any]]:
        """
        Send batch of SRT entries to OpenAI for correction.
        
        Args:
            entries: List of SRTEntry objects to correct
            retry_count: Number of retry attempts
            
        Returns:
            List of correction dictionaries
        """
        formatted_entries = self.format_entries_for_prompt(entries)
        prompt = CORRECTION_PROMPT.format(srt_entries=formatted_entries)
        
        for attempt in range(retry_count):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a transcript correction expert."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                
                # Parse response
                content = response.choices[0].message.content
                corrections = json.loads(content)
                
                return corrections
                
            except json.JSONDecodeError as e:
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise ValueError(f"Failed to parse OpenAI response: {e}")
            except Exception as e:
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception(f"OpenAI API error: {e}")
        
        raise Exception("Failed to get valid response from OpenAI after retries")
    
    @staticmethod
    def estimate_api_cost(text_length: int) -> float:
        """
        Estimate OpenAI API cost based on text length.
        
        Args:
            text_length: Length of text in characters
            
        Returns:
            Estimated cost in USD
        """
        # Simplified cost estimation
        # Actual pricing varies by model
        tokens_per_char = 0.25  # Approximate
        tokens = text_length * tokens_per_char
        
        # Example pricing (adjust based on actual model)
        input_cost_per_1k = 0.0015
        output_cost_per_1k = 0.002
        
        input_cost = (tokens * 0.7 / 1000) * input_cost_per_1k
        output_cost = (tokens * 0.3 / 1000) * output_cost_per_1k
        
        return input_cost + output_cost
    
    @staticmethod
    def map_corrections_to_entries(original_entries: List[SRTEntry], 
                                  corrections: List[Dict]) -> List[Dict[str, Any]]:
        """
        Map OpenAI corrections back to original entries.
        
        Args:
            original_entries: Original SRTEntry objects
            corrections: Correction dictionaries from OpenAI
            
        Returns:
            List of mapped correction dictionaries
        """
        mapped = []
        for i, entry in enumerate(original_entries):
            if i < len(corrections):
                correction = corrections[i]
                mapped.append({
                    "entry": entry,
                    "corrected_text": correction.get("corrected_text", entry.text),
                    "corrections": correction.get("corrections_made", []),
                    "needs_review": correction.get("needs_review", False)
                })
            else:
                # No correction provided, use original
                mapped.append({
                    "entry": entry,
                    "corrected_text": entry.text,
                    "corrections": [],
                    "needs_review": False
                })
        return mapped
