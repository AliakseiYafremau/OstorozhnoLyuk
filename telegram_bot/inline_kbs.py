
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


# Меню с инлайн кнопками (ссылки необходимо будет заменить)
def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Оставить Заявку",
                              callback_data='application')],
        [InlineKeyboardButton(text="📖 О проекте", callback_data='about')],
        [InlineKeyboardButton(text="📝 Контакты", callback_data='contact')],
        [InlineKeyboardButton(text="👤 Новости",
                              web_app=WebAppInfo(url="https://ixbt.games/tools/"))],
        [InlineKeyboardButton(text="📚 Открытые люки в моём городе",
                              web_app=WebAppInfo(url="https://translate.yandex.ru/?source_lang=en&target_lang=ru"))],
        [InlineKeyboardButton(text="😁 Стикеры", callback_data='stick')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def link_kb0():
    inline_kb_add = [
        [InlineKeyboardButton(text="Прервать", callback_data='cancel')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_add)


def kbg():
    inline_kb1 = [
        [InlineKeyboardButton(text="Предоставить координаты", callback_data='kb_geo')],
        [InlineKeyboardButton(text="Прервать", callback_data='cancel')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb1)


def kb1():
    inline_kb1 = [
        [InlineKeyboardButton(text="Пропустить", callback_data='Q5')],
        [InlineKeyboardButton(text="Прервать", callback_data='cancel')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb1)


def contact_kb():
    inline_co_kb_list = [
        [InlineKeyboardButton(text="email", callback_data='Q5a')],
        [InlineKeyboardButton(text="whatsapp", callback_data='Q5b')],
        [InlineKeyboardButton(text="telegram", callback_data='Q5c')],
        [InlineKeyboardButton(text="phone", callback_data='Q5d')],
        [InlineKeyboardButton(text="Пропустить", callback_data='Q7')],
        [InlineKeyboardButton(text="Прервать", callback_data='cancel')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_co_kb_list)


def fin():
    inline_kb_fin = [
        [InlineKeyboardButton(text="Завершить", callback_data='Q7')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_fin)


def f_s():
    inline_kbc = [
        [InlineKeyboardButton(text="Вернуться в Меню", callback_data='cancel')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kbc)
