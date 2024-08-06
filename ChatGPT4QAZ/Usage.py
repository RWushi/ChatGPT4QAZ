from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timezone
from Config import dp, bot, UserState, create_connection
from Keyboards import usage_kb

async def usage(chat_id):
    await bot.send_message(chat_id, text="Все, что связано с использованием бота", reply_markup=usage_kb)

#Из раздела оплаты
@dp.message_handler(lambda message: message.text == "Назад⏪️", state=UserState.payment)
async def payment_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.usage.set()
    await usage(message.chat.id)

from Payment import payment

@dp.message_handler(lambda message: message.text == "Пробные запросы🎟", state=UserState.usage)
async def free_messages(message: types.Message):
    user_id = message.from_user.id
    conn = await create_connection()
    free_messages_left = await conn.fetchval('SELECT free_messages_left FROM user_subscriptions WHERE user_id = $1', user_id)
    await conn.close()
    await bot.send_message(message.chat.id, f"Остаток Ваших пробных запросов: {free_messages_left}")

@dp.message_handler(lambda message: message.text == "Моя подписка📆", state=UserState.usage)
async def my_subscription(message: types.Message):
    user_id = message.from_user.id
    conn = await create_connection()
    subscription_end_date = await conn.fetchval("SELECT subscription_end_date FROM user_subscriptions WHERE user_id = $1", user_id)
    await conn.close()

    if subscription_end_date is None:
        await bot.send_message(message.chat.id, "У Вас нет активной подписки")
    elif subscription_end_date < datetime.now(timezone.utc):
        formatted_date = subscription_end_date.strftime('%Y-%m-%d %H:%M:%S UTC')
        await bot.send_message(message.chat.id, f"Срок действия Вашей подписки истек:\n{formatted_date}")
    else:
        formatted_date = subscription_end_date.strftime('%Y-%m-%d %H:%M:%S UTC')
        await bot.send_message(message.chat.id, "Вы обладатель подписки GPT-4 Access Plus💎")
        await bot.send_message(message.chat.id, f"Дата окончания:\n{formatted_date}\nРеальное время прекращения действия подписки будет немного позже")


@dp.message_handler(lambda message: message.text == "Тарифы📋", state=UserState.usage)
async def rates(message: types.Message):
    await bot.send_message(message.chat.id, "Стоимость использования:\n"
                                            "\n"
                                            "💠 За 1 месяц: 7080₸ (15$)\n"
                                            "\n"
                                            "💠 За 3 месяца: 18880₸ (40$)\n"
                                            "       -экономия 11.1% (2360₸)\n"
                                            "\n"
                                            "💠 За 6 месяцев: 33040₸ (70$)\n"
                                            "       -экономия 22.2% (9440₸)\n"
                                            "\n"
                                            "💠 За 12 месяцев: 56640₸ (120$)\n"
                                            "       -экономия 33.3% (28320₸)")

@dp.message_handler(lambda message: message.text == "Оплата💳", state=UserState.usage)
async def payment_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.payment.set()
    await payment(message.chat.id)

@dp.message_handler(lambda message: message.text == "Связаться📞", state=UserState.usage)
async def contacts(message: types.Message):
    button = InlineKeyboardButton("Помощь и предложения📞", url="https://t.me/Alanya2gether")
    await bot.send_message(
        message.chat.id,
        "По любым вопросам и предложениям Вы можете связаться с человеком ниже",
        reply_markup=InlineKeyboardMarkup().add(button)
    )