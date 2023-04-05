from aiogram import types, Dispatcher
from config import bot, ADMINS
from database.bot_db import sql_command_all, sql_command_delete
import random
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def dice_game(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer('Ur turn:')
        users_points = await bot.send_dice(message.chat.id)
        await message.answer('And my turn:')
        bots_points = await bot.send_dice(message.chat.id)
        if users_points.dice.value > bots_points.dice.value:
            await message.answer('U won!')
        elif users_points.dice.value < bots_points.dice.value:
            await message.answer('I won!')
        else:
            await message.answer('MEH')

async def ban(message: types.Message):
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

async def delete_data(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Ты не мой босс!")
    else:
        users = await sql_command_all()
        random_user = random.choice(users)
        await bot.send_message(
            message.from_user.id,
            text=f"ID: {random_user[1]},\nDirection: {random_user[3]},\nAge:{random_user[4]} "
                 f"\n\n{random_user[2]}",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"delete {random_user[2]}",
                                     callback_data=f"delete {random_user[2]}")
            )
        )
async def pin(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in ADMINS:
            await message.answer("Ты не мой босс!")
        elif not message.reply_to_message:
            await message.answer("Команда должны быть ответом на сообщение!")
        else:
            await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    else:
        await message.answer("Пиши в группу!")

async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text="Удалено", show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!/')
    dp.register_message_handler(dice_game, commands=['dice'], commands_prefix='!/')
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete "))