from transformers import pipeline
import torch
from typing import Dict, List
import re

class TextProcessor:
    """Handles text summarization and sentiment analysis using Hugging Face models"""
    
    def __init__(self):
        # Initialize summarization pipeline
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1
        )
    
    def summarize_text(self, text: str, max_length: int = 50, min_length: int = 10) -> str:
        """
        Summarize text using BART model
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Summarized text
        """
        try:
            # Clean and truncate text if too long
            cleaned_text = self._clean_text(text)
            if len(cleaned_text) > 1000:
                cleaned_text = cleaned_text[:1000]
            
            if len(cleaned_text) < 50:
                return cleaned_text
            
            # Generate summary
            result = self.summarizer(
                cleaned_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            return result[0]['summary_text']
            
        except Exception as e:
            print(f"Summarization error: {e}")
            return text[:100] + "..." if len(text) > 100 else text
    
    def analyze_sentiment(self, text: str) -> Dict[str, str]:
        """
        Analyze sentiment of text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment label and confidence
        """
        try:
            # Clean text
            cleaned_text = self._clean_text(text)
            
            if len(cleaned_text) < 10:
                return {"label": "NEUTRAL", "confidence": 0.5}
            
            # Analyze sentiment
            result = self.sentiment_analyzer(cleaned_text)
            
            # Map sentiment labels
            sentiment_mapping = {
                'LABEL_0': 'NEGATIVE',
                'LABEL_1': 'NEUTRAL', 
                'LABEL_2': 'POSITIVE'
            }
            
            label = sentiment_mapping.get(result[0]['label'], 'NEUTRAL')
            confidence = result[0]['score']
            
            return {
                "label": label,
                "confidence": round(confidence, 2)
            }
            
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {"label": "NEUTRAL", "confidence": 0.5}
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:-]', '', text)
        
        return text.strip()
    
    def process_article(self, article: Dict) -> Dict:
        """
        Process a single article with summarization and sentiment analysis
        
        Args:
            article: Article dictionary with title, description, content
            
        Returns:
            Enhanced article dictionary with summary and sentiment
        """
        # Combine title and description for analysis
        full_text = f"{article.get('title', '')} {article.get('description', '')}"
        
        # Generate summary
        summary = self.summarize_text(full_text)
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(full_text)
        
        # Add processed data to article
        article['summary'] = summary
        article['sentiment'] = sentiment['label']
        article['sentiment_confidence'] = sentiment['confidence']
        
        return article
