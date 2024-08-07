from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from States import PostgresStateStorage
import asyncpg


DATABASE_CONFIG = {
    'host': '',
    'database': '',
    'user': '',
    'password': '',
    'port': '5432',
    'ssl': 'require'
}


async def create_connection():
    return await asyncpg.connect(**DATABASE_CONFIG)


async def add_new_user(user_id):
    conn = await create_connection()

    await conn.execute('''
        INSERT INTO user_settings (user_id, style, chat_history, information) 
        VALUES ($1, NULL, NULL, NULL) ON CONFLICT (user_id) DO NOTHING
    ''', user_id)

    await conn.execute('''
        INSERT INTO user_subscriptions (user_id, free_messages_left, subscription_end_date) 
        VALUES ($1, 2, NULL) ON CONFLICT (user_id) DO NOTHING
    ''', user_id)

    await conn.close()


class UserState(StatesGroup):
    menu = State()
    prechat = State()
    chatfree = State()
    chatvip = State()
    customization = State()
    about = State()
    usage = State()
    payment = State()
    style = State()
    information = State()

bot = Bot(token='')
storage = PostgresStateStorage(**DATABASE_CONFIG)
dp = Dispatcher(bot, storage=storage)

OPENAI_API_KEY = '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'

