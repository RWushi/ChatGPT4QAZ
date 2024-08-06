from aiogram import types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Config import dp, bot, UserState, add_new_user
from Keyboards import menu_kb

async def menu(chat_id):
    await bot.send_message(chat_id, text="Выберите раздел", reply_markup=menu_kb)

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    await add_new_user(message.chat.id)
    await UserState.menu.set()
    await menu(message.chat.id)

#Из раздела пречата
@dp.message_handler(lambda message: message.text == "Вернуться в меню↩️", state=UserState.prechat)
async def prechat_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.menu.set()
    await menu(message.chat.id)

#Из раздела кастомизации
@dp.message_handler(lambda message: message.text == "Вернуться в меню↩️", state=UserState.customization)
async def customization_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.menu.set()
    await menu(message.chat.id)

#Из раздела информации
@dp.message_handler(lambda message: message.text == "Вернуться в меню↩️", state=UserState.about)
async def about_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.menu.set()
    await menu(message.chat.id)

#Из раздела использования
@dp.message_handler(lambda message: message.text == "Вернуться в меню↩️", state=UserState.usage)
async def usage_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.menu.set()
    await menu(message.chat.id)

from PreChat import prechat
from Customization import customization
from About import about
from Usage import usage

@dp.message_handler(lambda message: message.text == "Чат с GPT-4🤖", state=UserState.menu)
async def chat_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.prechat.set()
    await prechat(message.chat.id)

@dp.message_handler(lambda message: message.text == "Персонализация🎨", state=UserState.menu)
async def customization_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.customization.set()
    await customization(message.chat.id)

@dp.message_handler(lambda message: message.text == "О боте📱", state=UserState.menu)
async def about_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.about.set()
    await about(message.chat.id)

@dp.message_handler(lambda message: message.text == "Использование🖥", state=UserState.menu)
async def usage_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.usage.set()
    await usage(message.chat.id)

@dp.message_handler(lambda message: message.text == "🔮Сделано RTools🔮", state=UserState.menu)
async def rtools_start(message: types.Message):
    button = InlineKeyboardButton("🔮Связаться🔮", url="https://t.me/wuxieten")
    await bot.send_message(
        message.chat.id,
        "Мы предлагаем инновационные и очень точные решения для бизнеса и личной жизни. Сможем сделать сайт, анимацию, бота и прочее на заказ",
        reply_markup=InlineKeyboardMarkup().add(button)
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
