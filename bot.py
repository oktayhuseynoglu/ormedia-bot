import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8616220389:AAHYyvBBc-uUbnaPUN4x6q3Z7Wn4JCO7olw"

# istifadəçi üçün oyun məlumatı
games = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Oyun botuna xoş gəldin!\n\n/startgame yaz və oyuna başla."
    )

# oyuna başla
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    number = random.randint(1, 100)

    games[user_id] = number

    await update.message.reply_text(
        "🔢 Mən 1 ilə 100 arasında bir ədəd tutdum.\nTap görüm 😎"
    )

# mesaj handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in games:
        await update.message.reply_text("Əvvəl /startgame yaz 🤖")
        return

    try:
        guess = int(text)
    except:
        await update.message.reply_text("Zəhmət olmasa rəqəm yaz 🔢")
        return

    number = games[user_id]

    if guess < number:
        await update.message.reply_text("📉 Daha böyük rəqəm de")
    elif guess > number:
        await update.message.reply_text("📈 Daha kiçik rəqəm de")
    else:
        await update.message.reply_text("🎉 Düz tapdın! Təbriklər!")
        del games[user_id]

# bot setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("startgame", start_game))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🎮 Oyun botu işləyir...")
app.run_polling()
