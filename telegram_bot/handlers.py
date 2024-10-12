import os

from aiogram.client.session import aiohttp
from aiohttp import ClientSession
from aiogram import Router, F, html, types, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from inline_kbs import ease_link_kb, kb2, kb1, fin, link_kb0, f_s, kbg

start_router = Router()


class SaveStatus(StatesGroup):  # состояния для заявки
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    Q8 = State()


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


@start_router.callback_query(F.data == 'stop_survey')  # реализация прерывания
async def stop_survey(call: types.CallbackQuery, state: FSMContext):
    # Очищаем данные из MemoryStorage
    await state.clear()  # Удаляем данные пользователя
    # Отправляем стартовое сообщение
    await call.message.answer("Опрос прерван. Выберите действие:", reply_markup=ease_link_kb())
    await call.answer()


# регистрация заявки
@start_router.callback_query(F.data == 'application')  # реакция на кнопку Создание заявки
async def send_photo(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Пожалуйста, загрузите фото люка вблизи 1 шт.\n"
                              "Фото люка с окрестностями 2 шт. \n"
                              "Фотографии загружать по одной.")
    await call.answer()
    await state.set_state(SaveStatus.Q1)


@start_router.message(SaveStatus.Q1)
async def handle_photo(message: types.Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    photos = data.get('photos', [])  # Используем .get() для безопасного доступа
    photo = message.photo[-1]  # Берем фотографию наивысшего качества

    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    file_path = os.path.join('photos', f"{file_id}.jpg")

    await message.bot.download_file(file.file_path, file_path)  # Сохраняем фотографию на сервер
    photos.append(file_path)

    await state.update_data(photos=photos)  # Обновляем данные состояния

    if len(photos) < 3:
        await message.delete()
        media_group = []
        for photo in photos:
            media_group.append(InputMediaPhoto(media=photo))
        
        await bot.send_media_group(chat_id=message.chat.id,
                                media=media_group)
    else:
        # Если три фотографии получены
        await message.answer("Пожалуйста включите определение местоположения", reply_markup=kbg())


@start_router.callback_query(F.data == 'kb_geo')  # Создание кнопки для получения координат
async def send_geo(call: types.CallbackQuery,  state: FSMContext):
    button_geo = [[KeyboardButton(text="Отправить свою геолокацию", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard=button_geo, resize_keyboard=True)  # создаем простую кнопку
    await call.message.answer("Нажмите кнопку внизу", reply_markup=reply_markup)
    await call.answer()
    await state.set_state(SaveStatus.Q2)


@start_router.message(F.content_type == types.ContentType.LOCATION, SaveStatus.Q2)  # обработка координат
async def location_handler(message: types.Message, state: FSMContext):
    await state.update_data(location=message.location)
    await message.answer(text="Спасибо!", reply_markup=types.ReplyKeyboardRemove())  # удаляем простую кнопку
    await message.answer(text="В каком вы городе?", reply_markup=link_kb0())
    await state.set_state(SaveStatus.Q3)  # изменение статуса


@start_router.message(SaveStatus.Q3)
async def send_address(message: types.Message, state: FSMContext):
    user_city = message.text.lower()  # получаем город от пользователя
    await state.update_data(city=user_city)  # сохраняем город в состоянии
    await message.answer(text="Адрес ближайшего здания", reply_markup=link_kb0())
    await state.set_state(SaveStatus.Q4)  # Переход к следующему вопросу


@start_router.message(SaveStatus.Q4)  # Переводим инлин кнопку в обычную
async def send_geo(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.lower())  # сохраняем адрес в состоянии
    await message.answer(text='Опишите проблему (необязательно)', reply_markup=kb1())
    await state.set_state(SaveStatus.Q5)


@start_router.callback_query(F.data == 'Q5')  # Если это вызов через кнопку
async def send_description(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Ваши контакты: whatsapp, telegramm, email, phone  (не обязательно)',
                                        reply_markup=kb2())
    await callback_query.answer()
    await state.set_state(SaveStatus.Q6)


@start_router.message(SaveStatus.Q5)  # Если это вызов через текстовое сообщение
async def send_contacts(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text.lower())
    await message.answer(text="Ваши контакты: whatsapp, telegramm, email, phone (не обязательно)", reply_markup=kb2())
    await state.set_state(SaveStatus.Q6)


@start_router.message(SaveStatus.Q6)  # Если это вызов через текстовое сообщение
async def send_end(message: types.Message, state: FSMContext):
    await state.update_data(contacts=message.text.lower())
    await message.answer(text="Завершить", reply_markup=fin())
    await state.set_state(SaveStatus.Q7)


@start_router.callback_query(F.data == 'Q6')
async def send_description(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text="Завершить", reply_markup=fin())
    await callback_query.answer()
    await state.set_state(SaveStatus.Q7)


@start_router.callback_query(F.data == 'Q7')
async def end(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user = {call.from_user.id: {key: (
        value if not isinstance(value, types.Location) else {"latitude": value.latitude, "longitude": value.longitude})
                                for key, value in data.items()}}
    text = [f'{key}: {value}\n' for key, value in data.items()]

    await call.message.answer(text="Ваша заявка создана!", reply_markup=f_s())  # спросить у дизайнеров как написать благодарность

    # Создаем multipart/form-data

    async with ClientSession() as session:
        form_data = aiohttp.FormData()
        for key, value in user[call.from_user.id].items():
            if isinstance(value, dict):
                form_data.add_field(key + '[latitude]', value['latitude'])
                form_data.add_field(key + '[longitude]', value['longitude'])
            else:
                form_data.add_field(key, value)

        async with session.post('YOUR_ENDPOINT_URL', data=form_data) as response:   # не забыть вписать адрес
            if response.status == 200:
                await call.message.answer("Заявка успешно отправлена на сервер!")
            else:
                await call.message.answer("Произошла ошибка при отправке данных на сервер.")

    await state.clear()
    await call.answer()

  # multipart/form-data запрос