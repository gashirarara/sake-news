import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# rss2json.comはRSSをJSONに変換するプロキシサービス（無料・APIキー不要）
RSS2JSON_URL = "https://api.rss2json.com/v1/api.json"
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q=日本酒&hl=ja&gl=JP&ceid=JP:ja"


def fetch_news():
    response = requests.get(
        RSS2JSON_URL,
        params={"rss_url": GOOGLE_NEWS_RSS},
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    articles = []
    for item in data.get("items", [])[:20]:
        articles.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "published": item.get("pubDate", ""),
            "source": item.get("author", ""),
            "summary": item.get("description", ""),
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
