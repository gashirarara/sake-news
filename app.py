import feedparser
import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

RSS_URL = "https://news.yahoo.co.jp/rss/search?p=日本酒&ei=UTF-8"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "ja,en;q=0.9",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}


def fetch_news():
    response = requests.get(RSS_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    articles = []
    for entry in feed.entries[:20]:
        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "source": entry.get("source", {}).get("title", ""),
            "summary": entry.get("summary", ""),
        })
    return articles


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/news")
def api_news():
    try:
        articles = fetch_news()
        return jsonify({"articles": articles})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
