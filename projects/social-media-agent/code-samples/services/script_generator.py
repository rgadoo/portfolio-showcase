#!/usr/bin/env python3
"""
Script Generator
Uses RAG to find relevant book passages and generate 40-second video scripts
"""

import os
from pathlib import Path
from typing import List, Dict
import chromadb
from dotenv import load_dotenv

# LLM imports
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Load environment variables
load_dotenv()

# Paths
CHROMA_DIR = Path("data/chroma_db")


class ScriptGenerator:
    """Generate 40-second video scripts from book content"""
    
    def __init__(self):
        """Initialize the script generator"""
        # Setup ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        
        try:
            self.collection = self.chroma_client.get_collection("book_content")
        except Exception as e:
            raise Exception(f"ChromaDB collection not found. Please run ingestion first. Error: {e}")
        
        # Setup LLM
        if os.getenv("ANTHROPIC_API_KEY") and ANTHROPIC_AVAILABLE:
            self.llm = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.llm_type = "anthropic"
        elif os.getenv("OPENAI_API_KEY") and OPENAI_AVAILABLE:
            self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.llm_type = "openai"
        else:
            raise Exception("No LLM API key found. Please set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env")
    
    def find_relevant_passages(self, topic: str, n_results: int = 3) -> List[Dict]:
        """
        Query ChromaDB for relevant book passages using vector similarity search
        
        Args:
            topic: User's topic/trend query
            n_results: Number of passages to retrieve
            
        Returns:
            List of relevant passages with metadata
        """
        results = self.collection.query(
            query_texts=[topic],
            n_results=n_results
        )
        
        passages = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                passages.append({
                    "text": doc,
                    "source": metadata.get("source", "unknown"),
                    "chunk_id": metadata.get("chunk_id", 0)
                })
        
        return passages
    
    def generate_script(self, topic: str, passages: List[Dict]) -> str:
        """
        Generate a 40-second script from relevant passages using LLM
        
        Args:
            topic: User's topic/trend
            passages: Relevant book passages from RAG search
            
        Returns:
            Generated script text (100-120 words)
        """
        # Combine passages for context
        context = "\n\n---\n\n".join([p["text"] for p in passages])
        
        # Craft the prompt
        prompt = f"""You are a content creator specializing in mindfulness and spirituality.

Based on the following passages from my book and the trending topic, create a compelling 40-second video script (approximately 100-120 words).

TOPIC/TREND: {topic}

RELEVANT BOOK PASSAGES:
{context}

REQUIREMENTS:
1. Script must be exactly 100-120 words (40 seconds when spoken)
2. Start with a strong hook that connects to the trend/topic
3. Include 1-2 key insights from the book passages
4. Use conversational, engaging language suitable for social media
5. End with a thought-provoking question or subtle call-to-action
6. Maintain the spiritual/mindfulness tone
7. Make it relatable to modern audiences

OUTPUT FORMAT:
Just provide the script text, nothing else. No titles, no labels, just the words to be spoken.

SCRIPT:"""

        # Generate with appropriate LLM
        if self.llm_type == "anthropic":
            response = self.llm.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            script = response.content[0].text.strip()
        else:  # OpenAI
            response = self.llm.chat.completions.create(
                model="gpt-4-turbo-preview",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            script = response.choices[0].message.content.strip()
        
        return script
    
    def generate(self, topic: str) -> Dict[str, any]:
        """
        Complete workflow: find passages and generate script
        
        Args:
            topic: User's topic/trend query
            
        Returns:
            Dictionary with script and source passages
        """
        # Step 1: Find relevant passages using RAG
        passages = self.find_relevant_passages(topic, n_results=3)
        
        if not passages:
            raise Exception("No relevant passages found. Make sure book content is ingested.")
        
        # Step 2: Generate script from passages
        script = self.generate_script(topic, passages)
        
        return {
            "script": script,
            "passages": passages,
            "topic": topic
        }
