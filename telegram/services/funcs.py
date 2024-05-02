from datetime import timedelta, datetime

from aiogram import types


def get_fullname_keyboard(fullname):
    return types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text=fullname)
        ]
    ], resize_keyboard=True)


def get_event_duration(start, end):
    result = []

    while start < end:
        result.append(start.strftime("%H:%M"))
        start += timedelta(minutes=15)

    return result


def get_inlined_date_keyboard(dates):
    print(dates)
    result = []
    current_time = datetime.strptime("07:00", "%H:%M")

    for time in dates:
        time = datetime.strptime(time, "%H:%M")

        while current_time < time:
            result.append(' ')
            current_time += timedelta(minutes=15)

        if current_time == time:
            result.append(time.strftime("%H:%M"))
            current_time += timedelta(minutes=15)
        else:
            result.append(' ')

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])

    print(result)

    for i in range(0, len(result), 4):
        buttons = []
        if result[i:i+4] == [' ', ' ', ' ', ' ']:
            continue
        for j in result[i:i+4]:
            buttons.append(types.InlineKeyboardButton(text=j, callback_data=j))

        keyboard.inline_keyboard.append(buttons)


    # inline = [result[i:i+4] for i in range(0, len(result), 4)]
    # keyboad = types.InlineKeyboardMarkup(inline_keyboard=inline)
    # for date, ind in enumerate(dates, 1):
    #     dates[ind] = types.InlineKeyboardButton(text=date, callback_data=date)

    return keyboard
