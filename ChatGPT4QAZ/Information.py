from aiogram import types
from Config import dp, bot, UserState, create_connection
from Keyboards import information_kb

async def information(chat_id):
    await bot.send_message(chat_id, text="Задайте информацию, которую будет учитывать чат GPT", reply_markup=information_kb)

@dp.message_handler(lambda message: message.text == "Посмотреть пример💡", state=UserState.information)
async def example(message: types.Message):
    await bot.send_message(message.chat.id, "Меня зовут Дария, мне 25 лет, я увлекаюсь игрой на фортепиано, а также люблю рисовать. Я уже несколько недель слежу за одной вакансией и они наконец-то меня пригласили на собеседование, дату еще не назначали, но я очень жду и волнуюсь. Возможно мне устроят какой то тест, поэтому я бы хотела подтянуть свои знания в сфере бухгалтерского учета")


@dp.message_handler(lambda message: message.text == "Действующая информация✅", state=UserState.information)
async def current_information(message: types.Message):
    user_id = message.from_user.id
    conn = await create_connection()
    information = await conn.fetchval('SELECT information FROM user_settings WHERE user_id = $1', user_id)
    await conn.close()
    if information:
        await bot.send_message(message.chat.id, f"Действующая информация: {information}")
    else:
        await bot.send_message(message.chat.id, "Информация не задана")


@dp.message_handler(lambda message: message.text == "Сбросить информацию❌", state=UserState.information)
async def reset_information(message: types.Message):
    user_id = message.from_user.id
    conn = await create_connection()
    await conn.execute("UPDATE user_settings SET information = NULL WHERE user_id = $1", user_id)
    await conn.close()
    await bot.send_message(message.chat.id, "Информация сброшена, чтобы изменения вступили в силу нужно начать новый диалог")


@dp.message_handler(state=UserState.information)
async def set_information(message: types.Message):
    user_id = message.from_user.id
    information = message.text
    conn = await create_connection()
    await conn.execute('''
        INSERT INTO user_settings (user_id, information) 
        VALUES ($1, $2) 
        ON CONFLICT (user_id) DO UPDATE SET information = $2
    ''', user_id, information)
    await conn.close()
    await bot.send_message(message.chat.id, "Информация применена, чтобы ее использовать нужно начать новый диалог")
