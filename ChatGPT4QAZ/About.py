from aiogram import types
from Config import dp, bot, UserState
from Keyboards import about_kb

async def about(chat_id):
    await bot.send_message(chat_id, text="Что такое Chat GPT-4 Access Plus?", reply_markup=about_kb)

@dp.message_handler(lambda message: message.text == "О продукте📖", state=UserState.about)
async def product(message: types.Message):
    await bot.send_message(message.chat.id, "Чат GPT - это современное чудо технологии, способное создавать тексты, отвечать почти на вопросы, генерировать идеи и просто быть приятным собеседником. Однако, доступ к этому инструменту может быть сложным, дорогим и весьма проблематичным из-за большого количества пользователей. Именно поэтому мы создали \"GPT-4 Access Plus\"")

@dp.message_handler(lambda message: message.text == "Возможности☄️", state=UserState.about)
async def possibilities(message: types.Message):
    await bot.send_message(message.chat.id, "Вместе с чатом GPT можно:\n"
                                            "💻 Создать мини-программу, даже если Вы не знаете программирования\n"
                                            "🎯 Получать очень точные ответы на специфичные вопросы, которые нельзя найти в поисковике\n"
                                            "👨‍⚕ Провести сессии как с психологом или психотерапевтом\n"
                                            "❤️‍🔥️ Общаться как с любимым человеком и полностью настроить характер партнера\n"
                                            "📹 Получить свежие идеи для создания видео/фото или сценария\n"
                                            "📝 Сделать сложную домашку, которая не гуглится\n"
                                            "⚙️ Внедрить в свою службу поддержки или CRM систему (делается на заказ RTools)\n"
                                            "💫 В общем, практически все, на что у Вас хватит фантазии")

@dp.message_handler(lambda message: message.text == "Преимущества➕", state=UserState.about)
async def advantages(message: types.Message):
    await bot.send_message(message.chat.id, "⏱ Получение доступа к боту сразу же после подключения\n"
                                            "🗄 Невероятный объем данных, которые могут превратиться в Ваши знания\n"
                                            "👶 Самый привычный и удобный способ получения информации, пользоваться этим ботом сможет каждый\n"
                                            "🛠 Огромные возможности для персонализации бота лично под Ваши нужды\n"
                                            "📈 Высокая скорость обработки запросов\n"
                                            "⌚️ Доступность 24/7")


@dp.message_handler(lambda message: message.text == "Дополнительная информация📑", state=UserState.about)
async def additional_information(message: types.Message):
    await bot.send_message(message.chat.id, "Подождите...")

    with open('Договор публичной оферты на предоставление услуг.docx', 'rb') as f1:
        await bot.send_document(message.chat.id, f1)

    with open('Политика конфиденциальности.docx', 'rb') as f2:
        await bot.send_document(message.chat.id, f2)

    with open('Возврат и гарантия.docx', 'rb') as f2:
        await bot.send_document(message.chat.id, f2)

