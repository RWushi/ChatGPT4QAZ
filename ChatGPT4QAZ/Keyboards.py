from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Чат с GPT-4🤖")],
        [KeyboardButton(text="Персонализация🎨")],
        [KeyboardButton(text="О боте📱"), KeyboardButton(text="Использование🖥")],
        [KeyboardButton(text="🔮Сделано RTools🔮")]
    ],
    resize_keyboard=True
)

prechat_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Бесплатный чат🎁")],
        [KeyboardButton(text="VIP чат💎")],
        [KeyboardButton(text="В чем отличие💡")],
        [KeyboardButton(text="Вернуться в меню↩️")]
    ],
    resize_keyboard=True
)

customization_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Задать стиль🕶")],
        [KeyboardButton(text="Задать информацию📚")],
        [KeyboardButton(text="Что это💡")],
        [KeyboardButton(text="Вернуться в меню↩️")]
    ],
    resize_keyboard=True
)

about_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О продукте📖")],
        [KeyboardButton(text="Возможности☄️"), KeyboardButton(text="Преимущества➕")],
        [KeyboardButton(text="Дополнительная информация📑")],
        [KeyboardButton(text="Вернуться в меню↩️")]
    ],
    resize_keyboard=True
)

usage_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Пробные запросы🎟"), KeyboardButton(text="Моя подписка📆")],
        [KeyboardButton(text="Тарифы📋"), KeyboardButton(text="Оплата💳")],
        [KeyboardButton(text="Связаться📞")],
        [KeyboardButton(text="Вернуться в меню↩️")]
    ],
    resize_keyboard=True
)

chat_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Новый диалог🔄")],
        [KeyboardButton(text="Назад⏪")]
    ],
    resize_keyboard=True
)

style_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Посмотреть пример💡")],
        [KeyboardButton(text="Действующий стиль✅")],
        [KeyboardButton(text="Сбросить стиль❌")],
        [KeyboardButton(text="Назад⏪")]
    ],
    resize_keyboard=True
)

information_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Посмотреть пример💡")],
        [KeyboardButton(text="Действующая информация✅")],
        [KeyboardButton(text="Сбросить информацию❌")],
        [KeyboardButton(text="Назад⏪")]
    ],
    resize_keyboard=True
)

payment_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1 месяц💠"), KeyboardButton(text="3 месяца💠")],
        [KeyboardButton(text="6 месяцев💠"), KeyboardButton(text="12 месяцев💠")],
        [KeyboardButton(text="Назад⏪️")]
    ],
    resize_keyboard=True
)