from aiogram import Dispatcher, types
from database import UserController
from keyboards import kb_make_appointment, kb_back_main
# from create_bot import bot


async def auth_check(message: types.Message):
    isActive = await UserController.check_auth_user(message.from_user.id)
    if not (isActive):
        await message.answer('Вы не загеристрированны, чтобы зареситрироваться напишите команду: /start')
        return
    
    clinic = await UserController.get_contact_hospital()
    await UserController.send_statistics_info()

    await message.answer(clinic['description'], reply_markup=kb_make_appointment)

async def make_appointment_text(message: types.Message):
    res = await UserController.find_hospital()
    if res == False or res == None:
        await message.answer('Что-то пошло не так, свяжитесь с администратором клиники @mikhnusha', reply_markup=kb_back_main)
    contact = res['contact']
    
    auth = await UserController.check_auth_user(message.from_user.id)
    
    if auth:
        await UserController.send_statistics_entry()
        
        await message.answer(f'Контактные данные клиники:\n\n{contact}', reply_markup=kb_back_main)
    else:
        await message.answer(f'Записывайся к нам, мой дорогой друг, и мы увидимся снова❤️\nКонтактные данные клиники:\n\n{contact}', reply_markup=types.ReplyKeyboardRemove())
        # await bot.send_sticker(chat_id=message.from_user.id, sticker=r"CAACAgIAAxkBAAEJRlhkhLDEdirIFuVxHYXiMG8Z_AABRxcAAlYEAALMVEkJKT4bIPWet58vBA")

def register_handlers_info(dp: Dispatcher):
    dp.message.register(auth_check, text=["Информация о клинике"])
    dp.message.register(make_appointment_text, text=["Запись на прием"])