from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from configuration import dp, Session
from models.vendor import Vendor


class VendorCreateState(StatesGroup):
    name = State()
    address = State()
    category = State()
    rating = State()


@dp.message_handler(Command("vendor_create"))
async def cmd_register(message: types.Message):
    await message.answer("📦Создание карточки поставщика. Введите наименование поставщика.")
    await VendorCreateState.next()


@dp.message_handler(state=VendorCreateState.name)
async def process_register_name(message: types.Message, state: FSMContext):
    name = message.text

    async with state.proxy() as data:
        data["name"] = name

    await message.answer("Введите адрес поставщика")
    await VendorCreateState.next()


@dp.message_handler(state=VendorCreateState.address)
async def process_register_name(message: types.Message, state: FSMContext):
    address = message.text

    async with state.proxy() as data:
        data["address"] = address

    await message.answer("Введите наименование категории")
    await VendorCreateState.next()


@dp.message_handler(state=VendorCreateState.category)
async def process_register_name(message: types.Message, state: FSMContext):
    category = message.text

    async with state.proxy() as data:
        data["category"] = category

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Высокий', 'Средний', 'Низкий']
    keyboard.add(*buttons)
    await message.answer("Выберите рейтинг",reply_markup=keyboard)
    await VendorCreateState.next()


@dp.message_handler(state=VendorCreateState.rating)
async def process_register_age(message: types.Message, state: FSMContext):
    rating = message.text

    async with state.proxy() as data:
        data["rating"] = rating

        session = Session()
        new_vendor = Vendor(address=data["address"], name=data["name"],
                            category=data["category"], rating=data["rating"])
        session.add(new_vendor)
        session.commit()
        session.close()

    await state.finish()

    await message.answer("Новый поставщик занесен в базу!✅", reply_markup=types.ReplyKeyboardRemove())
