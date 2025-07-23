import requests
import time
import os
import json
import logging
from datetime import datetime
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

def fetch_binance_data(symbol="BTCUSDT", interval="15m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return data

def calculate_rsi(data, period=14):
    closes = [float(c[4]) for c in data]
    deltas = [closes[i+1] - closes[i] for i in range(len(closes)-1)]
    gains = [d for d in deltas if d > 0]
    losses = [-d for d in deltas if d < 0]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

def send_trade_signal(signal_type, price):
    message = f"🚨 *{signal_type} Signal for BTC/USDT*
Price: ${price:.2f}
Time: {datetime.utcnow().strftime('%H:%M UTC')}"
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def detect_trade():
    data = fetch_binance_data()
    rsi = calculate_rsi(data)
    close_price = float(data[-1][4])

    if rsi < 30:
        send_trade_signal("BUY", close_price)
    elif rsi > 70:
        send_trade_signal("SELL", close_price)

if __name__ == "__main__":
    while True:
        try:
            detect_trade()
            time.sleep(60 * 15)
        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(60)