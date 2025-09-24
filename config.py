import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# News API Configuration
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_news_api_key_here')
NEWS_API_BASE_URL = 'https://newsapi.org/v2'

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Available categories
CATEGORIES = {
    'technology': 'Technology',
    'sports': 'Sports', 
    'business': 'Business',
    'health': 'Health',
    'general': 'General'
}

# Sentiment labels
SENTIMENT_LABELS = {
    'POSITIVE': '😊',
    'NEGATIVE': '😞', 
    'NEUTRAL': '😐'
}
