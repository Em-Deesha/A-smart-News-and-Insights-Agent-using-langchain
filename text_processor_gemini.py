import google.generativeai as genai
from typing import Dict
import re
from config import GEMINI_API_KEY

class TextProcessorGemini:
    """Handles text summarization and sentiment analysis using Gemini API"""
    
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        Summarize text using Gemini API
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summarized text
        """
        try:
            # Clean and truncate text if too long
            cleaned_text = self._clean_text(text)
            if len(cleaned_text) > 2000:  # Gemini has token limits
                cleaned_text = cleaned_text[:2000]
            
            if len(cleaned_text) < 50:
                return cleaned_text
            
            prompt = f"""
            Please provide a concise summary of the following news article in 2-3 sentences. Make sure the summary is complete and not cut off:
            
            {cleaned_text}
            
            Summary:
            """
            
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            
            # Ensure summary is complete and not cut off
            if len(summary) > max_length:
                # Find the last complete sentence
                sentences = summary.split('. ')
                if len(sentences) > 1:
                    # Keep all complete sentences
                    complete_sentences = []
                    current_length = 0
                    for sentence in sentences:
                        if current_length + len(sentence) + 2 <= max_length:  # +2 for '. '
                            complete_sentences.append(sentence)
                            current_length += len(sentence) + 2
                        else:
                            break
                    summary = '. '.join(complete_sentences) + '.'
                else:
                    summary = summary[:max_length-3] + "..."
            
            return summary
            
        except Exception as e:
            print(f"Summarization error: {e}")
            return text[:100] + "..." if len(text) > 100 else text
    
    def analyze_sentiment(self, text: str) -> Dict[str, str]:
        """
        Analyze sentiment of text using Gemini API
        
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
            
            prompt = f"""
            Analyze the sentiment of this news article. Consider the overall tone, implications, and impact.
            - POSITIVE: Good news, achievements, progress, success, benefits
            - NEGATIVE: Bad news, problems, failures, crises, losses, conflicts
            - NEUTRAL: Factual reporting, announcements, updates without clear positive/negative tone
            
            Article: {cleaned_text}
            
            Respond with only one word: POSITIVE, NEGATIVE, or NEUTRAL
            """
            
            response = self.model.generate_content(prompt)
            sentiment = response.text.strip().upper()
            
            # Validate response
            if sentiment not in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
                sentiment = "NEUTRAL"
            
            # Gemini doesn't provide confidence scores, so we'll use a default
            confidence = 0.8 if sentiment in ["POSITIVE", "NEGATIVE"] else 0.6
            
            return {
                "label": sentiment,
                "confidence": confidence
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
