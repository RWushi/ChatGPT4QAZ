from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from datetime import datetime, timezone
import json
from Config import dp, bot, create_connection, UserState
from Keyboards import prechat_kb


async def save_history(user_id, history):
    history_str = json.dumps(history)

    conn = await create_connection()
    await conn.execute('''
        INSERT INTO user_settings (user_id, chat_history) 
        VALUES ($1, $2) 
        ON CONFLICT (user_id) DO UPDATE SET chat_history = $2
    ''', user_id, history_str)
    await conn.close()

async def reset_history(user_id):
    empty_history = json.dumps([])

    conn = await create_connection()
    await conn.execute('''
        UPDATE user_settings SET chat_history = $1 WHERE user_id = $2
    ''', empty_history, user_id)
    await conn.close()


async def get_user_data(user_id):
    conn = await create_connection()
    row = await conn.fetchrow('SELECT chat_history, style, information FROM user_settings WHERE user_id = $1', user_id)
    await conn.close()

    if row is None:
        return None, None, None

    history = json.loads(row['chat_history']) if row['chat_history'] else []

    return history, row['style'], row['information']

async def get_free_messages(user_id):
    conn = await create_connection()
    free_messages_left = await conn.fetchval('SELECT free_messages_left FROM user_subscriptions WHERE user_id = $1', user_id)
    await conn.close()
    return free_messages_left

async def decrement_free_messages(user_id):
    conn = await create_connection()
    await conn.execute('UPDATE user_subscriptions SET free_messages_left = free_messages_left - 1 WHERE user_id = $1', user_id)
    await conn.close()

async def has_free_messages(user_id, message):
    free_messages_left = await get_free_messages(user_id)
    if free_messages_left > 0:
        return True
    else:
        await message.answer("У вас закончились бесплатные запросы. Вы можете обратиться в поддержку или оплатить подписку")
        return False

async def pre_check_vip(user_id, message):
    conn = await create_connection()
    end_date = await conn.fetchval('SELECT subscription_end_date FROM user_subscriptions WHERE user_id = $1', user_id)
    await conn.close()

    if end_date is None:
        await message.answer("Для доступа к VIP чату💎 Вам нужно приобрести подписку")
        return False

    if datetime.now(timezone.utc) > end_date:
        await message.answer("Срок действия Вашей подписки истек. Для доступа к VIP чату💎 Вам нужно ее обновить")
        return False

    return True

async def pre_check_free(user_id, message):
    conn = await create_connection()
    end_date = await conn.fetchval('SELECT subscription_end_date FROM user_subscriptions WHERE user_id = $1', user_id)
    await conn.close()

    if end_date is not None and datetime.now(timezone.utc) <= end_date:
        await message.answer("У Вас есть активная подписка, воспользуйтесь VIP чатом💎")
        return False
    return True


async def expired(user_id):
    conn = await create_connection()
    current_state = await conn.fetchval('SELECT user_state FROM user_settings WHERE user_id = $1', user_id)
    await conn.close()

    if current_state == 'UserState:chatvip':
        await dp.current_state(chat=user_id).set_state(UserState.prechat.state)
        await bot.send_message(user_id, text="Срок действия Вашей подписки истек. Обновите подписку для доступа к VIP чату💎 или можете пользоваться бесплатными запросами", reply_markup=prechat_kb)
    else:
        await bot.send_message(user_id, text="Срок действия Вашей подписки истек. Обновите подписку для доступа к VIP чату💎 или можете пользоваться бесплатными запросами")

async def check_subscription_daily():
    conn = await create_connection()
    user_list = await conn.fetch('SELECT user_id FROM user_subscriptions WHERE subscription_end_date < $1', datetime.now(timezone.utc))
    await conn.close()

    for record in user_list:
        user_id = record['user_id']
        await expired(user_id)


scheduler = AsyncIOScheduler()
scheduler.add_job(check_subscription_daily, 'cron', hour=0, minute=0, timezone=utc)
scheduler.start()
