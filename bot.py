import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

# 🔥 Proxy TAM SÖNDÜR (çox vacib)
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

TOKEN = os.getenv("8978077989:AAHO7t5gKVpGdmxAqkc0ek4KFBb7k0jDIac")  # Railway üçün

logging.basicConfig(level=logging.INFO)

# 🎥 Video download funksiyası
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'proxy': None,  # 🔥 proxy OFF
        'outtmpl': 'video.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# 📩 Mesaj handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("Yüklənir ⏳")

    try:
        file = download_video(url)

        await update.message.reply_video(video=open(file, 'rb'))

        os.remove(file)

    except Exception as e:
        print("Xəta:", e)
        await update.message.reply_text("Media tapılmadı ❌")

# 🚀 Bot start
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot işləyir 🚀")

app.run_polling()
