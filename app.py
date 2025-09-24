import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from news_agent import NewsAgent
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
        st.session_state.news_agent = NewsAgent()
    
    if 'processed_articles' not in st.session_state:
        st.session_state.processed_articles = []
    
    # Header
    st.title("📰 News & Insights Agent")
    st.markdown("Get the latest news with AI-powered summaries and sentiment analysis")
    
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
        
        # Number of articles
        max_articles = st.slider("Number of Articles", 5, 50, 20)
        
        # Fetch news button
        if st.button("🔍 Fetch News", type="primary"):
            with st.spinner("Fetching and processing news..."):
                st.session_state.processed_articles = st.session_state.news_agent.get_news_insights(
                    category=selected_category,
                    keyword=search_keyword if search_keyword else None,
                    max_articles=max_articles
                )
        
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
        - 🤖 Get AI-generated summaries of articles
        - 😊 Analyze sentiment (positive, negative, neutral)
        - 🔍 Search by keywords or categories
        - 📊 View sentiment statistics and trends
        
        **To get started:**
        1. Select a news category from the sidebar
        2. Optionally enter a search keyword
        3. Click "Fetch News" to get started!
        
        **Note:** Make sure to set your NewsAPI key in the environment variables for the app to work.
        """)
        
        # API key setup instructions
        with st.expander("🔑 API Key Setup Instructions"):
            st.markdown("""
            **To use this application, you need a free NewsAPI key:**
            
            1. Go to [NewsAPI.org](https://newsapi.org/)
            2. Sign up for a free account
            3. Get your API key from the dashboard
            4. Create a `.env` file in the project directory
            5. Add your API key: `NEWS_API_KEY=your_api_key_here`
            
            **Free tier limits:**
            - 100 requests per day
            - Headlines only (no full articles)
            - Perfect for personal use and testing
            """)

if __name__ == "__main__":
    main()
