# 📰 Smart News & Insights Agent

An AI-powered news aggregator that fetches the latest news, provides intelligent summaries, and analyzes sentiment using Google's Gemini AI and NewsAPI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red.svg)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-green.svg)
![NewsAPI](https://img.shields.io/badge/NewsAPI-News-orange.svg)

## ✨ Features

- 🔍 **Smart News Fetching**: Get latest news from multiple categories (Tech, Sports, Business, Health)
- 🤖 **AI Summarization**: Automatic article summarization using Google Gemini AI
- 😊 **Sentiment Analysis**: Analyze news sentiment (Positive, Negative, Neutral)
- 🎛️ **Advanced Filtering**: Filter by sentiment, category, or keywords
- 📊 **Visual Analytics**: Interactive charts and statistics
- 🎨 **Modern UI**: Beautiful Streamlit dashboard with responsive design
- ⚡ **Real-time Processing**: Fast AI-powered analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- NewsAPI account (free tier available)
- Google Gemini API key (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Em-Deesha/A-smart-News-and-Insights-Agent-using-langchain.git
   cd A-smart-News-and-Insights-Agent-using-langchain
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**
   
   Create a `.env` file in the project directory:
   ```bash
   # Get your free API key from https://newsapi.org/
   NEWS_API_KEY=your_news_api_key_here
   
   # Get your free API key from https://makersuite.google.com/app/apikey
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app_gemini.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:8501` to see the dashboard!

## 🔧 Configuration

### NewsAPI Setup

1. Visit [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file

**Free tier includes:**
- 100 requests per day
- Headlines and descriptions
- Perfect for personal use

### Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Add it to your `.env` file

**Free tier includes:**
- 15 requests per minute
- 1,500 requests per day
- Fast and reliable AI processing

## 🏗️ Architecture

```
news-agent/
├── app_gemini.py              # Main Streamlit application
├── news_agent_gemini.py       # Main orchestrator with Gemini AI
├── news_fetcher.py            # NewsAPI integration
├── text_processor_gemini.py   # Gemini AI processing (summarization & sentiment)
├── config.py                  # Configuration and constants
├── requirements.txt           # Python dependencies
├── setup.py                  # Setup script
├── test_app.py               # Test script
└── README.md                 # This file
```

## 🤖 AI Models Used

- **Summarization**: Google Gemini 1.5 Flash
- **Sentiment Analysis**: Google Gemini 1.5 Flash
- **News Source**: NewsAPI (free tier)

## 📊 Features in Detail

### News Fetching
- Real-time news from NewsAPI
- Category-based filtering (Technology, Sports, Business, Health, General)
- Keyword search functionality
- Configurable article count (3-10 articles to respect rate limits)

### AI Processing
- **Summarization**: Converts long articles into 2-3 line summaries
- **Sentiment Analysis**: Categorizes news as Positive, Negative, or Neutral
- **Confidence Scores**: Shows how confident the AI is in its analysis
- **Rate Limiting**: Respects API limits with intelligent delays

### Dashboard Features
- **Interactive Filters**: Filter by sentiment, category, or keywords
- **Visual Analytics**: Pie charts showing sentiment distribution
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Fresh news with every fetch
- **Rate Limit Warnings**: Prevents API quota exhaustion

## 🛠️ Customization

### Adding New Categories
Edit `config.py` to add new categories:
```python
CATEGORIES = {
    'technology': 'Technology',
    'sports': 'Sports',
    'business': 'Business',
    'health': 'Health',
    'science': 'Science',  # New category
    'general': 'General'
}
```

### Changing AI Models
The app uses Gemini 1.5 Flash by default. You can modify `text_processor_gemini.py` to use different models or add fallback processing.

## 🐛 Troubleshooting

### Common Issues

1. **"No articles found"**
   - Check your NewsAPI key
   - Verify internet connection
   - Try different categories

2. **Rate limit errors**
   - Reduce number of articles
   - Wait a few minutes before retrying
   - The app includes automatic rate limiting

3. **Memory issues**
   - Use fewer articles
   - Close other applications

### Performance Tips

- Start with 3-5 articles for faster processing
- Use specific keywords for more targeted results
- The app caches API responses for better performance

## 📈 Future Enhancements

- [ ] Add more news sources (Reddit, Twitter)
- [ ] Implement news clustering
- [ ] Add email notifications
- [ ] Export functionality (PDF, CSV)
- [ ] Multi-language support
- [ ] Custom sentiment models
- [ ] Real-time news streaming
- [ ] User authentication
- [ ] Bookmark system
- [ ] Mobile app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [NewsAPI](https://newsapi.org/) for free news data
- [Google Gemini](https://ai.google.dev/) for AI models
- [Streamlit](https://streamlit.io/) for the dashboard framework
- [LangChain](https://langchain.com/) for AI orchestration

## 📞 Support

If you have any questions or need help:

1. Check the [Issues](https://github.com/Em-Deesha/A-smart-News-and-Insights-Agent-using-langchain/issues) page
2. Create a new issue if your problem isn't already reported
3. Join our community discussions

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Em-Deesha/A-smart-News-and-Insights-Agent-using-langchain&type=Date)](https://star-history.com/#Em-Deesha/A-smart-News-and-Insights-Agent-using-langchain&Date)

---

**Made with ❤️ for the AI community**

*Built with Python, Streamlit, and Google Gemini AI*