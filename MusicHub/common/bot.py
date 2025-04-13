import logging
import asyncio
import sys
import requests

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message


TOKEN = '7981053598:AAHYs0_g3VQ6B9myCpSiFzoIpjDeoXp244g'

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎵 Скачать трек"), KeyboardButton(text="💳 Проверить подписку")],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="🔄 Переключить тему")]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def send_welcome(message):
    starter_text = (
        f"Привет, {html.bold(message.from_user.first_name)}!\n"
        "Я MusicHub Bot — твой помощник по скачиванию купленных треков.\n\n"
        "Выбери нужную команду:\n"
        "🎵 Скачать трек\n"
        "💳 Проверить подписку\n"
        "ℹ️ Помощь\n"
    )
    await message.answer(starter_text, reply_markup=main_menu)


@dp.message(Command(commands=["help"]))
async def send_help(message):
    help_text = (
        "🔹 /start — Приветственное сообщение\n"
        "🔹 /download Название_Трека — Скачать купленный трек\n"
        "🔹 /check_subscription — Проверить подписку\n"
    )
    await message.answer(help_text)
    
    
@dp.message(F.text)
async def handle_unknown_commands(message: Message):
    await message.answer("❌ Извините, я не понял команду. Используйте /help для списка команд.")
    

@dp.message(Command(commands=["check_subscription"]))
async def check_subscription(message):
    user_id = message.from_user.id
    response = requests.get(f"http://127.0.0.1:8000/api/check-subscription/{user_id}/")
    data = response.json()
    
    if data['status'] == 'success':
        await message.answer("✅ У вас есть активная подписка! Вы можете скачивать треки.")
    else:
        await message.answer("❌ У вас нет подписки. Оформите её на сайте MusicHub.")

@dp.message(Command(commands=["download"]))
async def download_track(message):
    user_id = message.from_user.id
    track_name = message.text.replace("/download ", "").strip()

    response = requests.get(f"http://127.0.0.1:8000/api/check-subscription/{user_id}/{track_name}/")
    data = response.json()

    if data['status'] == 'success':
        await message.answer(f"🎵 Твой трек: {track_name}\nСкачивай тут: {data['download_url']}")
    else:
        await message.answer(f"❌ Ошибка: {data['message']}")


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    