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
    "👤 Soyad",
    "🏙 Şəhər",
    "🍎 Meyvə",
    "🔧 Əşya",
    "🐾 Heyvan"
]


games = {}


GAME_GIF = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"



# =========================
# START
# =========================

@dp.message(Command("start"))
async def start(message: Message):

    text = """
🎮 <b>TapBaTap Oyunu</b>

Söz tapma yarışına xoş gəlmisən!


📌 Qaydalar:

🔤 Bot hər raundda bir hərf verir.

Sən bu sırayla cavab yazırsan:

1️⃣ Ad
2️⃣ Soyad
3️⃣ Şəhər
4️⃣ Meyvə
5️⃣ Əşya
6️⃣ Heyvan


⭐ Düz cavab = 10 xal


❌ Söz tapa bilməsən:
<code>-</code> yaz


⏭ Eyni hərf təkrar gəlsə:
<code>/kec</code> yaz


🏆 100 xal toplayan qalib olur!


━━━━━━━━━━━━━━
<code>OR0310❤️</code>
"""

    await message.answer_animation(
        animation=GAME_GIF,
        caption=text,
        parse_mode="HTML"
    )


    await message.answer(
        "🚀 Oyuna başlamaq üçün:\n\n/basla"
    )



# =========================
# BASLA
# =========================

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
🎮 <b>TAPBATAP BAŞLADI!</b> 🔥

━━━━━━━━━━━━━━

🔤 <b>Sənin hərfin:</b>

🌟 <code>{letter}</code>

━━━━━━━━━━━━━━


📝 <b>Cavabları bu sırayla yaz:</b>


1️⃣ 👤 Ad

2️⃣ 👤 Soyad

3️⃣ 🏙 Şəhər

4️⃣ 🍎 Meyvə

5️⃣ 🔧 Əşya

6️⃣ 🐾 Heyvan


━━━━━━━━━━━━━━


💡 Söz tapa bilməsən:

➡️ <code>-</code> yaz


⏭ Təkrar hərf gəlsə:

➡️ /kec yaz


🏆 Düz cavab:

⭐ 10 xal


🎯 Qalib:

💯 100 xal


━━━━━━━━━━━━━━

🚀 Uğurlar!
""",
        parse_mode="HTML"
    )



# =========================
# STOP
# =========================

@dp.message(Command("stop"))
async def stop(message: Message):

    if message.chat.id in games:

        del games[message.chat.id]

        await message.answer(
            "🛑 Oyun dayandırıldı!"
        )

    else:

        await message.answer(
            "❌ Aktiv oyun yoxdur"
        )



# =========================
# KEC
# =========================

@dp.message(Command("kec"))
async def kec(message: Message):

    game = games.get(message.chat.id)


    if not game:

        await message.answer(
            "❌ Aktiv oyun yoxdur"
        )

        return


    if game["letter"] != game["last_letter"]:

        await message.answer(
            "❌ Bu hərf yenidir.\n/kec yalnız təkrar hərfdə işləyir."
        )

        return



    new_letter = random.choice(LETTERS)


    game["last_letter"] = game["letter"]

    game["letter"] = new_letter



    await message.answer(
        f"""
⏭ <b>Raund keçildi!</b>

🔤 Yeni hərf:

🌟 <code>{new_letter}</code>
""",
        parse_mode="HTML"
    )



# =========================
# OYUN CAVABLARI
# =========================

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
⚠️ <b>Oyunun qaydalarına uyğun mesaj yazın!</b>


📝 Format:


Ad

Soyad

Şəhər

Meyvə

Əşya

Heyvan


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
📊 <b>Nəticə</b>


{chr(10).join(results)}


⭐ Bu raund:
{score} xal


🏆 Ümumi:
{total} xal
""",
        parse_mode="HTML"
    )



    if total >= 100:


        await message.answer(
            f"""
🎉 <b>TƏBRİKLƏR!</b> 🏆


👑 {message.from_user.full_name}


100 xal toplayaraq qalib oldun!


🎮 Növbəti oyunda bütün iştirakçılara uğurlar arzulayırıq! 🚀
"""
            ,
            parse_mode="HTML"
        )


        del games[message.chat.id]

        return



    new_letter = random.choice(LETTERS)


    game["last_letter"] = game["letter"]

    game["letter"] = new_letter


    await message.answer(
        f"""
🔁 Yeni raund!


🔤 Hərf:

🌟 <code>{new_letter}</code>
""",
        parse_mode="HTML"
    )



# =========================
# RUN
# =========================

async def main():

    await dp.start_polling(bot)



if __name__ == "__main__":

    asyncio.run(main())
