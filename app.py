import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import news_api
import nlp_utils
import summary

st.set_page_config(
    page_title="News Sentiment Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📰 Real-Time News Sentiment Dashboard")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("📊 Analysis Settings")
topic = st.sidebar.text_input("Enter topic/keyword", value="Bitcoin", help="e.g., Nifty 50, Bitcoin, India elections")
num_articles = st.sidebar.slider("Number of articles", 10, 100, 30)
use_llm = st.sidebar.checkbox("Use AI Summary (requires OPENAI_API_KEY in secrets)", value=False)

if st.sidebar.button("🚀 Analyze Sentiment", type="primary"):
    with st.spinner("Fetching news articles..."):
        articles = news_api.fetch_news(topic, num_articles)
    
    if articles:
        st.success(f"✅ Found {len(articles)} articles. Analyzing sentiment...")
        
        with st.spinner("Running sentiment analysis & NLP..."):
            # Analyze sentiment
            sentiment_results = nlp_utils.analyze_sentiment(articles)
            df = pd.DataFrame(sentiment_results)
            
            # Generate summary
            summary_text = summary.generate_summary(articles, df, use_llm)
        
        # Main dashboard
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("📈 Sentiment Distribution")
            sentiment_counts = df['sentiment'].value_counts()
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Sentiment Distribution",
                color_discrete_map={'positive': '#00D084', 'negative': '#FF6B6B', 'neutral': '#A4B0BE'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.subheader("📊 Sentiment Over Time")
            df['published_at'] = pd.to_datetime(df['published_at'])
            df_sorted = df.sort_values('published_at')
            fig_line = px.line(
                df_sorted, x='published_at', y='compound_score',
                color='sentiment',
                title="Average Sentiment Score Over Time",
                color_discrete_map={'positive': '#00D084', 'negative': '#FF6B6B', 'neutral': '#A4B0BE'}
            )
            fig_line.update_traces(line=dict(width=3))
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            st.metric("Overall Sentiment", f"{df['compound_score'].mean():.2f}")
            st.metric("Positive Articles", f"{len(df[df['sentiment']=='positive'])}")
            st.metric("Negative Articles", f"{len(df[df['sentiment']=='negative'])}")
            st.metric("Neutral Articles", f"{len(df[df['sentiment']=='neutral'])}")
        
        # AI Summary
        with st.expander("🤖 AI-Powered Summary", expanded=True):
            st.markdown("### What's happening right now?")
            st.markdown(summary_text)
        
        # Top headlines
        st.header("🗞️ Top Headlines")
        col_pos, col_neg = st.columns(2)
        
        with col_pos:
            st.subheader("✅ Top Positive")
            pos_articles = df[df['sentiment']=='positive'].head(5)
            for _, row in pos_articles.iterrows():
                st.markdown(f"**[{row['source']}]({row['url']})**")
                st.caption(row['title'])
                st.markdown("---")
        
        with col_neg:
            st.subheader("❌ Top Negative")
            neg_articles = df[df['sentiment']=='negative'].head(5)
            for _, row in neg_articles.iterrows():
                st.markdown(f"**[{row['source']}]({row['url']})**")
                st.caption(row['title'])
                st.markdown("---")
        
        # Full article list
        with st.expander("📋 All Articles", expanded=False):
            st.dataframe(
                df[['title', 'sentiment', 'source', 'published_at', 'compound_score']].sort_values('published_at', ascending=False),
                use_container_width=True,
                column_config={
                    "sentiment": st.column_config.SelectboxColumn("Sentiment", options=["positive", "negative", "neutral"]),
                    "compound_score": st.column_config.NumberColumn("Score", format="%.2f")
                }
            )
    else:
        st.warning("⚠️ No articles found. Try a different topic or check API key.")

# Footer
st.markdown("---")
st.markdown("**Phase 1: Real-Time News Sentiment Dashboard** | Built with Streamlit | Zero-cost deployment")
