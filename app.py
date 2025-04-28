from flask import Flask, request, jsonify
from textblob import TextBlob
import praw

app = Flask(__name__)

# Set up Reddit API using PRAW (replace with your keys)
reddit = praw.Reddit(
    client_id='qxI6_F89joqaLEsOsNofVA',
    client_secret='tZoe9HTVzN27qWlstfn4y02IWZEc7A',
    user_agent='sentimentApp by /u/rishabh1263'
)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

@app.route('/')
def home():
    return jsonify({"message": "Reddit Sentiment Analysis API"}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get("url")

    if "comments" in url:
        comment = reddit.comment(url=url)
        sentiment = analyze_sentiment(comment.body)
        return jsonify({
            "text": comment.body,
            "sentiment": sentiment
        }), 200

    elif "reddit.com/r/" in url:
        submission = reddit.submission(url=url)
        sentiment = analyze_sentiment(submission.title + " " + submission.selftext)
        return jsonify({
            "title": submission.title,
            "content": submission.selftext,
            "sentiment": sentiment
        }), 200
    else:
        return jsonify({"error": "Invalid Reddit URL"}), 400
import os 

if __name__ == '__main__':
    port  = int(os.environ.get('PORT', 5000))
    app.run(host= '0.0.0.0', port=port)
