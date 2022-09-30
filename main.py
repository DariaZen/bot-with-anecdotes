import logging
from aiogram import Bot, Dispatcher, executor, types
import random
import sqlite3


bot = Bot(token='') #here must be a token
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

topics_numbers = []
for i in range(1, 30):
    topics_numbers.append(str(i))


@dp.message_handler(commands=['start'])
async def start_command(message):
    text = ''
    f = open('start.txt', 'r')
    for line in f:
        text += line
    f.close()
    await message.reply(text)
    return


@dp.message_handler(commands=topics_numbers)
async def print_anecdote(message):
    db = sqlite3.connect('anecdotes.db')
    cur = db.cursor()
    record = message['text'][1:]
    cur.execute('SELECT * FROM anecdotes WHERE topic='+record)
    rows = cur.fetchall()
    ids = []
    for row in rows:
        id, topic, text = row
        ids.append(id)
    if len(ids) > 0:
        cur = db.cursor()
        record = str(random.choice(ids))
        cur.execute('SELECT * FROM anecdotes WHERE id='+record)
        row = cur.fetchone()
        id, topic, text = row
        await bot.send_message(message.from_user.id, text)
        f = open('help.txt', 'r')
        for line in f:
            await bot.send_message(message.from_user.id, line)
        f.close()
    db.close()
    return


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
