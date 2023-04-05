import aioschedule
from aiogram import types, Dispatcher
from config import bot
import asyncio


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = []
    chat_id.append(message.from_user.id)
    await message.answer("Ok")


async def go_to_gym():
    for id in chat_id:
        await bot.send_message(id, "GO GO GO GO!")


async def club():
    for id in chat_id:
        await bot.send_message(id, "WELLCOME TO THE CLUB")


async def scheduler():
    aioschedule.every().thursday.at('17:25').do(club)
    aioschedule.every().thursday.at('17:44').do(go_to_gym)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def register_handler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id, lambda word: 'напомни' in word.text)