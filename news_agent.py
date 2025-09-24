from news_fetcher import NewsFetcher
from text_processor import TextProcessor
from typing import List, Dict
import time

class NewsAgent:
    """Main agent that orchestrates news fetching, processing, and analysis"""
    
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.text_processor = TextProcessor()
    
    def get_news_insights(self, category: str = 'general', keyword: str = None, 
                         max_articles: int = 10) -> List[Dict]:
        """
        Get news articles with insights (summaries and sentiment analysis)
        
        Args:
            category: News category
            keyword: Search keyword (optional)
            max_articles: Maximum number of articles to process
            
        Returns:
            List of processed articles with insights
        """
        print(f"Fetching news for category: {category}")
        if keyword:
            print(f"Search keyword: {keyword}")
        
        # Fetch news articles
        articles = self.news_fetcher.fetch_news(
            category=category,
            keyword=keyword,
            page_size=max_articles
        )
        
        if not articles:
            print("No articles found")
            return []
        
        print(f"Found {len(articles)} articles. Processing...")
        
        # Process articles with AI insights
        processed_articles = []
        
        for i, article in enumerate(articles):
            try:
                print(f"Processing article {i+1}/{len(articles)}")
                
                # Skip articles without content
                if not article.get('title') and not article.get('description'):
                    continue
                
                # Process article
                processed_article = self.text_processor.process_article(article)
                processed_articles.append(processed_article)
                
                # Small delay to avoid overwhelming the models
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error processing article {i+1}: {e}")
                continue
        
        print(f"Successfully processed {len(processed_articles)} articles")
        return processed_articles
    
    def get_available_categories(self) -> Dict[str, str]:
        """Get available news categories"""
        return self.news_fetcher.get_available_categories()
    
    def filter_articles_by_sentiment(self, articles: List[Dict], 
                                   sentiment_filter: str = None) -> List[Dict]:
        """
        Filter articles by sentiment
        
        Args:
            articles: List of processed articles
            sentiment_filter: Sentiment to filter by (POSITIVE, NEGATIVE, NEUTRAL)
            
        Returns:
            Filtered list of articles
        """
        if not sentiment_filter:
            return articles
        
        return [article for article in articles 
                if article.get('sentiment') == sentiment_filter]
    
    def get_sentiment_stats(self, articles: List[Dict]) -> Dict[str, int]:
        """
        Get sentiment statistics for articles
        
        Args:
            articles: List of processed articles
            
        Returns:
            Dictionary with sentiment counts
        """
        stats = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
        
        for article in articles:
            sentiment = article.get('sentiment', 'NEUTRAL')
            if sentiment in stats:
                stats[sentiment] += 1
        
        return stats
