
from flask import Flask, request, jsonify
from naver_news_crawler import naver_news_crawl
from google_news_crawler import google_news_crawl
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    naver_results = naver_news_crawl(query)
    for item in naver_results:
        item["sourceType"] = "네이버"

    google_results = google_news_crawl(query)
    for item in google_results:
        item["sourceType"] = "구글"
    combined = naver_results + google_results
    return jsonify(combined)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
