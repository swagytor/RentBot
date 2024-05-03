from datetime import datetime, timedelta

import requests
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import SimpleCalendar

from courts.models import Court
from telegram.handlers.basic import main_menu
from telegram.services.funcs import get_event_duration, get_inlined_date_keyboard, get_court_keyboard, get_max_duration, \
    get_available_periods_keyboard, is_user_limit_expired
from telegram.states.events import EventState


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

async def create_event(message: types.Message, state: FSMContext):

    courts = requests.get('http://127.0.0.1:8000/api/courts/').json()

    keyboard = get_court_keyboard(courts)

    await message.answer("Выберите корт", reply_markup=keyboard)
    await state.set_state(EventState.select_court)


async def select_date(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    try:
        court = await Court.objects.aget(title=message.text)

        await message.answer(
            f'Выбран корт "{message.text}"',
            reply_markup=types.ReplyKeyboardRemove()
        )

        state_data['selected_court'] = court.id
        await state.set_data(state_data)

        calendar = SimpleCalendar()
        # calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))

        await message.answer(
            "Выберите дату:",
            reply_markup=await calendar.start_calendar()
        )

    except Court.DoesNotExist:
        await message.answer("Выберите корт из списка")


async def set_date(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        if not today <= date.date() < next_week:
            await callback_query.message.answer(
                f"Укажите дату между {today.strftime('%d.%m.%Y')} и {next_week.strftime('%d.%m.%Y')}")
            # await state.set_state(EventState.select_court)
            await create_event(callback_query.message, state)
        elif await is_user_limit_expired(callback_query.from_user.id, date):
            await callback_query.message.answer(
                "Превышен лимит ваших игр на этой неделе."
            )
            return await main_menu(callback_query.message)
        else:
            date = date.strftime('%d.%m.%Y')
            await callback_query.message.answer(f"Вы выбрали дату: {date}")

            state_data = await state.get_data()
            state_data['selected_date'] = date
            await state.set_data(state_data)

            await state.set_state(EventState.select_start_time)
            await set_start_time(callback_query, state)


async def set_start_time(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    date = datetime.strptime(state_data['selected_date'], '%d.%m.%Y')
    court = state_data['selected_court']

    start_period = date.replace(hour=7, minute=0, second=0, microsecond=0)
    end_period = date.replace(hour=22, minute=0, second=0, microsecond=0)
    interval = timedelta(minutes=15)

    date_periods = []
    current_time = start_period

    while current_time < end_period:
        date_periods.append(current_time.strftime('%H:%M'))
        current_time += interval

    events = requests.get('http://127.0.0.1:8000/api/events/',
                          params={'court': court,
                                  'start_date': date.strftime('%Y-%m-%d'),
                                  },
                          )

    # events = sync_to_async(Event.objects.filter)(court_id=court, start_date__date=date.strftime('%Y-%m-%d'))
    if events.status_code == 200:
        for event in events.json():
            start_time = datetime.strptime(event['start_date'], '%d.%m.%Y %H:%M')
            end_time = datetime.strptime(event['end_date'], '%d.%m.%Y %H:%M')

            # start_time = event.start_date
            # end_time = event.end_date

            event_duration = get_event_duration(start_time, end_time)

            for time in event_duration:
                date_periods.remove(time)

        sorted_events = [date for date in sorted(date_periods, key=lambda x: datetime.strptime(x, '%H:%M'))]

        state_data['available_times'] = sorted_events
        await state.set_data(state_data)


        inlined_date = get_inlined_date_keyboard(sorted_events)

        await callback_query.message.answer(f"Доступное время:\n", reply_markup=inlined_date)

        await state.set_state(EventState.select_end_time)
    else:
        await callback_query.message.answer("Произошла ошибка при получении данных. Попробуйте позже.")


async def select_end_time(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    start_time = callback_query.data

    if start_time != ' ':
        await callback_query.message.answer(f"Вы выбрали время {start_time}")

        state_data['start_time'] = start_time
        await state.set_data(state_data)

        available_times = state_data['available_times']
        max_time = get_max_duration(start_time, available_times)

        available_periods = []

        start_time = datetime.strptime(start_time, "%H:%M")

        while start_time < max_time:
            start_time += timedelta(minutes=15)
            available_periods.append(start_time.strftime("%H:%M"))

        # user_data['available_periods'] = available_periods

        inlined_date = get_available_periods_keyboard(available_periods)

        await callback_query.message.answer(f"Доступное время для завершения:\n", reply_markup=inlined_date)

        await state.set_state(EventState.create_event)


async def confirm_event(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    state_data['end_time'] = callback_query.data
    date = datetime.strptime(state_data['selected_date'], '%d.%m.%Y')
    start_time = datetime.strptime(state_data['start_time'], "%H:%M")
    end_time = datetime.strptime(callback_query.data, "%H:%M")

    start_date = date.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
    end_date = date.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)

    event = requests.post('http://127.0.0.1:8000/api/events/', data={
        'start_date': start_date,
        'end_date': end_date,
        'court': state_data['selected_court'],
        'player': state_data['id']
    })

    if event.status_code == 201:
        await callback_query.message.answer(f"Отлично вы записались на {state_data['selected_court']} корт\n"
                                            f"Дата: {state_data['selected_date']}\n"
                                            f"Время начала: {state_data['start_time']}\n"
                                            f"Время окончания: {state_data['end_time']}\n"
                                            f"Хорошей игры!")

        await state.set_state()

        await main_menu(callback_query.message)
    else:
        await callback_query.message.answer("Произошла ошибка при создании события. Попробуйте позже.")

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
