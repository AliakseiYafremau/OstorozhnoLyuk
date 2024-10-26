import json
import logging
import os

from aiogram.client.session import aiohttp
from aiohttp import ClientSession
from aiogram import Router, F, html, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup

from inline_kbs import ease_link_kb, kb1, fin, link_kb0, f_s, kbg, contact_kb
from text_messages import cont, about_pr, hp, stick_pr

start_router = Router()
logging.basicConfig(level=logging.INFO)


class SaveStatus(StatesGroup):  # состояния для заявки
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q5a = State()
    Q5b = State()
    Q5c = State()
    Q5d = State()
    Q6 = State()
    Q6a = State()
    Q6b = State()
    Q6c = State()
    Q6d = State()


# Задачи выполняемые ботом
@start_router.message(CommandStart())  # старт, приветствие и меню с кнопками
async def cmd_start(message: Message):
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Здравствуйте, {html.bold(message.from_user.full_name)}!\n"
                         f"Я бот для регистрации открытых люков", reply_markup=ease_link_kb())


@start_router.callback_query(F.data == 'contact')  # реакция на кнопку "Контакты"
async def send_contact(call: CallbackQuery):
    await call.message.edit_text(cont, reply_markup=ease_link_kb())
    await call.answer()


@start_router.message(F.text == '/contact')
async def send_contact(message: types.Message):
    await message.answer(cont, reply_markup=ease_link_kb())


@start_router.callback_query(F.data == 'about')  # реакция на кнопку "О проекте"
async def send_about_project(call: CallbackQuery):
    await call.message.edit_text(about_pr, reply_markup=ease_link_kb())
    await call.answer()


@start_router.message(F.text == '/about')
async def send_about_com(message: types.Message):
    await message.answer(about_pr, reply_markup=ease_link_kb())


@start_router.callback_query(F.data == 'stick')  # реакция на кнопку "О проекте"
async def send_stick(call: CallbackQuery):
    await call.message.edit_text(stick_pr, reply_markup=ease_link_kb())
    await call.answer()


@start_router.callback_query(F.data == 'cancel')  # реализация прерывания
async def stop_survey(call: types.CallbackQuery, state: FSMContext):
    # Очищаем данные из MemoryStorage
    await state.clear()
    await call.answer()
    # Отправляем стартовое сообщение
    await call.message.answer("Оформление заявки завершено. Выберите действие:", reply_markup=ease_link_kb())


@start_router.message(F.text == '/cancel')
async def send_about_com(message: types.Message, state: FSMContext):
    # Очищаем данные из MemoryStorage
    await state.clear()
    # Отправляем стартовое сообщение
    await message.answer("Оформление заявки завершено. Выберите действие:", reply_markup=ease_link_kb())


@start_router.message(F.text == '/help')
async def send_help(message: types.Message):
    await message.answer(hp, reply_markup=ease_link_kb())


# регистрация заявки
@start_router.callback_query(F.data == 'application')  # реакция на кнопку Создание заявки
async def send_photo(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Сделайте 5 фото открытого люка в разных ракурсах: \n"
                              "одну вблизи и четыре с окрестностями. \n"
                              "Загрузите фото вблизи в режиме «фото» 1 шт.\n")
    await call.answer()
    await state.set_state(SaveStatus.Q1)


@start_router.message(SaveStatus.Q1)
async def handle_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    directory = 'photos'
    # Проверяем, существует ли директория
    if not os.path.exists(directory):
        os.makedirs(directory)  # Создаем директорию, если она не существует
    photos = data.get('photos', [])  # Используем .get() для безопасного доступа

    if message.photo:
        # Получаем первую (наилучшую) фотографию из списка
        best_photo = message.photo[-1]
        file_id = best_photo.file_id
        file = await message.bot.get_file(file_id)
        file_path = os.path.join(directory, f"{file_id}.jpg")  # Путь файла

        await message.bot.download_file(file.file_path, file_path)  # Сохраняем фотографию

        photos.append(file_path)  # Добавляем путь к фото в список
        await state.update_data(photos=photos)  # Обновляем состояние

        total_photos = len(photos)  # считаем количество фото
        if total_photos == 1:
            await message.reply("Загрузите 4 фото открытого люка с окрестностями в режиме «фото». 📷")

        if total_photos == 5:
            await message.answer("Все 5 фотографий загружены! Пожалуйста, включите определение местоположения.",
                                 reply_markup=kbg())
    else:
        await message.answer("Ошибка. Пожалуйста, загрузите фотографию люка.")


@start_router.callback_query(F.data == 'kb_geo')  # Создание кнопки для получения координат
async def send_geo(call: types.CallbackQuery,  state: FSMContext):
    button_geo = [[KeyboardButton(text="Отправить свою геолокацию", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard=button_geo, resize_keyboard=True)  # создаем простую кнопку
    await call.message.answer("Введи координаты в формате: широта, долгота (например: 55.7558, 37.6173) \n"
                              "Или нажмите кнопку внизу 👇", reply_markup=reply_markup)
    await call.answer()
    await state.set_state(SaveStatus.Q2)


@start_router.message(F.content_type == types.ContentType.LOCATION, SaveStatus.Q2)  # обработка координат
async def location_handler(message: types.Message, state: FSMContext):
    await state.update_data(location=message.location)
    await message.answer(text="Спасибо!", reply_markup=types.ReplyKeyboardRemove())  # удаляем простую кнопку
    await message.answer(text="В каком вы городе?", reply_markup=link_kb0())
    await state.set_state(SaveStatus.Q3)  # изменение статуса


# Новый хендлер для обработки координат вручную (в виде текста)

@start_router.message(SaveStatus.Q2)
async def manual_coordinates(message: types.Message, state: FSMContext):
    try:
        lat, lon = map(float, message.text.split(','))
        location = types.Location(latitude=lat, longitude=lon)
        await state.update_data(location=location)
        await message.answer(text="Спасибо за координаты!", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text="В каком вы городе?", reply_markup=link_kb0())
        await state.set_state(SaveStatus.Q3)
    except ValueError:
        await message.answer(
            "Ошибка! Пожалуйста, введи координаты в формате: широта, долгота (например: 55.7558, 37.6173)."
        )


@start_router.message(SaveStatus.Q3)
async def send_address(message: types.Message, state: FSMContext):
    user_city = message.text.lower()  # получаем город от пользователя
    await state.update_data(city=user_city)  # сохраняем город в состоянии
    await message.answer(text="Адрес ближайшего здания", reply_markup=link_kb0())
    await state.set_state(SaveStatus.Q4)  # Переход к следующему вопросу


@start_router.message(SaveStatus.Q4)  # Переводим инлин кнопку в обычную
async def send_description(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.lower())  # сохраняем адрес в состоянии
    await message.answer(text='Опишите проблему (необязательно)', reply_markup=kb1())
    await state.set_state(SaveStatus.Q5)


@start_router.callback_query(F.data == 'Q5')  # Если это вызов через кнопку
async def send_contacts(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Хотите оставить контакты для оповещения о статусе заявки? (не обязательно)',
                                        reply_markup=contact_kb())
    await callback_query.answer()


@start_router.message(SaveStatus.Q5)  # Если это вызов через текстовое сообщение
async def send_contacts(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text.lower())
    await message.answer(text="Хотите оставить контакты для оповещения о статусе заявки? (не обязательно)",
                         reply_markup=contact_kb())


@start_router.callback_query(F.data == 'Q5a')
async def send_email(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Укажите Email',
                                        reply_markup=link_kb0())
    await callback_query.answer()
    await state.set_state(SaveStatus.Q6a)


@start_router.callback_query(F.data == 'Q5b')
async def send_whatsapp(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Укажите Whatsapp',
                                        reply_markup=link_kb0())
    await callback_query.answer()
    await state.set_state(SaveStatus.Q6b)


@start_router.callback_query(F.data == 'Q5c')
async def send_telegram(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Укажите Telegram (без @)',
                                        reply_markup=link_kb0())
    await callback_query.answer()
    await state.set_state(SaveStatus.Q6c)


@start_router.callback_query(F.data == 'Q5d')
async def send_phone(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Укажите номер телефона',
                                        reply_markup=link_kb0())
    await callback_query.answer()
    await state.set_state(SaveStatus.Q6d)


@start_router.message(SaveStatus.Q6a)  # Если это вызов через текстовое сообщение
async def handle_email_input(message: types.Message, state: FSMContext):
    user_email = message.text.lower()
    await state.update_data(contacts=user_email)
    await message.answer(text="Завершить", reply_markup=fin())


@start_router.message(SaveStatus.Q6b)  # Если это вызов через текстовое сообщение
async def handle_whatsapp_input(message: types.Message, state: FSMContext):
    user_whatsapp = message.text.lower()
    await state.update_data(contacts=user_whatsapp)
    await message.answer(text="Завершить", reply_markup=fin())


@start_router.message(SaveStatus.Q6c)  # Если это вызов через текстовое сообщение
async def handle_telegram_input(message: types.Message, state: FSMContext):
    user_telegram = message.text.lower()
    await state.update_data(contacts=user_telegram)
    await message.answer(text="Завершить", reply_markup=fin())


@start_router.message(SaveStatus.Q6d)  # Если это вызов через текстовое сообщение
async def handle_phone_input(message: types.Message, state: FSMContext):
    user_phone = message.text.lower()
    await state.update_data(contacts=user_phone)
    await message.answer(text="Завершить", reply_markup=fin())


@start_router.callback_query(F.data == 'Q7')
async def end(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    logging.info(f"Данные, которые будут отправлены (Регулировочная): {data}")   # Логируем данные перед отправкой

    user = {call.from_user.id: {key: (
        value if not isinstance(value, types.Location) else {"latitude": value.latitude, "longitude": value.longitude})
                                for key, value in data.items()}}

    # Создаем multipart/form-data
    async with ClientSession() as session:
        form_data = aiohttp.FormData()

        # Создаем JSON c геоданными
        geo_data = {
            "type": "Point",
            "coordinates": [
                user[call.from_user.id]['location']['latitude'],
                user[call.from_user.id]['location']['longitude']
            ]
        }

        # Создаем JSON данных для поля 'json'
        data_json = {
            'geo': geo_data,
            'city': user[call.from_user.id]['city'],
            'address': user[call.from_user.id]['address'],
            'description': user[call.from_user.id].get('description', ''),
            'contacts': {
                'email': user[call.from_user.id].get('email', ''),
                'whatsapp': user[call.from_user.id].get('whatsapp', ''),
                'telegram': user[call.from_user.id].get('telegram', ''),
                'phone': user[call.from_user.id].get('phone', '')
            },
        }

        # Добавляем его в form data
        form_data.add_field('json', json.dumps(data_json), content_type='application/json')

        # Добавляем графические файлы
        photos = data.get('photos', [])

        for idx, file_path in enumerate(photos):
            if idx < 5:  # Добавляем максимум 5 файлов
                form_data.add_field(f'file{idx + 1}', open(file_path, 'rb'), filename=os.path.basename(file_path))

        async with session.post('https://sf-hackathon.xyz/api/reports/new', data=form_data) as response:

            # body = await response.text() # для отладки
            if response.status == 201:
                await call.message.answer(text="Благодарим за создание заявки! \n"
                                               "Мы ценим ваше внимание!", reply_markup=f_s())
            else:
                await call.message.answer("Произошла ошибка при отправке данных на сервер. \n"
                                          "Воспользуйтесь кнопкой в левом нижнем углу")
                                          # F"Статус: {response.status}, Ответ: {body}") # для отладки

    await state.clear()
    await call.answer()

