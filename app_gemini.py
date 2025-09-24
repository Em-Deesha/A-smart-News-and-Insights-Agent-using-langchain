import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from news_agent_gemini import NewsAgentGemini
from config import SENTIMENT_LABELS
import time

# Page configuration
st.set_page_config(
    page_title="News & Insights Agent",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .news-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #6c757d;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #007bff;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'news_agent' not in st.session_state:
        try:
            st.session_state.news_agent = NewsAgentGemini()
        except Exception as e:
            st.error(f"Failed to initialize News Agent: {e}")
            st.session_state.news_agent = None
    
    if 'processed_articles' not in st.session_state:
        st.session_state.processed_articles = []
    
    # Header
    st.title("📰 News & Insights Agent")
    st.markdown("Get the latest news with AI-powered summaries and sentiment analysis using Gemini")
    
    # Check if agent is available
    if st.session_state.news_agent is None:
        st.error("❌ News Agent not available. Please check your API keys in the .env file.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Search Options")
        
        # Category selection
        categories = st.session_state.news_agent.get_available_categories()
        selected_category = st.selectbox(
            "Select Category",
            options=list(categories.keys()),
            format_func=lambda x: categories[x]
        )
        
        # Keyword search
        search_keyword = st.text_input("Search Keyword (optional)", placeholder="e.g., AI, climate change")
        
        # Number of articles (limited to avoid rate limits)
        max_articles = st.slider("Number of Articles", 3, 10, 5)
        
        # Rate limit warning
        st.info("⚠️ **Rate Limit Notice**: Gemini free tier allows 15 requests per minute. Processing 5 articles = 10 requests (5 summaries + 5 sentiment analyses).")
        
        # Fetch news button
        if st.button("🔍 Fetch News", type="primary"):
            with st.spinner("Fetching and processing news with Gemini AI..."):
                try:
                    st.session_state.processed_articles = st.session_state.news_agent.get_news_insights(
                        category=selected_category,
                        keyword=search_keyword if search_keyword else None,
                        max_articles=max_articles
                    )
                    st.success(f"✅ Successfully processed {len(st.session_state.processed_articles)} articles!")
                except Exception as e:
                    st.error(f"Error fetching news: {e}")
        
        # Filters
        st.header("🎛️ Filters")
        
        # Sentiment filter
        sentiment_options = ["All", "POSITIVE", "NEGATIVE", "NEUTRAL"]
        selected_sentiment = st.selectbox("Filter by Sentiment", sentiment_options)
        
        # Apply filters
        filtered_articles = st.session_state.processed_articles.copy()
        if selected_sentiment != "All":
            filtered_articles = st.session_state.news_agent.filter_articles_by_sentiment(
                filtered_articles, selected_sentiment
            )
    
    # Main content area
    if st.session_state.processed_articles:
        # Statistics
        st.header("📊 News Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Articles", len(st.session_state.processed_articles))
        
        with col2:
            positive_count = sum(1 for article in st.session_state.processed_articles 
                               if article.get('sentiment') == 'POSITIVE')
            st.metric("Positive", positive_count)
        
        with col3:
            negative_count = sum(1 for article in st.session_state.processed_articles 
                               if article.get('sentiment') == 'NEGATIVE')
            st.metric("Negative", negative_count)
        
        with col4:
            neutral_count = sum(1 for article in st.session_state.processed_articles 
                              if article.get('sentiment') == 'NEUTRAL')
            st.metric("Neutral", neutral_count)
        
        # Sentiment distribution chart
        if len(st.session_state.processed_articles) > 0:
            sentiment_stats = st.session_state.news_agent.get_sentiment_stats(st.session_state.processed_articles)
            
            fig = px.pie(
                values=list(sentiment_stats.values()),
                names=list(sentiment_stats.keys()),
                title="Sentiment Distribution",
                color_discrete_map={
                    'POSITIVE': '#28a745',
                    'NEGATIVE': '#dc3545',
                    'NEUTRAL': '#6c757d'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # News articles
        st.header(f"📰 News Articles ({len(filtered_articles)} articles)")
        
        if filtered_articles:
            for i, article in enumerate(filtered_articles):
                with st.container():
                    st.markdown(f"""
                    <div class="news-card">
                        <h3>{article.get('title', 'No title')}</h3>
                        <p><strong>Source:</strong> {article.get('source', {}).get('name', 'Unknown')} | 
                        <strong>Published:</strong> {article.get('publishedAt', 'Unknown date')[:10]}</p>
                        <p><strong>Summary:</strong> {article.get('summary', 'No summary available')}</p>
                        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0;">
                            <strong>📝 AI Summary:</strong><br>
                            {article.get('summary', 'No summary available')}
                        </div>
                        <p><strong>Sentiment:</strong> 
                        <span class="sentiment-{article.get('sentiment', 'neutral').lower()}">
                            {SENTIMENT_LABELS.get(article.get('sentiment', 'NEUTRAL'), '😐')} 
                            {article.get('sentiment', 'NEUTRAL')} 
                            ({article.get('sentiment_confidence', 0):.2f})
                        </span></p>
                        <p><strong>Original Description:</strong> {article.get('description', 'No description')[:200]}...</p>
                        <p><a href="{article.get('url', '#')}" target="_blank">Read Full Article →</a></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
        else:
            st.warning("No articles match the selected filters.")
    
    else:
        # Welcome message
        st.markdown("""
        ## Welcome to News & Insights Agent! 🎉
        
        This AI-powered news aggregator helps you:
        - 📰 Fetch the latest news from multiple categories
        - 🤖 Get AI-generated summaries using Gemini
        - 😊 Analyze sentiment (positive, negative, neutral)
        - 🔍 Search by keywords or categories
        - 📊 View sentiment statistics and trends
        
        **To get started:**
        1. Make sure you have both NewsAPI and Gemini API keys in your .env file
        2. Select a news category from the sidebar
        3. Optionally enter a search keyword
        4. Click "Fetch News" to get started!
        """)
        
        # API key setup instructions
        with st.expander("🔑 API Key Setup Instructions"):
            st.markdown("""
            **You need two API keys:**
            
            **1. NewsAPI (Free):**
            - Go to [NewsAPI.org](https://newsapi.org/)
            - Sign up for a free account
            - Get your API key from the dashboard
            
            **2. Gemini API (Free):**
            - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
            - Sign in with your Google account
            - Create a new API key
            
            **Add both keys to your .env file:**
            ```
            NEWS_API_KEY=your_news_api_key_here
            GEMINI_API_KEY=your_gemini_api_key_here
            ```
            
            **Free tier limits:**
            - NewsAPI: 100 requests per day
            - Gemini: 15 requests per minute, 1,500 requests per day
            """)

if __name__ == "__main__":
    main()
