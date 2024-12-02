from flask import Flask, render_template_string, jsonify, request
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk

# Download required NLTK datasets
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Sentiment Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }
        th { background-color: #f4f4f4; }
        #word-cloud { max-width: 100%; height: auto; }
    </style>
</head>
<body>
    <h1>Crypto Sentiment Analysis</h1>
    <form id="search-form">
        <input type="text" id="crypto" placeholder="Enter cryptocurrency name" required>
        <button type="submit">Search</button>
    </form>
    <h2>Sentiment Breakdown</h2>
    <p>Positive: <span id="positive"></span>%</p>
    <p>Neutral: <span id="neutral"></span>%</p>
    <p>Negative: <span id="negative"></span>%</p>
    
    <h2>Frequent Keywords</h2>
    <div id="keywords"></div>

    <h2>Article Titles & Sentiment</h2>
    <table id="results-table">
        <thead>
            <tr>
                <th>Title</th>
                <th>Sentiment</th>
            </tr>
        </thead>
        <tbody>
            <!-- Data will be dynamically loaded here -->
        </tbody>
    </table>

    <h2>Word Cloud</h2>
    <img id="word-cloud" src="" alt="Word Cloud">
    
    <script>
        document.getElementById('search-form').addEventListener('submit', async (event) => {
            event.preventDefault();
            const crypto = document.getElementById('crypto').value;
            const response = await fetch(`/sentiment?crypto=${crypto}`);
            const data = await response.json();

            // Sentiment breakdown
            const positive = data.sentiment.positive;
            const neutral = data.sentiment.neutral;
            const negative = data.sentiment.negative;
            document.getElementById('positive').textContent = positive;
            document.getElementById('neutral').textContent = neutral;
            document.getElementById('negative').textContent = negative;

            // Keywords
            const keywords = data.keywords.join(', ');
            document.getElementById('keywords').textContent = keywords;

            // Display titles and sentiment
            const tableBody = document.querySelector('#results-table tbody');
            tableBody.innerHTML = ''; // Clear old results
            data.articles.forEach((item) => {
                const row = `
                    <tr>
                        <td>${item.title}</td>
                        <td>${item.sentiment}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });

            // Display word cloud
            const wordCloudUrl = data.wordcloud_url;
            document.getElementById('word-cloud').src = wordCloudUrl;
        });
    </script>
</body>
</html>
"""

def fetch_article_titles(crypto_name):
    """Fetch article titles from a public news source."""
    url = f"https://www.google.com/search?q={crypto_name}+cryptocurrency+news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    titles = []

    # Extracting titles from search results
    for result in soup.find_all("h3"):
        titles.append(result.text)

    return titles

def analyze_sentiment(titles):
    """Analyze sentiment for each title using VADER and TextBlob."""
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    polarity_scores = {"positive": 0, "neutral": 0, "negative": 0}

    for title in titles:
        # VADER Sentiment Analysis
        sentiment_score = analyzer.polarity_scores(title)
        sentiment = "Neutral"
        if sentiment_score['compound'] > 0.05:
            sentiment = "Positive"
            polarity_scores["positive"] += 1
        elif sentiment_score['compound'] < -0.05:
            sentiment = "Negative"
            polarity_scores["negative"] += 1
        else:
            polarity_scores["neutral"] += 1

        # TextBlob Sentiment Analysis
        polarity, subjectivity = analyze_contextual_sentiment(title)
        sentiments.append({
            "title": title,
            "sentiment": sentiment,
            "polarity": polarity,  # Range: -1 (negative) to 1 (positive)
            "subjectivity": subjectivity  # Range: 0 (objective) to 1 (subjective)
        })

    return sentiments, polarity_scores

def analyze_contextual_sentiment(title):
    """Analyze contextual sentiment using TextBlob."""
    blob = TextBlob(title)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def extract_keywords(title):
    """Extract keywords from the article title."""
    words = word_tokenize(title.lower())
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    return keywords

def generate_wordcloud(titles):
    """Generate a word cloud from article titles."""
    text = " ".join(titles)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    wordcloud_image_path = "static/wordcloud.png"
    wordcloud.to_file(wordcloud_image_path)
    return wordcloud_image_path

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/sentiment")
def sentiment():
    crypto = request.args.get("crypto", "")
    if not crypto:
        return jsonify([])

    titles = fetch_article_titles(crypto)
    sentiments, polarity_scores = analyze_sentiment(titles)
    keywords = extract_keywords(" ".join(titles))  # Extract keywords from all titles
    wordcloud_url = generate_wordcloud([item['title'] for item in sentiments])

    sentiment_trend = {
        "positive": round(polarity_scores["positive"] / len(titles) * 100, 2),
        "neutral": round(polarity_scores["neutral"] / len(titles) * 100, 2),
        "negative": round(polarity_scores["negative"] / len(titles) * 100, 2)
    }

    return jsonify({
        "articles": sentiments,
        "sentiment": sentiment_trend,
        "keywords": keywords,
        "wordcloud_url": wordcloud_url
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)
