import asyncio
import logging
import sys

from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start_router
from commands import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('TOKEN')  # Токен полученый при создании в наследство https://t.me/BotFather


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # инициация бота
    dp = Dispatcher(storage=MemoryStorage())  # диспетчер задач
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeDefault())  # очистка настроек ТГ
    # подключение наших команд
    await bot.set_my_commands(commands, scope=types.BotCommandScopeDefault())
    await dp.start_polling(bot)  # запуск


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
