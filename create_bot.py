# from aiogram import Bot, Dispatcher
from motor import motor_asyncio
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import DB

# storage = MemoryStorage()
# bot = Bot(token=TOKEN_API)
# dp = Dispatcher(bot, storage=storage)
cluster = motor_asyncio.AsyncIOMotorClient(DB)
collection = cluster.main
