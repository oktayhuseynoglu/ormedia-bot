import os

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "8978077989:AAHO7t5gKVpGdmxAqkc0ek4KFBb7k0jDIac"

# ================= MENU =================
def menu():
    keyboard = [
        [InlineKeyboardButton("🎥 Video yüklə", callback_data="video")],
        [InlineKeyboardButton("🎵 MP3 yüklə", callback_data="mp3")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Seçim et 👇", reply_markup=menu())

# ================= BUTTON =================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["mode"] = query.data

    if query.data == "video":
        await query.message.reply_text("Link göndər 🎥")
    elif query.data == "mp3":
        await query.message.reply_text("Link göndər 🎵")

# ================= SAFE DOWNLOAD =================
def download(url, mode="video"):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'proxy': '',   # 🔥 proxy OFF
    }

    if mode == "video":
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        })
    else:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            return None
        filename = ydl.prepare_filename(info)

        if mode == "mp3":
            filename = filename.rsplit(".", 1)[0] + ".mp3"

        return filename

# ================= MESSAGE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    mode = context.user_data.get("mode")

    if not mode:
        await update.message.reply_text("Əvvəl /start bas ⚠️")
        return

    await update.message.reply_text("Yüklənir... ⏳")

    try:
        file = download(url, mode)

        if not file or not os.path.exists(file):
            await update.message.reply_text("Media tapılmadı ❌")
            return

        if mode == "video":
            await update.message.reply_video(video=open(file, 'rb'))
        else:
            await update.message.reply_audio(audio=open(file, 'rb'))

        os.remove(file)

    except Exception as e:
        await update.message.reply_text(f"Xəta: {e}")

# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT, handle))

print("FULL FIX Bot işləyir 🚀")
app.run_polling()
