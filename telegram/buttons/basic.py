from aiogram import types

main_menu_keyboard_for_donate = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="🎾Записаться🎾"),
    ],
    [
        types.KeyboardButton(text="⚔Мои игры⚔"),
    ],
    [
        types.KeyboardButton(text="📜Все игры📜"),
    ],
    [
        types.KeyboardButton(text="❤Поддержать разработчиков❤")
    ]
], resize_keyboard=True)

main_menu_keyboard_admin = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="🎾Записаться🎾"),
    ],
    [
        types.KeyboardButton(text="⚔Мои игры⚔"),
    ],
    [
        types.KeyboardButton(text="📜Все игры📜"),
    ]
], resize_keyboard=True)
