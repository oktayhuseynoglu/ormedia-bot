import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8978077989:AAHO7t5gKVpGdmxAqkc0ek4KFBb7k0jDIac"
OPENROUTER_API_KEY = "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"

def ask_ai(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",  # 🔥 PREMIUM MODEL
        "messages": messages,
        "temperature": 0.7
    }

    res = requests.post(url, headers=headers, json=data)

    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        return "AI error 😢"

# 🔁 memory (chat history)
user_memory = {}

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_memory:
        user_memory[user_id] = [
            {"role": "system", "content": "You are a premium ChatGPT-like AI assistant."}
        ]

    user_memory[user_id].append({"role": "user", "content": text})

    reply = ask_ai(user_memory[user_id])

    user_memory[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("🔥 Premium bot running...")
app.run_polling()
