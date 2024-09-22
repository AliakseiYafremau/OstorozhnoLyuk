from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


# Меню с инлайн кнопками (ссыылки необходимо будет заменить)

def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Оставить Заявку",
                              web_app=WebAppInfo(url="https://docs.aiogram.dev/en/"))],
        [InlineKeyboardButton(text="📖 О проекте", callback_data='about')],
        [InlineKeyboardButton(text="📝 Контакты", callback_data='contacts')],
        [InlineKeyboardButton(text="👤 Новости",
                              web_app=WebAppInfo(url="https://ixbt.games/tools/"))],
        [InlineKeyboardButton(text="📚 Открытые люки в моём городе",
                              web_app=WebAppInfo(url="https://translate.yandex.ru/?source_lang=en&target_lang=ru"))],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

