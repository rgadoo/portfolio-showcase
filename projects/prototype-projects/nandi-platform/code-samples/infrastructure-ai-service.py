"""
Infrastructure Layer: AI Service
Demonstrates external service integration in Domain-Driven Design.
"""

import os
import openai
from typing import List, Dict, Any, Optional
from modules.karma_cafe.config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE

class AIService:
    """Service for interacting with OpenAI API using modern patterns."""
    
    def __init__(self) -> None:
        """Initialize the AI service with OpenAI API key."""
        if not OPENAI_API_KEY:
            logger.warning("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        openai.api_key = OPENAI_API_KEY
    
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response using OpenAI API.
        
        Args:
            messages: List of message dictionaries with role and content.
            
        Returns:
            Generated response text or error message.
        """
        if not OPENAI_API_KEY:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
        
        try:
            logger.info(f"Sending request to OpenAI API with model {OPENAI_MODEL}")
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"
