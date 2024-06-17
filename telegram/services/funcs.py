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


async def get_court_keyboard(courts):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, one_time_keyboard=True, selective=True)

    async for court in courts:
        keyboard.keyboard.append([types.KeyboardButton(text=court.title)])

    keyboard.keyboard.append([types.KeyboardButton(text="Назад")])
    return keyboard


def get_event_duration(start, end):
    result = []

    while start < end:
        result.append(start.strftime("%H:%M"))
        start += timedelta(minutes=30)

    return result


def get_max_duration(selected_time, time_list, is_weekend, start_time):
    selected_time = datetime.strptime(selected_time, "%H:%M")
    hours, minutes = start_time.split(':')
    if is_weekend in (5, 6) and (int(hours) > 9 or int(hours) == 9 and int(minutes) > 0):
        max_time = selected_time + timedelta(hours=1.5)
    elif is_weekend in (0, 1, 2, 3, 4) and int(hours) > 13:
        max_time = selected_time + timedelta(hours=1.5)
    else:
        max_time = selected_time + timedelta(hours=2)
    selected_time += timedelta(minutes=30)

    for time in time_list:
        time = datetime.strptime(time, "%H:%M")

        if selected_time == max_time:
            break
        elif time < selected_time:
            continue
        elif time == selected_time:
            selected_time += timedelta(minutes=30)

    return selected_time


def get_inlined_date_keyboard(times, start_time='07:00'):
    result = []
    current_time = datetime.strptime(start_time, "%H:%M")

    for time in times:
        time = datetime.strptime(time, "%H:%M")

        while current_time < time:
            result.append(' ')
            current_time += timedelta(minutes=30)

        if current_time == time:
            result.append(time.strftime("%H:%M"))
            current_time += timedelta(minutes=30)
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

    keyboard.inline_keyboard.append([types.InlineKeyboardButton(text="Назад", callback_data="Назад")])
    return keyboard


def get_available_periods_keyboard(times):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(0, len(times), 4):
        buttons = []
        for j in times[i:i + 4]:
            buttons.append(types.InlineKeyboardButton(text=j, callback_data=j))

        keyboard.inline_keyboard.append(buttons)

    keyboard.inline_keyboard.append([types.InlineKeyboardButton(text="Назад", callback_data="Назад")])
    return keyboard


@sync_to_async
def is_user_limit_expired(tg_id, date):
    player = Player.objects.get(tg_id=tg_id)

    if player.is_premium or player.name == 'Vitaly No one' or player.name == 'Anna':
        return False

    start_week = date - timedelta(days=date.weekday())
    end_week = start_week + timedelta(days=7)
    events = Event.objects.filter(player__tg_id=tg_id, start_date__range=[start_week, end_week])

    return events.count() >= 2


@sync_to_async
def day_limit(tg_id, date):
    events_on_day = Event.objects.filter(player__tg_id=tg_id, start_date__date=date)
    return events_on_day.count() > 0


@sync_to_async
def black_list_check(tg_id):
    black_list = [568341825, 'poteshkin', 286762993]
    return tg_id in black_list


#6386505711