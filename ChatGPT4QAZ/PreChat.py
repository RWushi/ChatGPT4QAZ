from aiogram import types
from Config import dp, bot, UserState
from Keyboards import prechat_kb
from ChatDB import pre_check_free, pre_check_vip

async def prechat(chat_id):
    await bot.send_message(chat_id, text="Если Вы хотите попробовать- перейдите в бесплатный чат\nЕсли у Вас активна подписка- перейдите в VIP чат💎", reply_markup=prechat_kb)

#Из бесплатного раздела
@dp.message_handler(lambda message: message.text == "Назад⏪", state=UserState.chatfree)
async def chatfree_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.prechat.set()
    await prechat(message.chat.id)

#Из платного раздела
@dp.message_handler(lambda message: message.text == "Назад⏪", state=UserState.chatvip)
async def chatvip_finish(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.prechat.set()
    await prechat(message.chat.id)

from ChatFree import chatfree
from ChatVIP import chatvip

@dp.message_handler(lambda message: message.text == "Бесплатный чат🎁", state=UserState.prechat)
async def chatfree_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    if await pre_check_free(message.from_user.id, message):
        await UserState.chatfree.set()
        await chatfree(message.chat.id)
    else:
        pass


@dp.message_handler(lambda message: message.text == "VIP чат💎", state=UserState.prechat)
async def chatvip_start(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")
    if await pre_check_vip(message.from_user.id, message):
        await bot.send_message(message.chat.id, "Проверка пройдена успешно, добро пожаловать в VIP чат💎")
        await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxkBAAIQAWUlEp7AtYdnYjZD5V5FtrfMb7mZAAI_EQACQQipSKePgWazX2l2MAQ")
        await UserState.chatvip.set()
        await chatvip(message.chat.id)
    else:
        pass


@dp.message_handler(lambda message: message.text == "В чем отличие💡", state=UserState.prechat)
async def customization_start(message: types.Message):
    await bot.send_message(message.chat.id, "Для обладателей подписки выделены отдельные ресурсы общения с чатом GPT, таким образом бесплатные и платные запросы представляют собой 2 разных потока\n"
                                            "Также в VIP потоке запросы работают немного быстрее (однако Вы вряд ли заметите эту разницу, потому что обработка бесплатных запросов тоже работает быстро)")