from aiogram import Dispatcher, types
from config import MENU_TEXT
from keyboards import kb_main


async def zero_text(message: types.Message):
    await message.answer('Я тебя не понимаю😩')


async def back_main_text(message: types.Message):
    await message.answer(MENU_TEXT, reply_markup=kb_main)


def register_handlers_other(dp: Dispatcher):
    dp.message.register(back_main_text, text=['Вернуться в главное меню'])
    dp.message.register(zero_text)
    