# Инициализация бота и диспетчера
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import API_TOKEN

#инициализация бота
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Подключение к базе данных
engine = create_engine("sqlite:///mydatabase.db", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Настройка логирования
logging.basicConfig(level=logging.INFO)