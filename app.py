from flask import Flask, render_template_string, jsonify
import ccxt
import threading
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h1>Top 10 Meme Coins with Sentiment Analysis</h1>
    <table id="coin-table">
        <thead>
            <tr>
                <th>Rank</th>
                <th>Name</th>
                <th>Symbol</th>
                <th>Price</th>
                <th>Volatility (24h)</th>
                <th>Sentiment</th>
            </tr>
        </thead>
        <tbody>
            <!-- Data will be dynamically loaded here -->
        </tbody>
    </table>
    <script>
        async function fetchMemeCoins() {
            try {
                const response = await fetch('/data');
                const coins = await response.json();
                const tableBody = document.querySelector('#coin-table tbody');
                tableBody.innerHTML = ''; // Clear existing data

                coins.forEach((coin, index) => {
                    const row = `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${coin.name}</td>
                            <td>${coin.symbol}</td>
                            <td>$${coin.price}</td>
                            <td>${coin.volatility}%</td>
                            <td>${coin.sentiment}</td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });
            } catch (error) {
                console.error('Error fetching meme coins:', error);
            }
        }

        // Fetch data every 10 seconds
        setInterval(fetchMemeCoins, 10000);
        fetchMemeCoins(); // Initial fetch
    </script>
</body>
</html>
"""

binance = ccxt.binance()
top_meme_coins = []

# Function to perform sentiment analysis on a crypto
def perform_sentiment_analysis(symbol):
    try:
        since = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
        ohlcv = binance.fetch_ohlcv(f"{symbol}/USDT", '1h', since)

        if not ohlcv:
            return "Unknown"

        closing_prices = [candle[4] for candle in ohlcv]
        price_change = ((closing_prices[-1] - closing_prices[0]) / closing_prices[0]) * 100

        if price_change > 2:
            return "Positive"
        elif price_change < -2:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"Error analyzing sentiment for {symbol}: {e}")
        return "Error"

# Thread to update meme coin data with sentiment analysis
def update_top_meme_coins():
    global top_meme_coins
    while True:
        try:
            tickers = binance.fetch_tickers()
            meme_coins = []
            for symbol, data in tickers.items():
                if "/USDT" not in symbol:
                    continue
                high = data.get("high", 0)
                low = data.get("low", 0)
                last = data.get("last", 0)
                info = data.get("info", {})
                name = info.get("symbol", "").upper()

                if high and low and last:
                    volatility = ((high - low) / low) * 100
                    if volatility > 10 and last < 1:
                        meme_coins.append({
                            "name": name,
                            "symbol": symbol.replace("/USDT", ""),
                            "price": round(last, 8),
                            "volatility": round(volatility, 2),
                            "sentiment": "Calculating..."  # Placeholder
                        })

            # Add sentiment analysis for each crypto
            for coin in meme_coins:
                coin["sentiment"] = perform_sentiment_analysis(coin["symbol"])

            top_meme_coins = sorted(meme_coins, key=lambda x: x["volatility"], reverse=True)[:10]
        except Exception as e:
            print(f"Error fetching data: {e}")
        time.sleep(10)

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/data")
def data():
    return jsonify(top_meme_coins)

# Start the thread for meme coin updates
threading.Thread(target=update_top_meme_coins, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)
