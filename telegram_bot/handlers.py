from aiogram import Router, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from telegram_bot.inline_kbs import ease_link_kb


start_router = Router()

# Задачи выполняемые ботом
@start_router.message(CommandStart())  # старт, приветствие и меню с кнопками
async def cmd_start(message: Message):
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Здравствуйте, {html.bold(message.from_user.full_name)}!", reply_markup=ease_link_kb())


@start_router.callback_query(F.data == 'contacts')  # реакция на кнопку контакты
async def send_contacts(call: CallbackQuery):
    cont = (
        "👤 <b>Название:</b> 'Осторожно люк!'\n"
        "🏠 <b>Адрес:</b> 'address'\n"
        "📧 <b>Email:</b> 'email'\n"
        "📞 <b>Телефон:</b> 'phone_number'\n"
        "🏢 <b>Компания:</b> 'Лиза Алерт'\n"
    )

    await call.message.edit_text(cont, reply_markup=ease_link_kb())
    await call.answer()


@start_router.callback_query(F.data == 'about')  # реакция на кнопку О проекте
async def send_about_project(call: CallbackQuery):
    about_pr = (
        "🏠 bla\n"
        "bla\n"
        "bla\n"
    )
    await call.message.edit_text(about_pr, reply_markup=ease_link_kb())
    await call.answer()


