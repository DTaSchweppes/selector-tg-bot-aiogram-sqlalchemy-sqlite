from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State

from configuration import dp

class WaitForChooseParsersState(StatesGroup):
    parser = State()
@dp.message_handler(Command("parsers"))
async def cmd_register(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['ETM', 'В разработке', 'В разработке']
    keyboard.add(*buttons)
    await WaitForChooseParsersState.next()
    await message.answer('Можно воспользоваться парсерами:', reply_markup=keyboard)

@dp.message_handler(state=WaitForChooseParsersState.parser)
async def cmd_register(message: types.Message, state: FSMContext):
    if message.text == 'ETM':
        print('какая-то логика')

    await message.answer("Парсер отработал данные в БД!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()