import requests
import logging
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 TOKENLER
TELEGRAM_TOKEN = "8978077989:AAHO7t5gKVpGdmxAqkc0ek4KFBb7k0jDIac"
OPENROUTER_API_KEY = "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"

# ⚙️ SETTINGS
DAILY_LIMIT = 20

# 🧠 USER DATA
user_history = defaultdict(list)
user_count = defaultdict(int)

# 📝 LOG
logging.basicConfig(level=logging.INFO)

# AI sorğu
def ask_ai(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openchat/openchat-3.5",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "AI xətası 😢"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Salam!\n\nMən PRO AI botam.\nMənə istənilən sualı ver!"
    )

# /reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_history[user_id] = []
    await update.message.reply_text("Yaddaş sıfırlandı 🔄")

# mesaj handle
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # LIMIT
    if user_count[user_id] >= DAILY_LIMIT:
        await update.message.reply_text("❌ Günlük limit bitdi!")
        return

    user_count[user_id] += 1

    # HISTORY əlavə et
    user_history[user_id].append({"role": "user", "content": text})

    # SYSTEM mesaj (AZ dili)
    messages = [
        {"role": "system", "content": "Sən ağıllı AI botsan və Azərbaycan dilində cavab verirsən."}
    ] + user_history[user_id][-10:]

    reply = ask_ai(messages)

    # cavabı history-ə yaz
    user_history[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)

    # LOG
    logging.info(f"{user_id}: {text}")

# BOT START
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 PRO BOT işləyir...")
app.run_polling()
