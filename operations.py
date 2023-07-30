from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from configuration import dp, Base, engine, Session
from models.user import User


class RegisterState(StatesGroup):
    name = State()
    age = State()

# Обработчик команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    # Создание таблицы пользователей в базе данных, если она ещё не создана
    Base.metadata.create_all(bind=engine)

    await message.reply("Приветствуем в системе для работы с поставщиками SELECTOR.")


# Обработчик команды /register
@dp.message_handler(Command("register"))
async def cmd_register(message: types.Message):
    await message.answer("Нужно пройти небольшую регистрацию! Введите ваше имя.")
    await RegisterState.next()


# Обработчик состояния RegisterState.name
@dp.message_handler(state=RegisterState.name)
async def process_register_name(message: types.Message, state: FSMContext):
    name = message.text

    async with state.proxy() as data:
        data["name"] = name

    await message.answer("Введите ваш возраст.")
    await RegisterState.next()


# Обработчик состояния RegisterState.age
@dp.message_handler(state=RegisterState.age)
async def process_register_age(message: types.Message, state: FSMContext):
    age = message.text

    async with state.proxy() as data:
        data["age"] = age

        # Сохранение нового пользователя в базе данных
        session = Session()
        new_user = User(name=data["name"], age=data["age"])
        session.add(new_user)
        session.commit()
        session.close()

    await state.finish()

    await message.answer("Регистрация успешно завершена!")
