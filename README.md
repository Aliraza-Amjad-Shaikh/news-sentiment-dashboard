# 📰 Real‑Time News Sentiment Dashboard

A lightweight end‑to‑end **Streamlit** app that fetches recent news for any topic, runs **sentiment analysis**, and shows **interactive insights + an AI summary**, designed to run on the free **Streamlit Community Cloud** tier.[web:9][web:27]

---

## ✨ Features

- 🔍 **Topic search** – enter any keyword (`Bitcoin`, `Nifty 50`, `India elections`, etc.).
- 📰 **Live news fetching** – pulls recent articles via a news API (e.g., [NewsAPI](https://newsapi.org/)) using its free tier limits.[web:2][web:3]
- 😊 **Sentiment analysis** – uses the VADER model to score each article and classify it as positive, neutral, or negative.[web:27][web:29]
- 📊 **Interactive visualizations**
  - Sentiment distribution (pie/bar chart).
  - Sentiment over time (line chart based on publication time).
- 🏷️ **Headline insights**
  - Top positive headlines.
  - Top negative headlines.
  - Full article table with sentiment labels and links.
- 🤖 **AI Summary**
  - If an `OPENAI_API_KEY` is configured, uses a small OpenAI chat model to generate a concise bullet‑point summary.[web:39][web:40]
  - If not, falls back to a rule‑based summary built from sentiment stats and headlines.

Phase 1 focuses on a single Streamlit codebase that is easy to deploy, understand, and extend later (separate backend, React frontend, RAG, auth, etc.).

---

## 🧱 Project Structure

.
├── app.py # Main Streamlit app: UI, charts, and orchestration
├── news_api.py # News fetching logic (NewsAPI + sample fallback)
├── nlp_utils.py # Sentiment analysis / NLP helpers
├── summary.py # AI + rule-based summary generation
├── requirements.txt # Python dependencies
└── .streamlit/
└── secrets.toml # Local secrets (NOT committed to GitHub)


**Responsibilities in short:**

- `app.py` – handles layout, user inputs, calling helper functions, and rendering charts/tables.
- `news_api.py` – talks to the news API (or returns sample data if keys/rate‑limits fail).[web:2][web:6]
- `nlp_utils.py` – computes VADER sentiment scores and assigns labels.[web:27][web:34]
- `summary.py` – produces the “What’s happening right now?” section using OpenAI if available, otherwise a deterministic summary.[web:39][web:41]

---

## 🚀 Getting Started Locally

### 1. Clone the repo

git clone https://github.com/Aliraza-Amjad-Shaikh/news-sentiment-dashboard.git
cd news-sentiment-dashboard


### 2. (Optional) Create a virtual environment

python -m venv .venv

Windows
.venv\Scripts\activate

macOS / Linux
source .venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt


### 4. Configure secrets (local only)

Create the directory:

mkdir -p .streamlit

Create `.streamlit/secrets.toml`:

NEWS_API_KEY = "your_newsapi_key_here"
OPENAI_API_KEY = "sk-your_openai_key_here"


- `NEWS_API_KEY` – required for real live news (e.g., free key from https://newsapi.org/).[web:3][web:7]
- `OPENAI_API_KEY` – optional; enables OpenAI chat‑based summaries, otherwise the app uses a rule‑based summary.[web:39][web:40]

> Important: `.streamlit/secrets.toml` should be in `.gitignore` and **must not** be committed.

### 5. Run the app

streamlit run app.py



Open the URL shown in the terminal (usually `http://localhost:8501`), enter a topic, choose number of articles, optionally enable **Use AI Summary**, and click **Analyze Sentiment**.

---

## ☁️ Deployment on Streamlit Community Cloud

1. Push this repository to GitHub (already done for `Aliraza-Amjad-Shaikh/news-sentiment-dashboard`).  
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.[web:22][web:23]  
3. Click **New app** and configure:
   - **Repository**: `Aliraza-Amjad-Shaikh/news-sentiment-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. In the app’s **Settings → Secrets**, add:

NEWS_API_KEY = "your_newsapi_key_here"
OPENAI_API_KEY = "sk-your_openai_key_here"


5. Click **Deploy**. After the build, you’ll get a public URL like:

https://news-sentiment-dashboard-<your-username>.streamlit.app


Use that link to access and share the live dashboard.

---

## 🔍 How It Works (High‑Level)

1. **User input** (topic, number of articles, AI summary toggle) is handled in `app.py`.
2. `news_api.fetch_news(topic, limit)` calls the news API’s “everything” endpoint with query parameters and time filters; on failure or missing key, it falls back to sample data so the app still runs.[web:2][web:6]
3. `nlp_utils.analyze_sentiment(articles)` uses the VADER lexicon‑based model to compute `compound` scores in \([-1, 1]\) and assign positive/neutral/negative labels per article.[web:27][web:29]
4. The analyzed list is converted to a pandas DataFrame and visualized via Plotly charts and Streamlit widgets.[web:9]
5. `summary.generate_summary(articles, df, use_llm)`:
   - If `use_llm` is enabled and `OPENAI_API_KEY` is present, calls a small OpenAI Chat Completions model to produce a 4‑bullet Markdown summary.[web:39][web:40]
   - Otherwise, constructs a rule‑based summary using sentiment counts and top headlines.

---

## 🛠️ Extending the App

This repo is intentionally modular so you can iterate easily:

- Add keyword extraction or entity highlighting in `nlp_utils.py`.
- Support additional news providers or social feeds in `news_api.py`.
- Customize the summary prompt for finance, politics, or other domains in `summary.py`.
- Add filters (date range, language, sources) and layout changes in `app.py`.

Feel free to fork and extend for learning, internal tools, or prototypes.
