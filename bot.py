import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "616220389:AAHYyvBBc-uUbnaPUN4x6q3Z7Wn4JCO7olw"

waiting_player = None
games = {}

keyboard = [["🎮 Multiplayer", "❌ Stop"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Multiplayer oyununa xoş gəldin!",
        reply_markup=markup
    )

# multiplayer start
async def multiplayer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_player

    user = update.message.from_user
    user_id = user.id

    if waiting_player is None:
        waiting_player = user_id
        await update.message.reply_text("⏳ Rəqib gözlənilir...")
    else:
        player1 = waiting_player
        player2 = user_id

        number = random.randint(1, 100)

        games[player1] = {
            "number": number,
            "turn": player1,
            "opponent": player2
        }

        games[player2] = {
            "number": number,
            "turn": player1,
            "opponent": player1
        }

        waiting_player = None

        await update.message.reply_text("🎮 Oyun başladı!\n🔢 1-100 arası ədəd tutuldu.")
        await context.bot.send_message(player1, "👉 Sənin növbəndir!")
        await context.bot.send_message(player2, "⏳ Rəqibin oynayır...")

# handle
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    text = update.message.text

    if text == "🎮 Multiplayer":
        await multiplayer(update, context)
        return

    if user_id not in games:
        return

    game = games[user_id]

    if game["turn"] != user_id:
        await update.message.reply_text("⏳ Növbə səndə deyil")
        return

    try:
        guess = int(text)
    except:
        await update.message.reply_text("🔢 Rəqəm yaz!")
        return

    number = game["number"]
    opponent = game["opponent"]

    if guess < number:
        await update.message.reply_text("📉 Daha böyük")
        await context.bot.send_message(opponent, "👉 Sənin növbəndir")
        games[user_id]["turn"] = opponent
        games[opponent]["turn"] = opponent

    elif guess > number:
        await update.message.reply_text("📈 Daha kiçik")
        await context.bot.send_message(opponent, "👉 Sənin növbəndir")
        games[user_id]["turn"] = opponent
        games[opponent]["turn"] = opponent

    else:
        await update.message.reply_text("🎉 QAZANDIN!")
        await context.bot.send_message(opponent, "😢 Uduzdun!")

        del games[user_id]
        del games[opponent]

# stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in games:
        opponent = games[user_id]["opponent"]
        await context.bot.send_message(opponent, "❌ Rəqib oyunu tərk etdi")
        del games[opponent]
        del games[user_id]

    await update.message.reply_text("🛑 Oyun dayandırıldı")

# setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.add_handler(CommandHandler("stop", stop))

print("🎮 Multiplayer bot işləyir...")
app.run_polling()
