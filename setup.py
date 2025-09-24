#!/usr/bin/env python3
"""
Setup script for News & Insights Agent
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# News API Configuration\n")
            f.write("NEWS_API_KEY=your_news_api_key_here\n\n")
            f.write("# Hugging Face Configuration (optional)\n")
            f.write("HUGGINGFACE_API_TOKEN=your_huggingface_token_here\n")
        print("✅ .env file created!")
        print("🔑 Please edit .env file and add your NewsAPI key")
    else:
        print("✅ .env file already exists")

def check_api_key():
    """Check if API key is configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('NEWS_API_KEY')
        if api_key and api_key != 'your_news_api_key_here':
            print("✅ NewsAPI key is configured")
            return True
        else:
            print("⚠️  NewsAPI key not configured")
            print("   Please edit .env file and add your API key")
            return False
    except ImportError:
        print("⚠️  python-dotenv not installed yet")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up News & Insights Agent...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return
    
    # Create .env file
    create_env_file()
    
    # Check API key
    api_configured = check_api_key()
    
    print("\n" + "=" * 50)
    if api_configured:
        print("🎉 Setup complete! You can now run:")
        print("   streamlit run app.py")
    else:
        print("🔧 Setup almost complete!")
        print("   1. Get your free API key from https://newsapi.org/")
        print("   2. Edit the .env file and add your API key")
        print("   3. Run: streamlit run app.py")

if __name__ == "__main__":
    main()
