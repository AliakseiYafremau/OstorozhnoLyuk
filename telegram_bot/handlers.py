import json
import os

from aiogram import Router, F, html, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from telegram_bot.inline_kbs import ease_link_kb, kb2, kb1, fin, link_kb0, f_s

start_router = Router()


class SaveStatus(StatesGroup):  # состояния для заявки
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()


# Задачи выполняемые ботом
@start_router.message(CommandStart())  # старт, приветствие и меню с кнопками
async def cmd_start(message: Message, state: FSMContext):
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Здравствуйте, {html.bold(message.from_user.full_name)}!\n"
                         f"Я бот для регистрации открытых люков", reply_markup=ease_link_kb())


@start_router.callback_query(F.data == 'contact')  # реакция на кнопку контакты
async def send_contact(call: CallbackQuery):
    cont = (
        "👤 <b>Название:</b> 'Осторожно люк!'\n"
        "🏠 <b>Адрес:</b> 'Россия'\n"
        "📧 <b>Email:</b> 'email'\n"
        "📞 <b>Телефон:</b> 'phone_number'\n"
        "🏢 <b>Компания:</b> 'Лиза Алерт'\n"
        "<b>ВКонтакте:</b> vk.com/ostorozhnolyuk \n"
        "<b>Instagram:</b> @ostorozhnolyuk \n"
        "<b>Facebook:</b> www.facebook.com/Осторожнолюк-111280130477743 \n"
        "<b>Х (Твиттер):</b> @ostorozhnolyuk \n"
    )

    await call.message.edit_text(cont, reply_markup=ease_link_kb())
    await call.answer()


@start_router.callback_query(F.data == 'about')  # реакция на кнопку "О проекте"
async def send_about_project(call: CallbackQuery):
    about_pr = (
        "🏠 здесь\n"
        "будет\n"
        "описание\n"
        "проекта\n"
    )
    await call.message.edit_text(about_pr, reply_markup=ease_link_kb())
    await call.answer()


@start_router.callback_query(F.data == 'stop_survey')
async def stop_survey(call: types.CallbackQuery, state: FSMContext):
    # Очищаем данные из MemoryStorage
    await state.clear()  # Удаляем данные пользователя
    # Отправляем стартовое сообщение
    await call.message.answer("Опрос прерван. Выберите действие:", reply_markup=ease_link_kb())
    await call.answer()

# регистрация заявки
@start_router.callback_query(F.data == 'kb_geo')  # реакция на кнопку Создание заявки
async def send_geo(call: types.CallbackQuery):
    button_geo = [[KeyboardButton(text="Отправить свою геолокацию", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard=button_geo, resize_keyboard=True)  # создаем простую кнопку
    await call.message.answer("Нажмите кнопку внизу", reply_markup=reply_markup)
    await call.answer()


@start_router.message(F.content_type == types.ContentType.LOCATION)  # Пробелы возле равенства не ставить иначе не работает
async def location_handler(message: types.Message, state: FSMContext):
    await state.update_data(location=message.location)
    await message.answer(text="Спасибо!", reply_markup=types.ReplyKeyboardRemove())  # удаляем простую кнопку
    await message.answer(text="В каком вы городе?", reply_markup=link_kb0())
    await state.set_state(SaveStatus.Q1)  # изменение статуса


@start_router.message(SaveStatus.Q1)
async def send_address(message: types.Message, state: FSMContext):
    user_city = message.text.lower()  # получаем город от пользователя
    await state.update_data(city=user_city)  # сохраняем город в состоянии
    await message.answer(text="Адрес ближайшего здания", reply_markup=link_kb0())
    await state.set_state(SaveStatus.Q2)  # Переход к следующему вопросу


@start_router.message(SaveStatus.Q2)  # Переводим инлин кнопку в обычную
async def send_geo(message: types.Message, state: FSMContext):
    user_address = message.text.lower()
    await state.update_data(address=user_address)  # сохраняем адрес в состоянии
    await message.answer(text='Загрузите 3 фотографии', reply_markup=link_kb0())
    await state.set_state(SaveStatus.Q3)


@start_router.message(SaveStatus.Q3)
async def send_photo(message: types.Message, state: FSMContext):
    user_photos = message.photo

    if not user_photos:
        await message.answer("Пожалуйста, загрузите фотографии.")
        return

    directory = "photos"
    # Убедимся, что директория существует
    os.makedirs(directory, exist_ok=True)
    uploaded_photos = []

    #for i, user_photo in enumerate(user_photos):
    #    file_path = os.path.join(directory, f"user_photo_{i + 1}.jpg")  # Уникальное имя для каждого файла
    #    photo_file = await message.bot.get_file(user_photo.file_id)  # Получаем файл
    #    await message.bot.download_file(photo_file.file_path, file_path)  # Загружаем файл
    #    uploaded_photos.append(file_path)  # Сохраняем путь к загруженной фотографии

    if len(user_photos) >= 3:
        for i, user_photo in enumerate(user_photos[:3]):
            file_path = os.path.join(directory, f"user_photo_{i + 1}.jpg")  # Уникальное имя для каждого файла
            photo_file = await message.bot.get_file(user_photo.file_id)  # Получаем файл
            await message.bot.download_file(photo_file.file_path, file_path)  # Загружаем файл
            uploaded_photos.append(file_path)  # Сохраняем путь к загруженной фотографии
    else:
        await message.answer()
        return

    await state.update_data(photo=uploaded_photos)  # Сохраняем путь в состоянии
    await message.answer(text='Опишите проблему (необязательно)', reply_markup=kb1())
    await state.set_state(SaveStatus.Q4)


@start_router.callback_query(F.data == 'Q4')  # Если это вызов через кнопку
async def send_description(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Ваши контакты: whatsapp, telegramm, email, phone  (не обязательно)',
                                        reply_markup=kb2())
    await callback_query.answer()
    await state.set_state(SaveStatus.Q5)


@start_router.message(SaveStatus.Q4)  # Если это вызов через текстовое сообщение
async def send_contacts(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text.lower())
    await message.answer(text="Ваши контакты: whatsapp, telegramm, email, phone (не обязательно)", reply_markup=kb2())
    await state.set_state(SaveStatus.Q5)


@start_router.message(SaveStatus.Q5)  # Если это вызов через текстовое сообщение
async def send_end(message: types.Message, state: FSMContext):
    await state.update_data(contacts=message.text.lower())
    await message.answer(text="Завершить", reply_markup=fin())
    await state.set_state(SaveStatus.Q6)


@start_router.callback_query(F.data == 'Q5')
async def send_description(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text="Завершить", reply_markup=fin())
    await callback_query.answer()
    await state.set_state(SaveStatus.Q6)


@start_router.callback_query(F.data == 'Q6')
async def end(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user = {call.from_user.id: {key: (
        value if not isinstance(value, types.Location) else {"latitude": value.latitude, "longitude": value.longitude})
                                for key, value in data.items()}}
    text = [f'{key}: {value}\n' for key, value in data.items()]

    await call.message.answer(text="Ваша заявка создана!", reply_markup=f_s())  # спросить у дизайнеров как написать благодарность
    await call.message.answer(''.join(text))  # отключить после тестов

    try:
        with open('application.json', encoding='utf-8') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}
    existing_data.update(user)

    with open('application.json', 'w', encoding='utf-8') as outfile:
        json.dump(existing_data, outfile, indent=4, ensure_ascii=False)

    await state.clear()
    await call.answer()

