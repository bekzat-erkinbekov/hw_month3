from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from uuid import uuid4
from database.bot_db import sql_command_insert
from keyboards.client_kb import submit_markup, cancel_markup, direction_markup
from config import ADMINS

class FSMAdmin(StatesGroup):
    id = State()
    name = State()
    direction = State()
    age = State()
    mgroup = State()
    submit = State()

async def fsm_start(message: types.Message):
    if message.chat.type == 'private' and message.chat.id in ADMINS:
        await FSMAdmin.id.set()
        await message.answer(f"ID Ментора был загружен в БД. Давайте продолжим?", reply_markup=submit_markup)
    else:
        await message.answer("Убедитесь в том что вы являетесь Администратором "
                             "или пишите ли в ЛС?")


async def load_id(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        mentors_id = str(uuid4())
        async with state.proxy() as data:
            # Проверка в БД на сходство id если есть сходство запустить еще раз (64 000 000 айдишек)
            data['id'] = mentors_id
        await FSMAdmin.next()
        await message.answer("Как зовут ментора?")
    elif message.text.lower() == "нет":
        await state.finish()
    else:
        await message.answer("Нипонял!?")

async def load_name(message: types.Message, state: FSMContext):
    num = False
    for numbers in message.text:
        if numbers.isdigit():
            num = True

    if num == False:
        async with state.proxy() as data:
            data['name'] = message.text
            await FSMAdmin.next()
            await message.answer('Направление?', reply_markup=direction_markup)
    else:
        await message.answer('Убедитесь что в имени нет чисел')


async def load_direction(message: types.Message, state: FSMContext):
    check = False
    for dictionary in direction_markup['keyboard'][0]:
        for k, i in dictionary:
            if i == message.text.upper():
                check = True
    if check == True:
        async with state.proxy() as data:
            data['direction'] = message.text
        await FSMAdmin.next()
        await message.answer('Сколько лет ментору?', reply_markup=cancel_markup)
    else:
        await message.answer('Убедитесь что направление выбрано правильно')

async def load_age(message: types.Message, state: FSMContext):
    try:
        if int(message.text) <= 0:
            await message.answer("Только положительные числа!")
        else:
            if 14 < int(message.text) < 50:
                async with state.proxy() as data:
                    data['age'] = message.text
                await FSMAdmin.next()
                await message.answer('Группа?', reply_markup=cancel_markup)
            else:
                await message.answer("Доступ воспрещен!")
    except ValueError:
        await message.answer("Числа брат, числа")
async def load_mgroup(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mgroup'] = message.text
        python_photo = open('media/pythonlogo.jpg', 'rb')
        designer_photo = open('media/uxuilogo.jpg', 'rb')
        js_photo = open('media/JavaScript-logo.png', 'rb')
        java_photo = open('media/javalogo.png', 'rb')
        caption = f'''
        ID: {data['id']}, \n
Name: {data['name']}, \n
Direction: {data['direction']}, \n
Age: {data['age']}, \n
Group: {data['mgroup']}
                '''

        if data['direction'] == 'BACKEND':
            await message.answer_photo(photo=python_photo, caption=caption)
        elif data['direction'] == 'FRONTEND':
            await message.answer_photo(photo=js_photo, caption=caption)
        elif data['direction'] == 'ANDROID':
            await message.answer_photo(photo=java_photo, caption=caption)
        else:
            await message.answer_photo(photo=designer_photo, caption=caption)


        await FSMAdmin.next()
        await message.answer("Все верно?", reply_markup=submit_markup)

async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await sql_command_insert(state)
        await state.finish()
    elif message.text.lower() == "нет":
        await state.finish()
    else:
        await message.answer("Нипонял!?")

async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Cancled")

def register_handlers_mentor(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_reg,
                                Text(equals='cancel', ignore_case=True),
                                state='*')

    dp.register_message_handler(fsm_start, commands=['register'])
    dp.register_message_handler(load_id, state=FSMAdmin.id)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_mgroup, state=FSMAdmin.mgroup)
    dp.register_message_handler(submit, state=FSMAdmin.submit)