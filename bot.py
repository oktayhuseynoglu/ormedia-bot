import asyncio
import logging
import random

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

API_TOKEN = "8859564877:AAFzU5M2q6nsrvL-y2_89DAskjGgjDNz_5I"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 🔤 hərflər
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# 📊 kateqoriyalar
CATEGORIES = ["Ad", "Soyad", "Şəhər", "Meyvə", "Əşya", "Heyvan"]

# 📂 oyunlar
games = {}

# 🎬 GIF
GAME_GIF = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"


# 🚀 START
@dp.message(Command("start"))
async def start(message: Message):
    text = """🎮 TapBaTap Oyunu

Bot sənə bir hərf verəcək (məs: B)

Aşağıdakı sırayla yaz:

👤 Ad
👤 Soyad
🏙 Şəhər
🍎 Meyvə
🔧 Əşya
🐾 Heyvan

Hamısı həmin hərflə başlamalıdır!

🟡 Bilmirsənsə:
👉 - yaz

💰 Xal:
✔ Düz söz → 10 xal

🏆 100 xal qazanan qalib olur!

━━━━━━━━━━━━━━
<code>© OR0310❤️</code>
"""

    await message.answer_animation(
        animation=GAME_GIF,
        caption=text,
        parse_mode="HTML"
    )

    await message.answer("▶ Oyuna başla: /basla")


# ▶ BASLA
@dp.message(Command("basla"))
async def basla(message: Message):
    letter = random.choice(letters)

    games[message.chat.id] = {
        "letter": letter,
        "scores": {},
        "round": 1
    }

    await message.answer(f"""
🎯 Oyun başladı!

🔤 Hərf: *{letter}*

Bu sırayla yaz:

👤 Ad
👤 Soyad
🏙 Şəhər
🍎 Meyvə
🔧 Əşya
🐾 Heyvan

✍ Hərəsi yeni sətirdə!
""", parse_mode="Markdown")


# 🛑 STOP
@dp.message(Command("stop"))
async def stop(message: Message):
    if message.chat.id in games:
        del games[message.chat.id]
        await message.answer("🛑 Oyun dayandırıldı!")
    else:
        await message.answer("❌ Aktiv oyun yoxdur")


# 🎮 OYUN
@dp.message()
async def game_input(message: Message):

    game = games.get(message.chat.id)
    if not game:
        return

    user_id = message.from_user.id
    text = message.text.strip()
    words = text.split("\n")

    if len(words) != 6:
        await message.answer("❌ 6 sətir yazmalısan!")
        return

    letter = game["letter"].lower()
    score = 0
    results = []

    for i, w in enumerate(words):
        w = w.strip().lower()

        if w == "-":
            results.append(f"{CATEGORIES[i]}: ❌ -")
            continue

        if w.startswith(letter):
            score += 10
            results.append(f"{CATEGORIES[i]}: ✅ {w}")
        else:
            results.append(f"{CATEGORIES[i]}: ❌ {w}")

    if user_id not in game["scores"]:
        game["scores"][user_id] = 0

    game["scores"][user_id] += score
    total = game["scores"][user_id]

    await message.answer(f"""
📊 Nəticə:

{chr(10).join(results)}

💰 Bu raund: {score} xal
🏆 Ümumi: {total} xal
""")

    # 🏆 QALİB
    if total >= 100:
        winner_name = message.from_user.full_name

        await message.answer(f"""
🎉 TƏBRİKLƏR {winner_name}! 🏆

Sən 100 xal toplayaraq oyunun qalibi oldun! 👏🔥

🎮 Növbəti oyunda bütün iştirakçılara uğurlar arzulayırıq!

▶ Yenidən başlamaq üçün: /basla

━━━━━━━━━━━━━━
<code>© OR0310❤️</code>
""")

        del games[message.chat.id]
        return

    # 🔁 yeni raund
    new_letter = random.choice(letters)
    game["letter"] = new_letter
    game["round"] += 1

    await message.answer(f"""
🔁 Yeni raund!

🔤 Hərf: *{new_letter}*
""", parse_mode="Markdown")


# ▶ RUN
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
