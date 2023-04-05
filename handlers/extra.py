from aiogram import types, Dispatcher
from config import bot, ADMINS
from random import choice


async def echo(message: types.Message):
    bad_words = ['сабина', 'алдияр', 'дурак', "дура", "сука", "бля", "наса"]
    username = f"@{message.from_user.username}" \
        if message.from_user.username is not None else message.from_user.first_name
    for word in bad_words:
        if word in message.text.lower().replace(' ', ''):
            # DRY - Don't Repeat Yourself
            await message.reply(f'Администраторы кикнуть его?')

    if message.from_user.id in ADMINS:
        emoji_list = ['⚽️', '🏀', '🎲', '🎰', '🎯', '🎳']
        emoji = choice(emoji_list)
        if message.text == 'game':
            await bot.send_dice(message.chat.id, emoji=emoji)


async def kick(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in ADMINS:
            await message.answer("Ты не мой босс!")
        elif not message.reply_to_message:
            await message.answer("Команда должны быть ответом на сообщение!")
        else:
            await bot.kick_chat_member(message.chat.id,
                                       message.reply_to_message.from_user.id)
            await message.answer(f"{message.from_user.first_name} братан кикнул "
                                 f"{message.reply_to_message.from_user.full_name}")

    else:
        await message.answer("Пиши в группу!")


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)