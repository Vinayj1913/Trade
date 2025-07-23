# BTC Telegram Signal Bot

This bot fetches BTC/USDT data every 15 minutes and sends high-accuracy trade signals (based on RSI) to a Telegram bot.

## Setup

1. Create your Telegram bot using @BotFather and get the token.
2. Set the following environment variables:
   - TELEGRAM_TOKEN
   - TELEGRAM_CHAT_ID (your own chat ID or group ID)
3. Host it using [Render](https://render.com) or [Railway](https://railway.app).

## Strategy

- RSI < 30: Buy signal
- RSI > 70: Sell signal