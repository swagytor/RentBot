from aiogram import types

main_menu_keyboard = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="Предстоящие игры"),
    ],
    [
        types.KeyboardButton(text="Прошедшие игры"),
    ]
], resize_keyboard=True)
