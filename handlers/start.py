from aiogram import Dispatcher, types
from database import UserController
# from handlers import timer, registration
from config import MENU_TEXT, COLLECTION_ID_FOR_MESSAGE, REGISTATION_LINK
# from create_bot import bot
from keyboards import kb_main, kb_make_appointment
from aiogram import Bot
from config import TOKENS

async def start_command(message: types.Message):
    auth = await UserController.check_auth_user(message.from_user.id)
    bots = [Bot(token) for token in TOKENS]
    for bot in bots:
        bot_info = await bot.get_me()
    
    if (auth):
        await message.answer('Куда направимся?😚', reply_markup=kb_main)
        
    if not(auth):
        url_id = message.get_args()
        find_url_id = await UserController.find_url_id(url_id)
        
        print(REGISTATION_LINK, url_id)
        if REGISTATION_LINK == url_id:
            print('Вход есть - ', url_id)
            # return await registration.start_command(message)
        
        if find_url_id:
            user = { 'username': message.from_user.username, 'firstName': message.from_user.first_name, 'lastName': message.from_user.last_name, 'telegramId': message.from_user.id }
            updata_patient_is_url = await UserController.updata_patient_is_url(user, url_id)
            push_user_id_to_collection = await UserController.push_user_id_to_collection(url_id)
            
            if updata_patient_is_url and push_user_id_to_collection: 
                await message.answer('Вы успешно авторизовались!', reply_markup=kb_main)
                find_collection_in_user = await UserController.check_on_collection(url_id, COLLECTION_ID_FOR_MESSAGE)
                # Только для коллекции персональное сообщение
                if find_collection_in_user:
                    await message.answer('Здравствуйте!\nВас приветствует чатбот заботы Alma clinic 👋\n\nМеня создали руководители клиники, чтобы быть ближе к каждому пациенту ❤️\n\nМы заботимся о здоровье и красоте наших пациентов и хотим контролировать качество лечения и сервис нашей клиники.\nА также мы хотим радовать вас персональными подарками и акциями ❤️')
                    await message.answer('В благодарность за выбор нашей клиники мы дарим вам подарок -\n🎁бесплатную процедуру лазерной эпиляции (зона подмышек)\n\nПромокод подарка LetoAlma2023 (скажите администратору клиники при записи на процедуру)\n*акция действует до 31.08.2023\n\nЧтобы получить бесплатную процедуру вы можете записаться на прием в разделе «Информация о клинике» ✅')
                else:
                    bots = [Bot(token) for token in TOKENS]
                    for bot in bots:
                        await bot.send_message(message.chat.id, f'Вас приветствует чат заботы клиники <b>{bot_info.first_name}</b>👋\n\nЯ буду вашим гидом по клинике🤗', parse_mode="html")
                # Выводим все приветсвенные сообщения
                # await timer.scheduled_job('now')
            else: 
                await message.answer('При авторизации произошла ошибка, попробуйте ещё раз!')

        else:    
            bots = [Bot(token) for token in TOKENS]
            for bot in bots:
                await bot.send_message(message.chat.id, f'Вас приветствует чат заботы клиники <b>{bot_info.first_name}</b>👋\n\nЯ буду вашим гидом по клинике. В данный момент, вы не являетесь пациентом нашей клиники, но вы можете записаться на прием!🤗', reply_markup=kb_make_appointment , parse_mode="html")
            # await bot.send_sticker(chat_id=message.from_user.id, sticker=r"CAACAgIAAxkBAAEJRl9khLELI79VGUQdcVIr8hMS-nLDRgACWAQAAsxUSQk3DsXJLeC4fC8E")
    await message.delete()
    
async def main_command(message: types.Message):
    auth = await UserController.check_auth_user(message.from_user.id)
    if auth: await message.answer(MENU_TEXT, reply_markup=kb_main)
    else: await message.answer('Для перехода в главное меню, вы должны быть авторизованны')
    await message.delete()


async def help_command(message: types.Message):
    await message.answer(text='<b>Список команд:\n</b>/start - начало работы\n/main - вернуться на главную страницу\n/help - список команд', parse_mode='html')
    await message.delete()


def register_handlers_start(dp: Dispatcher):
    dp.message.register(start_command, commands=["start"])
    dp.message.register(main_command, commands=["main"])
    dp.message.register(help_command, commands=['help'])
