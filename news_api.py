import streamlit as st
import requests
from typing import List, Dict
from datetime import datetime, timedelta

def fetch_news(topic: str, limit: int = 30) -> List[Dict]:
    """
    Fetch recent news articles using NewsAPI (free tier).
    Fallback to sample data if API key missing or fails.
    """
    # Get API key SAFELY - only when Streamlit is running
    try:
        NEWS_API_KEY = st.secrets.get("NEWS_API_KEY")
    except:
        NEWS_API_KEY = None
    
    if not NEWS_API_KEY:
        st.warning("⚠️ No NEWS_API_KEY found. Using sample data.")
        return _get_sample_data(topic, limit)
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': topic,
            'apiKey': NEWS_API_KEY,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': min(limit, 100),
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200 and data['articles']:
            articles = []
            for article in data['articles'][:limit]:
                if article.get('title') and article.get('description'):
                    articles.append({
                        'title': article['title'],
                        'description': article['description'] or '',
                        'url': article['url'],
                        'published_at': article['publishedAt'],
                        'source': article['source']['name']
                    })
            return articles
        else:
            st.warning(f"API returned no articles: {data.get('message', 'Unknown error')}")
            return _get_sample_data(topic, limit)
            
    except Exception as e:
        st.error(f"News API error: {str(e)}")
        return _get_sample_data(topic, limit)

def _get_sample_data(topic: str, limit: int) -> List[Dict]:
    """Realistic sample data for demo"""
    samples = [
        {
            'title': f'{topic} surges 5% amid positive market sentiment',
            'description': f'Latest developments in {topic} show strong bullish trend with major investors entering.',
            'url': 'https://example.com/positive',
            'published_at': '2025-12-19T10:30:00Z',
            'source': 'MarketWatch'
        },
        {
            'title': f'{topic} faces regulatory scrutiny, drops 3%',
            'description': f'Government announces new regulations impacting {topic} operations.',
            'url': 'https://example.com/negative',
            'published_at': '2025-12-19T09:45:00Z',
            'source': 'Reuters'
        },
        {
            'title': f'{topic} partnership rumors boost investor confidence',
            'description': f'Unconfirmed reports of major partnership send {topic} higher in pre-market.',
            'url': 'https://example.com/positive2',
            'published_at': '2025-12-19T08:20:00Z',
            'source': 'Bloomberg'
        },
        {
            'title': f'{topic} technical analysis: Neutral outlook',
            'description': f'Analysts maintain neutral stance on {topic} amid mixed signals.',
            'url': 'https://example.com/neutral',
            'published_at': '2025-12-19T07:15:00Z',
            'source': 'CNBC'
        }
    ]
    return samples[:limit]
