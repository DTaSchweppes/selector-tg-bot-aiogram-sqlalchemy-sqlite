from operations.parsers import dp

if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)