import streamlit as st
from typing import List, Dict
from openai import OpenAI


def generate_summary(articles: List[Dict], df, use_llm: bool) -> str:
    """
    Entry point used by app.py.

    - If use_llm is True and OPENAI_API_KEY exists -> use GPT for summary.
    - Otherwise -> use rule-based summary (no cost).
    """
    has_key = "OPENAI_API_KEY" in st.secrets

    if use_llm and has_key:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            return _generate_llm_summary(client, df)
        except Exception as e:
            # Any error from OpenAI -> fall back to rule-based summary
            st.error(f"LLM summary failed: {e}")
            return _generate_rule_based_summary(df)

    # If checkbox is off or key missing
    if use_llm and not has_key:
        st.info("OPENAI_API_KEY not found in secrets. Using rule-based summary.")

    return _generate_rule_based_summary(df)


def _generate_llm_summary(client: OpenAI, df) -> str:
    """
    Use OpenAI Chat Completions to generate a short summary.

    IMPORTANT: uses df, which already has 'sentiment' column.
    This avoids KeyError: 'sentiment' on raw articles.
    """
    # Take up to 10 most recent headlines with their sentiment label
    df_sorted = df.sort_values("published_at", ascending=False).head(10)

    headline_lines = [
        f"- {row['title']} ({row['sentiment']})"
        for _, row in df_sorted.iterrows()
    ]

    sentiment_counts = df["sentiment"].value_counts().to_dict()

    prompt = f"""
You are an analyst summarizing recent news coverage about a topic.

Sentiment distribution (article counts) = {sentiment_counts}

Example headlines with sentiment:
{chr(10).join(headline_lines)}

Write EXACTLY 4 concise Markdown bullet points:
1. Overall sentiment trend (bullish / bearish / mixed) and how strong it is.
2. Main themes or storylines appearing in these headlines.
3. Strong positive developments (if any).
4. Strong negative signals or concerns (if any).

Be objective and avoid speculation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",          # cheap, fast model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def _generate_rule_based_summary(df) -> str:
    """
    Cheap fallback summary that does not call any LLM.
    Operates only on df (which contains sentiment and titles).
    """
    if df.empty:
        return "• No articles were found for this topic in the selected time window."

    sentiment_counts = df["sentiment"].value_counts()
    total = len(df) or 1

    pos = sentiment_counts.get("positive", 0)
    neg = sentiment_counts.get("negative", 0)
    neu = sentiment_counts.get("neutral", 0)

    pos_pct = pos / total * 100
    neg_pct = neg / total * 100

    if pos_pct > neg_pct + 10:
        trend = "bullish (more positive than negative coverage)"
    elif neg_pct > pos_pct + 10:
        trend = "bearish (more negative than positive coverage)"
    else:
        trend = "mixed (positive and negative are fairly balanced)"

    top_pos = df[df["sentiment"] == "positive"].sort_values(
        "compound_score", ascending=False
    ).head(2)["title"].tolist()

    top_neg = df[df["sentiment"] == "negative"].sort_values(
        "compound_score"
    ).head(2)["title"].tolist()

    bullets = []

    bullets.append(
        f"• Overall sentiment: {pos} positive, {neg} negative, {neu} neutral articles. "
        f"The tone looks **{trend}**."
    )

    bullets.append(
        "• Main themes: Headlines cluster around a few recurring stories for this topic "
        "such as recent events, reactions, and commentary."
    )

    if top_pos:
        bullets.append(
            "• Strong positive signals:\n"
            + "\n".join(f"  - {t[:90]}..." for t in top_pos)
        )
    else:
        bullets.append("• Strong positive signals: No clearly positive headlines dominate right now.")

    if top_neg:
        bullets.append(
            "• Strong negative signals:\n"
            + "\n".join(f"  - {t[:90]}..." for t in top_neg)
        )
    else:
        bullets.append("• Strong negative signals: No clearly negative headlines dominate right now.")

    return "\n".join(bullets)
