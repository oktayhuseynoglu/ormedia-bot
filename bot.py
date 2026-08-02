import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8616220389:AAHYyvBBc-uUbnaPUN4x6q3Z7Wn4JCO7olw"
OPENROUTER_API_KEY = "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"

# 🧠 AI function (ASYNC - FIXED)
async def ask_ai(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openchat/openchat-3.5",
        "messages": messages
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as res:
                text = await res.text()

                if res.status != 200:
                    return f"API ERROR {res.status}\n{text}"

                json_data = await res.json()
                return json_data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Xəta: {str(e)}"

# 🧠 memory
user_memory = {}

# 💬 handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_memory:
        user_memory[user_id] = [
            {"role": "system", "content": "Azərbaycan dilində danışan ChatGPT kimisən."}
        ]

    user_memory[user_id].append({"role": "user", "content": text})

    reply = await ask_ai(user_memory[user_id])

    user_memory[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)

# 🚀 run
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🔥 Bot işləyir...")
app.run_polling()
