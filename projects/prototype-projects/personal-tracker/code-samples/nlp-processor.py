"""
NLP Processor for Personal Activity Tracker
Demonstrates NLP processing with NLTK and spaCy.
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re

class JournalProcessor:
    """Processes journal entries using NLP to extract insights."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()
        
        # Mood mapping based on sentiment scores
        self.mood_mapping = {
            (-1.0, -0.5): 'very negative',
            (-0.5, -0.1): 'negative',
            (-0.1, 0.1): 'neutral',
            (0.1, 0.5): 'positive',
            (0.5, 1.0): 'very positive'
        }
        
        # Activity patterns
        self.activity_patterns = {
            'exercise': r'(ran|run|walk|walked|gym|workout|exercise|yoga|swimming|biking)',
            'work': r'(meeting|work|project|study|read|write|code|program)',
            'social': r'(met|meet|talk|chat|party|dinner|lunch|coffee|friend|date)',
            'health': r'(doctor|dentist|therapy|meditation|sleep|rest)',
            'entertainment': r'(watch|play|game|movie|show|music|concert|book)',
            'chores': r'(clean|laundry|cook|shop|grocery|errands)',
        }
        
        # Metric patterns with named groups
        self.metric_patterns = {
            'distance': r'(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>km|mile|miles|m|kilometer|kilometers)',
            'money': r'\$(?P<value>\d+(?:\.\d+)?)',
            'time': r'(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>hour|hours|hr|hrs|minute|minutes|min|mins)',
        }

    def process_entry(self, text):
        """Process a journal entry and extract meaningful information"""
        
        # Basic text cleaning
        text = text.lower().strip()
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        # Sentiment analysis
        sentiment_scores = self.sia.polarity_scores(text)
        sentiment = sentiment_scores['compound']
        
        # Determine mood
        mood = self._get_mood(sentiment)
        
        # Extract topics
        topics = self._extract_topics(words)
        
        # Extract entities (people, places)
        entities = self._extract_entities(text)
        
        # Extract activities
        activities = self._extract_activities(text)
        
        # Extract metrics
        metrics = self._extract_metrics(text)
        
        return {
            'sentiment': sentiment,
            'mood': mood,
            'topics': topics,
            'entities': entities,
            'activities': activities,
            'metrics': metrics
        }
        
    def _get_mood(self, sentiment):
        """Map sentiment score to mood"""
        for (low, high), mood in self.mood_mapping.items():
            if low <= sentiment <= high:
                return mood
        return 'neutral'
        
    def _extract_topics(self, words):
        """Extract main topics from words"""
        # Remove stopwords and get word frequencies
        words = [w for w in words if w not in self.stop_words and w.isalnum()]
        freq_dist = nltk.FreqDist(words)
        
        # Get top 5 most common words as topics
        return [word for word, freq in freq_dist.most_common(5)]
    
    def _extract_entities(self, text):
        """Extract named entities using spaCy"""
        # Note: This is a simplified version
        # In production, would use spaCy NER
        entities = {
            'persons': [],
            'locations': [],
            'organizations': []
        }
        # Implementation would use spaCy here
        return entities
    
    def _extract_activities(self, text):
        """Extract activities based on patterns"""
        activities = []
        for activity_type, pattern in self.activity_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                activities.append(activity_type)
        return activities
    
    def _extract_metrics(self, text):
        """Extract numerical metrics"""
        metrics = {}
        for metric_type, pattern in self.metric_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            values = []
            for match in matches:
                value = float(match.group('value'))
                unit = match.group('unit') if 'unit' in match.groupdict() else None
                values.append({'value': value, 'unit': unit})
            if values:
                metrics[metric_type] = values
        return metrics
