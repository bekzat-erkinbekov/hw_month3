from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = config('TOKEN')
PAYMENT = config('PAYMENTS_TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
ADMINS = (1180795329, 933132682)