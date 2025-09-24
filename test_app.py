#!/usr/bin/env python3
"""
Test script for News & Insights Agent
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import transformers
        print("✅ Transformers imported successfully")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import torch
        print("✅ PyTorch imported successfully")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import NEWS_API_KEY, CATEGORIES, SENTIMENT_LABELS
        print("✅ Configuration loaded successfully")
        
        if NEWS_API_KEY == 'your_news_api_key_here':
            print("⚠️  NewsAPI key not configured (using placeholder)")
        else:
            print("✅ NewsAPI key is configured")
        
        print(f"✅ Available categories: {list(CATEGORIES.keys())}")
        print(f"✅ Sentiment labels: {list(SENTIMENT_LABELS.keys())}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_news_fetcher():
    """Test news fetcher (without API key)"""
    print("\n📰 Testing news fetcher...")
    
    try:
        from news_fetcher import NewsFetcher
        fetcher = NewsFetcher()
        categories = fetcher.get_available_categories()
        print("✅ NewsFetcher initialized successfully")
        print(f"✅ Available categories: {list(categories.keys())}")
        return True
        
    except Exception as e:
        print(f"❌ NewsFetcher test failed: {e}")
        return False

def test_text_processor():
    """Test text processor initialization"""
    print("\n🤖 Testing text processor...")
    
    try:
        from text_processor import TextProcessor
        processor = TextProcessor()
        print("✅ TextProcessor initialized successfully")
        
        # Test text cleaning
        test_text = "This is a <b>test</b> text with   extra   spaces."
        cleaned = processor._clean_text(test_text)
        print(f"✅ Text cleaning works: '{cleaned}'")
        
        return True
        
    except Exception as e:
        print(f"❌ TextProcessor test failed: {e}")
        return False

def test_news_agent():
    """Test main news agent"""
    print("\n🎯 Testing news agent...")
    
    try:
        from news_agent import NewsAgent
        agent = NewsAgent()
        categories = agent.get_available_categories()
        print("✅ NewsAgent initialized successfully")
        print(f"✅ Available categories: {list(categories.keys())}")
        return True
        
    except Exception as e:
        print(f"❌ NewsAgent test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing News & Insights Agent")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    tests = [
        test_imports,
        test_config,
        test_news_fetcher,
        test_text_processor,
        test_news_agent
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        print("\nTo run the application:")
        print("  streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
