import json
from datetime import datetime, timedelta

import requests
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import SimpleCalendar
from django.utils import timezone
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from telegram.services.funcs import get_event_duration, get_inlined_date_keyboard


async def my_events(message: types.Message):
    response = requests.get('http://127.0.0.1:8000/api/events/my_events/',
                            params={'tg_id': message.from_user.id,
                                    'ordering': 'start_date'})

    if response.status_code == 200:
        response = response.json()

        if response:
            await message.bot.send_message(message.from_user.id, "Ваши игры:")

            for event in response:
                date, start_time = event['start_date'].split()
                _, end_time = event['end_date'].split()

                text = (f"Дата: {date}\n"
                        f"Время: {start_time} - {end_time}\n"
                        f"Корт: {event['_court']}\n")

                await message.bot.send_message(message.from_user.id, text)
        else:
            await message.bot.send_message(message.from_user.id, "У вас нет активных игр")

    else:
        await message.bot.send_message(message.from_user.id, "Произошла ошибка при получении данных. Попробуйте позже.")


async def all_events(message: types.Message):
    response = requests.get('http://127.0.0.1:8000/api/events/',
                            params={'ordering': 'start_date'})

    if response.status_code == 200:
        response = response.json()

        await message.bot.send_message(message.from_user.id, "Все игры:")

        for event in response:
            date, start_time = event['start_date'].split()
            _, end_time = event['end_date'].split()

            text = (f"Дата: {date}\n"
                    f"Время: {start_time} - {end_time}\n"
                    f"Корт: {event['_court']}\n")

            await message.bot.send_message(message.from_user.id, text)

    else:
        await message.bot.send_message(message.from_user.id, "Произошла ошибка при получении данных. Попробуйте позже.")


# async def create_event(message: types.Message):
#     today = datetime.now().date()
#     next_week = today + timedelta(days=7)
#     calendar, step = DetailedTelegramCalendar(min_date=today, max_date=next_week).build()
#     calendar = json.loads(calendar)
#     await message.bot.send_message(message.from_user.id, "Выберите дату", reply_markup=calendar)

async def create_event(message: types.Message):
    calendar = SimpleCalendar()
    # calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    await message.answer(
        "Выберите дату",
        reply_markup=await calendar.start_calendar()
    )


async def select_date(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar()
    # calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        if not today <= date.date() < next_week:
            await callback_query.message.answer(
                f"Укажите дату между {today.strftime('%d.%m.%Y')} и {next_week.strftime('%d.%m.%Y')}")
            await create_event(callback_query.message)
        else:
            await callback_query.message.answer(f"Вы выбрали дату: {date.strftime('%d.%m.%Y')}")
            state_data = await state.get_data()
            state_data[f'{callback_query.message.from_user.id}'] = {
                'selected_date': date,
            }

            await state.set_data(state_data)

            await set_start_time(callback_query, state)


async def set_start_time(callback_query: types.CallbackQuery, state: FSMContext):
    date = await state.get_data()
    date = date[f'{callback_query.message.from_user.id}']['selected_date']
    start_period = date.replace(hour=7, minute=0, second=0, microsecond=0)
    end_period = date.replace(hour=22, minute=0, second=0, microsecond=0)
    interval = timedelta(minutes=15)

    date_periods = []
    event_period = []
    current_date = start_period

    while current_date < end_period:
        date_periods.append(current_date.strftime('%H:%M'))
        current_date += interval

    events = requests.get('http://127.0.0.1:8000/api/events/',
                          params={'court': 'all', }
                          # params={'start_date__date': callback_data['date']}
                          )

    if events.status_code == 200:
        events = events.json()
        if events:
            for event in events:

                print(event['start_date'])
                start_time = datetime.strptime(event['start_date'], '%d.%m.%Y %H:%M')
                end_time = datetime.strptime(event['end_date'], '%d.%m.%Y %H:%M')

                event_duration = get_event_duration(start_time, end_time)

                for time in event_duration:
                    date_periods.remove(time)

                # _, start_time = event['start_date'].sp
                event_period.append(start_time.strftime('%H:%M'))

        # date_set = set(date_periods)
        # await callback_query.message.answer(str(date_set))
        # event_set = set(event_period)
        # await callback_query.message.answer(str(event_set))

        # available_dates = list(date_set)
        # await callback_query.message.answer(str(available_dates))

        sorted_events = [date for date in sorted(date_periods, key=lambda x: datetime.strptime(x, '%H:%M'))]

        inlined_date = get_inlined_date_keyboard(sorted_events)

        await callback_query.message.answer(f"Доступное время:\n", reply_markup=inlined_date)
    else:
        await callback_query.message.answer("Произошла ошибка при получении данных. Попробуйте позже.")

    dates = []

# async def cal(c: types.CallbackQuery):
#     result, key, step = DetailedTelegramCalendar().process(c.data)
#     if not result and key:
#         key = json.loads(key)
#         await c.message.bot.edit_message_text(f"Select {LSTEP[step]}",
#                                             c.message.chat.id,
#                                             c.message.message_id,
#                                             reply_markup=key)
#     elif result:
#         await c.message.bot.edit_message_text(f"You selected {result}",
#                                             c.message.chat.id,
#                                             c.message.message_id)
