from Config import create_connection

async def get_free_messages(user_id):
    conn = await create_connection()
    free_messages_left = await conn.fetchval('SELECT free_messages_left FROM user_subscriptions WHERE user_id = $1', user_id)
    await conn.close()
    return free_messages_left

async def decrement_free_messages(user_id):
    conn = await create_connection()
    await conn.execute('UPDATE user_subscriptions SET free_messages_left = free_messages_left - 1 WHERE user_id = $1', user_id)
    await conn.close()

async def has_free_messages(user_id):
    free_messages_left = await get_free_messages(user_id)
    return free_messages_left > 0
