from aiogram import types
from aiogram.types import ChatActions
from Config import dp, bot, UserState, OPENAI_API_KEY
from ChatDB import save_history, reset_history, get_user_data, decrement_free_messages, has_free_messages
from Keyboards import chat_kb
import json
import openai

openai.api_key = OPENAI_API_KEY

async def chatfree(chat_id):
    await bot.send_message(chat_id, text="Напишите запрос чату GPT-4", reply_markup=chat_kb)

async def gpt_response(prompt, history, style, information, user_id):
    if history is None:
        history = []
    if len(history) == 0:
        system_message = "style: {}\ninformation: {}".format(style, information)
        history.append({"role": "system", "content": system_message})

    if not isinstance(history, list):
        history = []

    history.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=history,
        temperature=0.1,
        max_tokens=1000
    )

    generated_message = response['choices'][0]['message']['content'].strip()
    history.append({"role": "assistant", "content": generated_message})

    await save_history(user_id, history)

    return generated_message

@dp.message_handler(lambda message: message.text == "Новый диалог🔄", state=UserState.chatfree)
async def reset_chat(message: types.Message):
    user_id = message.from_user.id
    await reset_history(user_id)
    await message.answer("Старый диалог сброшен, можно начинать новый")


@dp.message_handler(state=UserState.chatfree)
async def echo(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not await has_free_messages(user_id, message):
        return

    await bot.send_chat_action(chat_id, ChatActions.TYPING)

    history, style, information = await get_user_data(user_id)

    if isinstance(history, str):
        history = json.loads(history)

    gpt_response_text = await gpt_response(message.text, history, style, information, user_id)

    await decrement_free_messages(user_id)

    await message.answer(gpt_response_text)


