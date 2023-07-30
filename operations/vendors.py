from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from configuration import dp, Session, bot, session
from models.vendor import Vendor


@dp.message_handler(commands=["vendors"], state="*")
async def show_vendors_page(message: types.Message, state: FSMContext):
    # Получение текущей страницы из состояния пользователя (если сохранено)
    current_page = await state.get_state()

    # Если текущая страница не задана, установите ее на 1
    if not current_page:
        current_page = 1

    # Запрос к базе данных для получения записей с пагинацией
    per_page = 5  # Количество записей на странице
    offset = (current_page - 1) * per_page  # Смещение записей
    vendors = session.query(Vendor).limit(per_page).offset(offset).all()

    # Создание сообщения с информацией о поставщиках
    response_message = "Список поставщиков:\n"
    for vendor in vendors:
        response_message += f"📦Наименование: {vendor.name}\n" \
                            f"🌐Адрес: {vendor.address}\n" \
                            f"💼Категория: {vendor.category}\n" \
                            f"⬆️Рейтинг: {vendor.rating}\n\n"

    # Создание клавиатуры для пагинации
    keyboard = InlineKeyboardMarkup(row_width=2)
    previous_button = InlineKeyboardButton("Предыдущая", callback_data="previous_page")
    next_button = InlineKeyboardButton("Следующая", callback_data="next_page")
    keyboard.add(previous_button, next_button)

    # Отправка сообщения с информацией о поставщиках и клавиатурой пагинации
    await message.answer(response_message, reply_markup=keyboard)
@dp.callback_query_handler(lambda c: c.data in ["previous_page", "next_page"],
                                       state="*")
async def handle_pagination_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    # Получение данных о нажатой кнопке
    button = callback_query.data

    # Получение текущей страницы из состояния пользователя
    current_page = int(await state.get_state())

    if button == "previous_page":
        # Если была нажата кнопка "Предыдущая", уменьшите номер текущей страницы на 1
        current_page -= 1
    elif button == "next_page":
        # Если была нажата кнопка "Следующая", увеличьте номер текущей страницы на 1
        current_page += 1

    # Сохранение новой текущей страницы в состояние пользователя
    await state.set_state(str(current_page))

    # Обновление сообщения с информацией о поставщиках и клавиатуры пагинации
    vendors_message_id = callback_query.message.message_id
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=vendors_message_id,
                                text="Загрузка...", reply_markup=None)
    await show_vendors_page(callback_query.message, state)

    await callback_query.answer()