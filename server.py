import asyncio
import threading
from flask import Flask
import downloader

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    asyncio.run(downloader.main())

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
