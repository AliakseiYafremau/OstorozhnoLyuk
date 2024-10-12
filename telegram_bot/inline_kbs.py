
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
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def link_kb0():
    inline_kb_add = [
        [InlineKeyboardButton(text="Прервать", callback_data='stop_survey')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_add)


def kbg():
    inline_kb1 = [
        [InlineKeyboardButton(text="Предоставить координаты", callback_data='kb_geo')],
        [InlineKeyboardButton(text="Прервать", callback_data='stop_survey')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb1)


def kb1():
    inline_kb1 = [
        [InlineKeyboardButton(text="Пропустить", callback_data='Q6')],
        [InlineKeyboardButton(text="Прервать", callback_data='stop_survey')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb1)


def kb2():
    inline_kb2 = [
        [InlineKeyboardButton(text="Пропустить", callback_data='Q7')],
        [InlineKeyboardButton(text="Прервать", callback_data='stop_survey')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb2)


def fin():
    inline_kb_fin = [
        [InlineKeyboardButton(text="Завершить", callback_data='Q8')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_fin)


def f_s():
    inline_kbc = [
        [InlineKeyboardButton(text="Вернуться в Меню", callback_data='stop_survey')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kbc)