import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from config import API_TOKEN
from aiogram.dispatcher.filters.state import State, StatesGroup

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Подключение к базе данных
engine = create_engine("sqlite:///mydatabase.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Модель данных для пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

class RegisterState(StatesGroup):
    name = State()
    age = State()

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)