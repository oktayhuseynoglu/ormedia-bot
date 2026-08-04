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


LETTERS = list("ABÇDEƏFGHİJKLMNOPRSŞTUÜVXYZ")


CATEGORIES = [
    "👤 Ad",
    "👥 Soyad",
    "🌍 Şəhər",
    "🍎 Meyvə",
    "📦 Əşya",
    "🐾 Heyvan"
]


games = {}


GAME_GIF = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"



# ======================
# START
# ======================

@dp.message(Command("start"))
async def start(message: Message):

    text = """
🎮 <b>TapBaTap Oyunu</b> 🔥

👋 Xoş gəlmisən!

🧩 Söz tapma yarışına başla!
━━━━━━━━━━━━━━
📌 <b>Oyun qaydaları:</b>

🔤 Bot bir hərf verir.

📝 Bu sırayla cavab yaz:

1️⃣ 👤 Ad

2️⃣ 👥 Soyad

3️⃣ 🌍 Şəhər

4️⃣ 🍎 Meyvə

5️⃣ 📦 Əşya

6️⃣ 🐾 Heyvan
━━━━━━━━━━━━━━
⭐ Düz cavab:
➕ 10 xal
❌ Söz tapa bilmirsənsə:
➡️ - yaz
⏭️ Təkrar hərf olsa:
➡️ /kec yaz
🏆 100 xal:
👑 QALİB
━━━━━━━━━━━━━━
⚙️ Bot coperating OR0310 ❤️
"""

    await message.answer_animation(
        animation=GAME_GIF,
        caption=text,
        parse_mode="HTML"
    )


    await message.answer(
        "🚀 Oyuna başlamaq üçün:\n\n🎮 /basla"
    )



# ======================
# BASLA
# ======================

@dp.message(Command("basla"))
async def basla(message: Message):

    letter = random.choice(LETTERS)


    games[message.chat.id] = {

        "letter": letter,
        "last_letter": None,
        "scores": {},
        "round": 1

    }


    await message.answer(
f"""
🎮 <b>Yeni oyun başladı!</b> 🔥
━━━━━━━━━━━━━━
🔤 <b>Hərf:</b>

⭐ {letter}
━━━━━━━━━━━━━━
📝 Cavabları bu formada yaz:
👤 Ad
👥 Soyad
🌍 Şəhər
🍎 Meyvə
📦 Əşya
🐾 Heyvan
━━━━━━━━━━━━━━
💡 Bilmədiyin söz:
➖ - yaz
⏭️ Təkrar hərf:
➡️ /kec
🍀 Uğurlar!
""",
parse_mode="HTML"
)



# ======================
# STOP
# ======================

@dp.message(Command("stop"))
async def stop(message: Message):

    if message.chat.id in games:

        del games[message.chat.id]

        await message.answer(
"""
🛑 <b>Oyun dayandırıldı!</b>

🎮 Yenidən başlamaq üçün:

➡️ /basla
""",
parse_mode="HTML"
        )

    else:

        await message.answer(
            "❌ Aktiv oyun yoxdur"
        )



# ======================
# KEC
# ======================

@dp.message(Command("kec"))
async def kec(message: Message):

    game = games.get(message.chat.id)


    if not game:

        await message.answer(
            "❌ Aktiv oyun yoxdur"
        )

        return



    new_letter = random.choice(LETTERS)


    game["last_letter"] = game["letter"]

    game["letter"] = new_letter



    await message.answer(
f"""
⏭️ <b>Hərf keçildi!</b>
🔄 Yeni raund:
🔤 Yeni hərf:
⭐ {new_letter}

🔥 Davam et!
""",
parse_mode="HTML"
)



# ======================
# OYUN
# ======================

@dp.message()
async def game_input(message: Message):


    if message.text.startswith("/"):
        return



    game = games.get(message.chat.id)


    if not game:
        return



    words = message.text.strip().split("\n")



    if len(words) != 6:

        await message.answer(
"""
⚠️ <b>Oyunun qaydasına uyğun yaz!</b>
📝 Cavab formatı:
👤 Ad
👥 Soyad
🌍 Şəhər
🍎 Meyvə
📦 Əşya
🐾 Heyvan
Hər biri ayrı sətirdə olmalıdır.
""",
parse_mode="HTML"
        )

        return



    user_id = message.from_user.id


    letter = game["letter"].lower()


    score = 0

    results = []



    for i, word in enumerate(words):

        word = word.strip().lower()


        if word == "-":

            results.append(
                f"{CATEGORIES[i]} ❌ -"
            )

            continue



        if word.startswith(letter):

            score += 10

            results.append(
                f"{CATEGORIES[i]} ✅ {word}"
            )

        else:

            results.append(
                f"{CATEGORIES[i]} ❌ {word}"
            )



    if user_id not in game["scores"]:

        game["scores"][user_id] = 0



    game["scores"][user_id] += score


    total = game["scores"][user_id]



    await message.answer(
f"""
📊 <b>Raund nəticəsi</b> 🎯


━━━━━━━━━━━━━━


{chr(10).join(results)}


━━━━━━━━━━━━━━


⭐ Bu raund:
➕ {score} xal

🏆 Ümumi:
💰 {total} xal

🔥 Davam edirik!
""",
parse_mode="HTML"
)



    if total >= 100:


        await message.answer(
f"""
🎉🎉 <b>TƏBRİKLƏR!</b> 🎉🎉

👑 Qalib:

<b>{message.from_user.full_name}</b>

🏆 100 xal topladı!

🍀 Növbəti oyunda hamıya uğurlar!

━━━━━━━━━━━━━━

⚙️ OR0310 ❤️

━━━━━━━━━━━━━━
""",
parse_mode="HTML"
        )


        del games[message.chat.id]

        return



    new_letter = random.choice(LETTERS)


    game["last_letter"] = game["letter"]

    game["letter"] = new_letter



    await message.answer(
f"""
🔄 <b>Yeni raund!</b>

🔤 Hərf:

⭐ {new_letter}

🎮 Uğurlar!
""",
parse_mode="HTML"
)



# ======================
# RUN
# ======================

async def main():

    await dp.start_polling(bot)



if __name__ == "__main__":

    asyncio.run(main())
