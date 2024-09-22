import asyncio
import logging
import sys

from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from telegram_bot.handlers import start_router
from dotenv import load_dotenv

load_dotenv()


TOKEN = getenv('TOKEN')  # Токен полученый при создании в наследство https://t.me/BotFather

dp = Dispatcher()  # диспетчер задач

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # инициация бота


async def main() -> None:
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  # запуск


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
