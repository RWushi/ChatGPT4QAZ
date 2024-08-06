from aiogram import types
from Config import dp, bot, UserState, create_connection
from Keyboards import style_kb

async def style(chat_id):
    await bot.send_message(chat_id, text="Задайте стиль, в котором будет общаться чат GPT", reply_markup=style_kb)

@dp.message_handler(lambda message: message.text == "Посмотреть пример💡", state=UserState.style)
async def example(message: types.Message):
    await bot.send_message(message.chat.id, "Ты мой лучший друг, тебя зовут Алексей, мы с тобой знакомы со школы и ты занимаешься боксом уже 10 лет. Ты немного грубоват, но  зато всегда меня поддерживаешь и смеешься над моими шутками, даже если они не смешные. Тебе 35 лет и ты живешь в Баку, тебе очень нравится этот город. Сейчас я хочу, чтобы ты помог мне с моими курсами по английскому на тему Present Simple.")

@dp.message_handler(lambda message: message.text == "Действующий стиль✅", state=UserState.style)
async def current_style(message: types.Message):
    user_id = message.from_user.id
    conn = await create_connection()
    style = await conn.fetchval('SELECT style FROM user_settings WHERE user_id = $1', user_id)
    await conn.close()
    if style and style[0]:
        await bot.send_message(message.chat.id, f"Действующий стиль: {style}")
    else:
        await bot.send_message(message.chat.id, "Стиль не задан")


@dp.message_handler(lambda message: message.text == "Сбросить стиль❌", state=UserState.style)
async def reset_style(message: types.Message):
    user_id = message.from_user.id
    conn = await create_connection()
    await conn.execute("UPDATE user_settings SET style = NULL WHERE user_id = $1", user_id)
    await conn.close()
    await bot.send_message(message.chat.id, "Стиль сброшен, чтобы изменения вступили в силу нужно начать новый диалог")


@dp.message_handler(state=UserState.style)
async def set_style(message: types.Message):
    user_id = message.from_user.id
    style = message.text
    conn = await create_connection()
    await conn.execute('''
        INSERT INTO user_settings (user_id, style) 
        VALUES ($1, $2) 
        ON CONFLICT (user_id) DO UPDATE SET style = $2
    ''', user_id, style)
    await conn.close()
    await bot.send_message(message.chat.id, "Стиль применен, чтобы его использовать нужно начать новый диалог")