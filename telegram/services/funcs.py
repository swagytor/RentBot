from aiogram import types


def get_fullname_keyboard(fullname):
    return types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text=fullname)
        ]
    ], resize_keyboard=True)
