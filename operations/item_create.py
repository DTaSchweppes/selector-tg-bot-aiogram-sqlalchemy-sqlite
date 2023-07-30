from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from configuration import dp, session, Base, engine
from models.item import Item
from models.vendor import Vendor


class ItemCreateState(StatesGroup):
    name = State()
    brand = State()
    vendor_id = State()


@dp.message_handler(Command("item_create"))
async def cmd_register(message: types.Message):
    #Base.metadata.create_all(bind=engine)

    await message.answer("💼Создание карточки товара. Введите наименование товара:")
    await ItemCreateState.next()


@dp.message_handler(state=ItemCreateState.name)
async def process_register_name(message: types.Message, state: FSMContext):
    name = message.text

    async with state.proxy() as data:
        data["name"] = name

    await message.answer("Введите наименование бренда")
    await ItemCreateState.next()


@dp.message_handler(state=ItemCreateState.brand)
async def process_register_name(message: types.Message, state: FSMContext):
    brand = message.text

    async with state.proxy() as data:
        data["brand"] = brand

    await message.answer("Введите наименование поставщика")
    await ItemCreateState.next()


@dp.message_handler(state=ItemCreateState.vendor_id)
async def process_register_age(message: types.Message, state: FSMContext):
    vendor_name = message.text

    async with state.proxy() as data:
        vendor = session.query(Vendor).filter(Vendor.name == vendor_name).first()
        if not vendor:
            await message.answer("⚠️Данный поставщик не найден в базе!")
        else:
            data["vendor_id"] = vendor.id
            new_item = Item(name=data["name"], brand=data["brand"],
                            vendor_id=data["vendor_id"])
            session.add(new_item)
            session.commit()
            session.close()

            await state.finish()

            await message.answer("Новый товар занесен в базу!✅")