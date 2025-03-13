from flask import Flask
import asyncio
import downloader  # Sizning bot kodingiz downloader.py faylida

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def run_bot():
    await downloader.main()  # downloader.py ichidagi asosiy bot funksiyasini asinxron chaqirish

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(run_bot())  # Botni ishga tushiramiz
    app.run(host="0.0.0.0", port=10000)  # Flask server 10000-portda ishlaydi
