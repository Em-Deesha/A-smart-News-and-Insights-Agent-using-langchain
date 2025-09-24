from news_fetcher import NewsFetcher
from text_processor_gemini import TextProcessorGemini
from typing import List, Dict
import time

class NewsAgentGemini:
    """Main agent that orchestrates news fetching, processing, and analysis using Gemini API"""
    
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        try:
            self.text_processor = TextProcessorGemini()
        except ValueError as e:
            print(f"Warning: {e}")
            self.text_processor = None
    
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
                
                # Process article with Gemini if available, otherwise use simple processing
                if self.text_processor:
                    processed_article = self.text_processor.process_article(article)
                else:
                    # Fallback to simple processing
                    processed_article = self._simple_process_article(article)
                
                processed_articles.append(processed_article)
                
                # Longer delay to avoid rate limiting (15 requests per minute limit)
                time.sleep(4)
                
            except Exception as e:
                print(f"Error processing article {i+1}: {e}")
                # Add article with simple processing as fallback
                processed_article = self._simple_process_article(article)
                processed_articles.append(processed_article)
                continue
        
        print(f"Successfully processed {len(processed_articles)} articles")
        return processed_articles
    
    def _simple_process_article(self, article: Dict) -> Dict:
        """Simple fallback processing without AI"""
        # Simple sentiment analysis based on keywords
        text = f"{article.get('title', '')} {article.get('description', '')}"
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'win', 'profit', 'growth', 'up', 'rise']
        negative_words = ['bad', 'terrible', 'negative', 'loss', 'fail', 'down', 'fall', 'crisis', 'problem']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = "POSITIVE"
        elif neg_count > pos_count:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL"
        
        # Simple summarization
        description = article.get('description', '')
        summary = description[:150] + "..." if len(description) > 150 else description
        
        article['summary'] = summary
        article['sentiment'] = sentiment
        article['sentiment_confidence'] = 0.7
        
        return article
    
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
