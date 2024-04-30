from aiogram import types

main_menu_keyboard = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="🎾Записаться🎾"),
    ],
    [
        types.KeyboardButton(text="🥎Мои игры🥎"),
    ],
    [
        types.KeyboardButton(text="📜Все игры📜"),
    ]
], resize_keyboard=True)
