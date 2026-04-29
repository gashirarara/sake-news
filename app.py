import feedparser
from flask import Flask, jsonify, render_template

app = Flask(__name__)

RSS_URL = "https://news.google.com/rss/search?q=日本酒&hl=ja&gl=JP&ceid=JP:ja"


def fetch_news():
    feed = feedparser.parse(RSS_URL)
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
