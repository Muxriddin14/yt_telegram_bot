import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def get_video_info_and_download(url: str):
    ydl_opts = {
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'merge_output_format': 'mp4',
        'socket_timeout': 60,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info_dict)

            return {
                "title": info_dict.get('title'),
                "view_count": info_dict.get('view_count'),
                "duration": info_dict.get('duration'),
                "file": video_file
            }
        except Exception as e:
            logger.error(f"❌ Video yuklab olishda xatolik yuz berdi: {str(e)}")
            raise e

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Salom! 👋 Video va shorts linkini yuboring. Katta videolar yuklab olib bo\'lmaydi')

async def handle_video_link(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    await update.message.reply_text('Yuklanmoqda... ⏳ 1-2 daqiqa kuting ')

    try:
        video_info = get_video_info_and_download(url)

        response = f"🎬Sarlavha: {video_info['title']}\n"
        
        if video_info['view_count']:
            response += f"👀Ko\'rishlar soni: {video_info['view_count']}\n"
        
        response += f"⏱️Video davomiyligi: {video_info['duration']} soniya"

        await update.message.reply_text(response)

        with open(video_info["file"], 'rb') as video:
            await update.message.reply_video(video, caption="Mana, video yuklandi! 🎥")
        
        os.remove(video_info["file"])

    except Exception as e:
        if os.path.exists(video_info["file"]):
            os.remove(video_info["file"])

        await update.message.reply_text(f"❌Xatolik yuz berdi: {str(e)}")

def main() -> None:
    TOKEN = '7648754033:AAGc4aoTJM8dZtrzUfy2pdr2sgxD6EnSEdU'

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))

    application.run_polling()

if __name__ == '__main__':
    main()