from datetime import timedelta, datetime

from aiogram import types
from asgiref.sync import sync_to_async

from events.models import Event
from players.models import Player


def get_fullname_keyboard(fullname):
    return types.ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text=fullname)
        ]
    ], resize_keyboard=True)


def get_user_state_data(state_data, tg_id):
    state_data.setdefault(f'{tg_id}', {})

    return state_data


def get_court_keyboard(courts):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, one_time_keyboard=True)

    for court in courts:
        keyboard.keyboard.append([types.KeyboardButton(text=court['title'])])

    return keyboard


def get_event_duration(start, end):
    result = []

    while start < end:
        result.append(start.strftime("%H:%M"))
        start += timedelta(minutes=15)

    return result


def get_max_duration(selected_time, time_list):
    selected_time = datetime.strptime(selected_time, "%H:%M")
    max_time = selected_time + timedelta(hours=2)
    selected_time += timedelta(minutes=15)

    for time in time_list:
        time = datetime.strptime(time, "%H:%M")

        if selected_time == max_time:
            break
        elif time < selected_time:
            continue
        elif time == selected_time:
            selected_time += timedelta(minutes=15)

    return selected_time


def get_inlined_date_keyboard(times, start_time='07:00'):
    result = []
    current_time = datetime.strptime(start_time, "%H:%M")

    for time in times:
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

    for i in range(0, len(result), 4):
        buttons = []
        if result[i:i + 4] == [' ', ' ', ' ', ' ']:
            continue
        for j in result[i:i + 4]:
            buttons.append(types.InlineKeyboardButton(text=j, callback_data=j))

        keyboard.inline_keyboard.append(buttons)

    return keyboard


def get_available_periods_keyboard(times):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(0, len(times), 4):
        buttons = []
        for j in times[i:i + 4]:
            buttons.append(types.InlineKeyboardButton(text=j, callback_data=j))

        keyboard.inline_keyboard.append(buttons)

    return keyboard


@sync_to_async
def is_user_limit_expired(tg_id, date):
    player = Player.objects.get(tg_id=tg_id)
    start_week = date - timedelta(days=date.weekday())
    end_week = start_week + timedelta(days=7)
    events = Event.objects.filter(player__tg_id=tg_id, start_date__range=[start_week, end_week])

    return not player.is_premium or events.count() >= 2
