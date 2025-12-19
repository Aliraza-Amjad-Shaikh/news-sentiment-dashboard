import streamlit as st
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from typing import List, Dict

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(articles: List[Dict]) -> List[Dict]:
    """Analyze sentiment for all articles using VADER + TextBlob ensemble"""
    results = []
    
    for article in articles:
        text = f"{article['title']} {article['description']}"
        
        # VADER sentiment (best for news/social media)
        vader_scores = analyzer.polarity_scores(text)
        compound = vader_scores['compound']
        
        # Classify sentiment
        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        results.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'published_at': article['published_at'],
            'source': article['source'],
            'compound_score': compound,
            'sentiment': sentiment,
            'vader_pos': vader_scores['pos'],
            'vader_neg': vader_scores['neg'],
            'vader_neu': vader_scores['neu']
        })
    
    return results
