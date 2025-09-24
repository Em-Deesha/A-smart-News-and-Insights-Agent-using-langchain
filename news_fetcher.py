import requests
import json
from typing import List, Dict, Optional
from config import NEWS_API_KEY, NEWS_API_BASE_URL, CATEGORIES

class NewsFetcher:
    """Fetches news articles from NewsAPI"""
    
    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.base_url = NEWS_API_BASE_URL
        
    def fetch_news(self, category: str = 'general', keyword: str = None, 
                   country: str = 'us', page_size: int = 20) -> List[Dict]:
        """
        Fetch news articles from NewsAPI
        
        Args:
            category: News category (technology, sports, business, health, general)
            keyword: Search keyword (optional)
            country: Country code (default: 'us')
            page_size: Number of articles to fetch (max 100)
            
        Returns:
            List of news articles
        """
        try:
            if keyword:
                # Search by keyword
                url = f"{self.base_url}/everything"
                params = {
                    'q': keyword,
                    'apiKey': self.api_key,
                    'pageSize': page_size,
                    'language': 'en',
                    'sortBy': 'publishedAt'
                }
            else:
                # Search by category
                url = f"{self.base_url}/top-headlines"
                params = {
                    'category': category,
                    'apiKey': self.api_key,
                    'pageSize': page_size,
                    'country': country
                }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                return data['articles']
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
    
    def get_available_categories(self) -> Dict[str, str]:
        """Get available news categories"""
        return CATEGORIES
