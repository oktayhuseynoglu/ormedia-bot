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

letters = list("ABCDEFGHİJKLMNOPQRSTUVXYZ")
CATEGORIES = ["Ad", "Soyad", "Şəhər", "Meyvə", "Əşya", "Heyvan"]

games = {}

GAME_GIF = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"


# 🚀 START
@dp.message()
async def game_input(message: Message):

    # Komandaları oyuna salma
    if message.text.startswith("/"):
        return

    game = games.get(message.chat.id)
    if not game:
        return
    text = """🎮 TapBaTap Oyunu

Bot sənə bir hərf verəcək

🟡 Qaydalar:
👉 Söz tapa bilmirsənsə → - yaz
👉 Eyni hərf təkrar gəlsə → /kec yaz

💰 Düz söz = 10 xal
🏆 100 xal qalib

━━━━━━━━━━━━━━
<code>OR0310❤️</code>
"""
    await message.answer_animation(animation=GAME_GIF, caption=text, parse_mode="HTML")
    await message.answer("▶ Başla: /basla")


# ▶ BASLA
@dp.message(Command("basla"))
async def basla(message: Message):
    letter = random.choice(letters)

    games[message.chat.id] = {
        "letter": letter,
        "last_letter": None,
        "scores": {},
        "round": 1
    }

    await message.answer(f"🎯 Başladı!\n🔤 Hərf: *{letter}*", parse_mode="Markdown")


# ⏭️ KEC (yalnız eyni hərfdirsə işləsin)
@dp.message(Command("kec"))
async def skip(message: Message):
    game = games.get(message.chat.id)

    if not game:
        await message.answer("❌ Aktiv oyun yoxdur")
        return

    if game["letter"] != game["last_letter"]:
        await message.answer("❌ Bu hərf yeni gəlib, keçə bilməzsən!")
        return

    new_letter = random.choice(letters)
    game["last_letter"] = game["letter"]
    game["letter"] = new_letter

    await message.answer(f"⏭️ Keçildi!\n🔤 Yeni hərf: *{new_letter}*", parse_mode="Markdown")


# 🎮 OYUN
@dp.message()
async def game_input(message: Message):

    game = games.get(message.chat.id)
    if not game:
        return

    user_id = message.from_user.id
    words = message.text.strip().split("\n")

    if len(words) != 6:
        await message.answer("❌ 6 sətir yaz!")
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

    game["scores"][user_id] = game["scores"].get(user_id, 0) + score
    total = game["scores"][user_id]

    await message.answer(f"""
📊 Nəticə:

{chr(10).join(results)}

💰 Raund: {score}
🏆 Ümumi: {total}
""")

    # 🏆 qalib
    if total >= 100:
        await message.answer(f"""
🎉 {message.from_user.full_name} QALİB OLDU!

Növbəti oyunda hamıya uğurlar! 🚀
""")
        del games[message.chat.id]
        return

    # 🔁 yeni raund (eyni hərf də gələ bilər)
    new_letter = random.choice(letters)
    game["last_letter"] = game["letter"]
    game["letter"] = new_letter

    await message.answer(f"🔁 Yeni hərf: *{new_letter}*", parse_mode="Markdown")


# ▶ RUN
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
