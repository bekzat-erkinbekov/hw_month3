from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from config import bot, ADMINS
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.client_kb import start_markup, cancel_markup
from database.bot_db import sql_command_random
from parser.allcomics import parser
from parser.kaktus import new_parser
from config import PAYMENT
from aiogram.types.message import ContentType
async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id,  f'Hello, {message.from_user.first_name}',
                           reply_markup=start_markup)


    # await message.answer('This is answer method!')
    #
    # await message.reply('This is reply answer!')


async def quiz(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton('NEXT', callback_data='button_call_1')
    button_call_2 = InlineKeyboardButton('NEXT-2', callback_data='button_call_2')
    button_call_3 = InlineKeyboardButton('NEXT-3', callback_data='button_call_3')

    markup.add(button_call_1, button_call_2, button_call_3)


    question = "By whom invented Rust?"
    answers = [
        "Dennis Ritchie",
        "Graydon Hoare",
        "Guido Van Rossum",
        "Robert Griesemer",
    ]

    await bot.send_poll(
        message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Software developer Graydon Hoare created Rust as a personal project while working at Mozilla "
                    "Research in 2006.",
        open_period=120,
        reply_markup=markup,
    )

async def get_comic(message: types.Message):
    comics = parser()
    for i in comics:
        src = i['photo']
        await bot.send_photo(message.from_user.id,
            photo=src,
            caption=
            f"❤️Title: {i['title']}❤️\n\n"
            f"⭐️{i['rate']}⭐️\n"
            f"Link: {i['link']}"
        )

class FSMAdmin(StatesGroup):
    start = State()
    info = State()



async def start_kaktus(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.start.set()
        await message.answer("Начнем", reply_markup=cancel_markup)
    else:
        await message.answer("Пиши в личку!")

async def loading(message: types.Message):
    global news
    news = new_parser()
    for info in news:
        markup = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True).add(
            InlineKeyboardButton(text=f"Time: {info['time']}", callback_data=f'callback{info["time"]}')
        )
        await bot.send_message(message.from_user.id, info['title'], reply_markup=markup)
        await FSMAdmin.next()

async def sending(call: types.CallbackQuery):
    for i in news:
        src = i['photo']
        await bot.send_photo(call.from_user.id, photo=src, caption=
            f'Link: {i["link"]}\n\n'
            f'Title: {i["title"]}'
            )






# async def start_command(message: types.Message):
#     await message.answer_photo(open('/home/kuba/Pictures/shrek.jpeg', 'rb'), caption="Shrek")
#     await message.delete()
#
# async def start_command(message: types.Message):
#     await message.answer_photo(open('/home/kuba/Pictures/villager.jpeg', 'rb'), caption="MineVillagerStonks")
#     # await message.delete()
PRICE = types.LabeledPrice(label='Подписка на 1 месяц', amount=500*100)


async def buy(message: types.Message):
    await bot.send_message(message.chat.id, 'Тестовый платеж')

    await bot.send_invoice(message.chat.id,
                           title='Подписка на бота',
                           provider_token=PAYMENT,
                           currency='rub',
                           description='Активация',
                           photo_url='https://pythonru.com/wp-content/uploads/2018/12/random-module-icon.png',
                           photo_width=416,
                           photo_height=234,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter='one-month-sub',
                           payload='test-payload')

# async def pre_checkout_query(pre_check_q: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_check_q.id, ok=True)

async def success(message: types.Message):
    print('ПЛАТЕЖ УСПЕШНО ПРОВЕДЕН!')
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info:
        print(f'{k} = {v}')

    await bot.send_message(message.chat.id, f'Платеж на сумму{message.successful_payment.total_amount // 100} '
                                            f'{message.successful_payment.currency} проведен')

async def get_random_user(message: types.Message):
    await sql_command_random(message)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands='start')
    dp.register_message_handler(quiz, commands='quiz')
    dp.register_message_handler(get_random_user, commands=['get'])
    '''ДЗ'''
    dp.register_message_handler(get_comic, commands=['comic'])
    """Проблема с этим"""
    dp.register_message_handler(start_kaktus, commands=['kaktus'])
    dp.register_message_handler(loading, state=FSMAdmin.start)
    dp.register_callback_query_handler(sending,
                                       lambda call: call.data and call.data.startswith("Time: "), state=FSMAdmin.info)
    dp.register_message_handler(buy, commands=['buy'])
    # dp.pre_checkout_query_handlers(pre_checkout_query)
    dp.register_message_handler(success)