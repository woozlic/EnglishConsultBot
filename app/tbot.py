import logging

from aiogram import Bot, Dispatcher, types
from config import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_API_KEY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help', 'q'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Echo")
