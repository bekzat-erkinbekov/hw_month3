# SQL - Structured Query Language
# СУБД - Система Управления Базой Данных
# CRUD = Create Read Update Delete
import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS anketa "
               "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "tid VARCHAR (255), "
               "name VARCHAR (255), "
               "direction VARCHAR (255), "
               "age INTEGER, "
               "mgroup VARCHAR (255))")

    db.commit()

async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO anketa(tid, name, direction, age, mgroup) VALUES (?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM anketa").fetchall()
    random_user = random.choice(result)
    await bot.send_message(
        message.from_user.id,
        text=f"ID: {random_user[1]},\nDirection: {random_user[3]},\nAge:{random_user[4]} "
                f"\n\n{random_user[2]}"
    )


async def sql_command_all():
    return cursor.execute("SELECT * FROM anketa").fetchall()


async def sql_command_delete(user_id):
    cursor.execute("DELETE FROM anketa WHERE id = ?", (user_id,))
    db.commit()