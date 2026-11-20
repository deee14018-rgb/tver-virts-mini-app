
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
        "🔥 TVER VIRTS RAKUZAN\n\n"
        "Выбирай количество виртов и отправляй заявку!",
        reply_markup=keyboard
    )


@dp.message(F.web_app_data)
async def receive_order(message: Message):
    try:
        data = json.loads(message.web_app_data.data)

        if data.get("type") != "new_order":
            await message.answer("Неизвестный тип заявки.")
            return

        amount = int(data.get("amount_millions", 0))
        price = int(data.get("total_rub", 0))
        server = str(data.get("server", ""))[:30]

        if not (1 <= amount <= 10000):
            raise ValueError("Invalid amount")

        if price != amount * 50 or server != "83 Tver":
            raise ValueError("Invalid order")

        user = message.from_user
        username = user.username or "не указан"

        await bot.send_message(
            ADMIN_ID,
            "📦 НОВАЯ ЗАЯВКА!\n\n"
            f"🎮 Сервер: {server}\n"
            f"💰 Количество: {amount}кк\n"
            f"💵 Стоимость: {price} ₽\n"
            f"👤 Telegram: @{username}\n"
            f"🆔 ID: {user.id}"
        )

        await message.answer("✅ Заявка отправлена администратору!")

    except (ValueError, TypeError, json.JSONDecodeError):
        await message.answer("❌ Не удалось обработать заявку.")


async def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")

    global bot
    bot = Bot(token=TOKEN)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
