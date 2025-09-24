# 🚀 Deployment Guide

## Option 1: Streamlit Cloud (Recommended - Free)

### Step 1: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `Em-Deesha/A-smart-News-and-Insights-Agent-using-langchain`
5. Set the main file path to: `streamlit_app.py`
6. Click "Deploy!"

### Step 2: Configure Environment Variables
In the Streamlit Cloud dashboard:
1. Go to your app settings
2. Add these secrets:
   ```
   NEWS_API_KEY = "your_news_api_key_here"
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

### Step 3: Access Your App
Your app will be available at: `https://your-app-name.streamlit.app`

---

## Option 2: Heroku (Free Tier Available)

### Step 1: Create Heroku Files
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt
```

### Step 2: Deploy to Heroku
```bash
# Install Heroku CLI
# Then run:
heroku create your-app-name
heroku config:set NEWS_API_KEY=your_news_api_key
heroku config:set GEMINI_API_KEY=your_gemini_api_key
git push heroku main
```

---

## Option 3: Railway (Modern Alternative)

### Step 1: Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select your repository

### Step 2: Configure Environment
Add environment variables in Railway dashboard:
- `NEWS_API_KEY`
- `GEMINI_API_KEY`

---

## Option 4: Docker Deployment

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Build and Run
```bash
docker build -t news-agent .
docker run -p 8501:8501 -e NEWS_API_KEY=your_key -e GEMINI_API_KEY=your_key news-agent
```

---

## Option 5: Local Production Server

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 streamlit_app:app
```

### Using Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔧 Environment Variables

Make sure to set these environment variables in your deployment:

```bash
NEWS_API_KEY=your_news_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

## 📊 Monitoring & Analytics

### Streamlit Cloud
- Built-in analytics
- Usage statistics
- Error monitoring

### Custom Monitoring
- Add logging to track API usage
- Monitor rate limits
- Set up alerts for errors

## 🚀 Performance Optimization

1. **Caching**: Implement Redis for caching API responses
2. **Rate Limiting**: Add request throttling
3. **CDN**: Use CloudFlare for static assets
4. **Database**: Add PostgreSQL for user data

## 🔒 Security Considerations

1. **API Keys**: Never commit to repository
2. **HTTPS**: Always use SSL in production
3. **Rate Limiting**: Implement request limits
4. **Input Validation**: Sanitize user inputs
5. **CORS**: Configure cross-origin requests

## 📱 Mobile Deployment

### PWA (Progressive Web App)
Add to your app:
```python
# In app_gemini.py
st.markdown("""
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#FF6B6B">
""", unsafe_allow_html=True)
```

### Mobile App
- Use Streamlit Mobile
- React Native wrapper
- Flutter integration

---

## 🎯 Recommended Deployment Strategy

**For Beginners**: Streamlit Cloud (Free, Easy)
**For Production**: Railway or Heroku
**For Enterprise**: Docker + Kubernetes
**For Learning**: Local server + Nginx

Choose the option that best fits your needs! 🚀
