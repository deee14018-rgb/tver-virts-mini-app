
import os
import json
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 1440263445
WEBAPP_URL = "https://deee14018-rgb.github.io/tver-virts-mini-app/"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text="🟢 Открыть TVER VIRTS",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]],
        resize_keyboard=True
    )

    await message.answer(
        "🔥 Добро пожаловать в TVER VIRTS RAKUZAN!\n\n"
        "Выбирай количество виртов и отправляй заявку.",
        reply_markup=keyboard
    )


@dp.message(F.web_app_data)
async def receive_order(message: Message):
    try:
        data = json.loads(message.web_app_data.data)

        nick = str(data.get("nick", ""))[:50]
        amount = str(data.get("amount", ""))[:30]
        price = str(data.get("price", ""))[:30]

        if not nick or not amount or not price:
            await message.answer("Не удалось прочитать заявку.")
            return

        await bot.send_message(
            ADMIN_ID,
            "📦 НОВАЯ ЗАЯВКА TVER VIRTS\n\n"
            f"🎮 Ник: {nick}\n"
            f"💰 Количество: {amount}\n"
            f"💵 Стоимость: {price}\n"
            f"👤 Telegram ID: {message.from_user.id}"
        )

        await message.answer("✅ Заявка отправлена!")

    except (ValueError, TypeError):
        await message.answer("Ошибка обработки заявки.")


async def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
