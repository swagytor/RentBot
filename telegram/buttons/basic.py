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
        types.KeyboardButton(text="❤Сбор на сетки❤")
    ]
], resize_keyboard=True)


start_button = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="❤Сбор на сетки ❤")
    ],
    [
        types.KeyboardButton(text="🔙В Главное меню🔙"),
    ],

], resize_keyboard=True)
