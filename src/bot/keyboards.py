from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Что вы можете сделать для ритейлеров?")],
    ],
    resize_keyboard=True,
)
