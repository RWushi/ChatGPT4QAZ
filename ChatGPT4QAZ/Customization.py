from aiogram import types
from Config import dp, bot, UserState
from Keyboards import customization_kb

async def customization(chat_id):
    await bot.send_message(chat_id, text="Здесь Вы сможете задать определенный стиль и некоторую информацию чату GPT", reply_markup=customization_kb)

#Из раздела стиля
@dp.message_handler(lambda message: message.text == "Назад⏪", state=UserState.style)
async def style_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.customization.set()
    await customization(message.chat.id)

#Из раздела информации
@dp.message_handler(lambda message: message.text == "Назад⏪", state=UserState.information)
async def information_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.customization.set()
    await customization(message.chat.id)

from Style import style
from Information import information

@dp.message_handler(lambda message: message.text == "Задать стиль🕶", state=UserState.customization)
async def style_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.style.set()
    await style(message.chat.id)

@dp.message_handler(lambda message: message.text == "Задать информацию📚", state=UserState.customization)
async def information_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.information.set()
    await information(message.chat.id)

@dp.message_handler(lambda message: message.text == "Что это💡", state=UserState.customization)
async def information_start(message: types.Message):
    await bot.send_message(message.chat.id, "🔸 Стиль нужен для того, чтобы задать стилистику Вашего диалога с чатом GPT: неофициальный, шутливый, любовный, поучительный и так далее. Здесь Вас ничего не ограничивает, Вы можете задать любой стиль, и его будет придерживаться чат GPT на протяжении разговора\n"
                                            "🔸 Информация нужна для того, чтобы передать какие-либо данные чату GPT, это может быть информация о Вас, или о том, чего Вы на данный момент хотите: я учу математику 10 класса, мне нужно подготовиться к экзамену по психологии и так далее. Здесь Вас также ничего не ограничивает, Вы можете задать любую информацию, и ее будет учитывать чат GPT на протяжении разговора")
