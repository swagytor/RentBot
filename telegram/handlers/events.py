from datetime import datetime, timedelta
import requests
from bot import Bot
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import SimpleCalendar
from asgiref.sync import sync_to_async
from courts.models import Court
from events.models import Event
from players.models import Player
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

                inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text="Отменить", callback_data=f"cancel_event_{event['id']}")]
                ], resize_keyboard=True)

                await message.bot.send_message(message.from_user.id, text, reply_markup=inline_keyboard)
        else:
            await message.bot.send_message(message.from_user.id, "У вас нет активных игр")

    else:
        await message.bot.send_message(message.from_user.id, "Произошла ошибка при получении данных. Попробуйте позже.")


async def cancel_event(callback_query: types.CallbackQuery, bot: Bot):
    *_, event_id = callback_query.data.split('_')

    event = await Event.objects.aget(id=event_id)
    court = await Court.objects.aget(id=event.court_id)
    player = await Player.objects.aget(tg_id=callback_query.from_user.id)

    date_time, start_time = event.start_date.strftime("%d-%m-%Y %H:%M").rsplit()
    end_time = event.end_date.strftime("%Y-%m-%d %H:%M").split()[1]

    message_text = f"Игрок - {player} отменил(a) игру на {court}e\n" \
                   f"Дата: {date_time.replace('-', '.')}\n" \
                   f"Время: {start_time} - {end_time}"

    if event.start_date < datetime.now():
        await callback_query.message.answer("Нельзя отменить прошедшую игру")
        return await main_menu(callback_query.message)

    try:
        await sync_to_async(event.delete)()
        await callback_query.message.answer("Игра отменена")
        await bot.send_message(-1002127840587, message_text, reply_to_message_id=5)
    except Exception as e:
        await callback_query.message.answer("Произошла ошибка при отмене игры. Попробуйте позже.")

    await main_menu(callback_query.message)


async def all_events(message: types.Message, state: FSMContext):
    calendar = SimpleCalendar()

    await state.set_state(EventState.select_all_events_date)
    await message.answer(
        "Выберите дату:",
        reply_markup=await calendar.start_calendar()
    )


# async def select_date(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
#     calendar = SimpleCalendar()


async def select_all_events_date(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        if not today <= date.date() <= next_week:
            await callback_query.message.answer(
                f"Укажите дату между {today.strftime('%d.%m.%Y')} и {next_week.strftime('%d.%m.%Y')}")
            # await state.set_state(EventState.select_court)
            await all_events(callback_query.message, state)
        else:
            await callback_query.message.answer(f"Вы выбрали дату: {date.strftime('%d.%m.%Y')}")

            courts = await sync_to_async(Court.objects.all)()
            # courts =  courts

            result = []
            text = ''

            async for court in courts:
                text += f"Корт: {court.title}\n"

                response = requests.get('http://127.0.0.1:8000/api/events/',
                                        params={
                                            'start_date': f'{date.strftime("%Y-%m-%d")}',
                                            'court': court.id,
                                            'ordering': 'start_date'
                                        })

                if response.status_code == 200:
                    if response.json():
                        for event in response.json():
                            _, start_time = event['start_date'].split()
                            _, end_time = event['end_date'].split()
                            text += (f"{start_time}-{end_time} {event['_player']}\n")
                    else:
                        text += "В этот день нет активных игр\n"

                text += '\n'

            await callback_query.message.answer(f'<b>Расписание игр на {date.strftime("%d.%m.%Y")}:</b>\n\n'
                                                f'{text}')

            # await callback_query.message.answer("Все игры:")

            # if not response:
            #     await callback_query.message.answer("В этот день нет активных игр")
            #     await main_menu(callback_query.message)

            # for event in response:
            #     date, start_time = event['start_date'].split()
            #     _, end_time = event['end_date'].split()
            #
            #     text = (f"Дата: {date}\n"
            #             f"Время: {start_time} - {end_time}\n"
            #             f"Корт: {event['_court']}\n")
            #
            #     await callback_query.message.answer(text)

    else:
        await callback_query.message.answer("Произошла ошибка при получении данных. Попробуйте позже.")


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

        await state.set_state(EventState.select_date)
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
        if not today <= date.date() <= next_week:
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
        # inlined_date.inline_keyboard.append([types.InlineKeyboardButton(text="Назад", callback_data=f"select_end_time")])

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

    try:
        event = await Event.objects.acreate(
            start_date=start_date,
            end_date=end_date,
            court_id=state_data['selected_court'],
            player_id=state_data['id']
        )
        # event = requests.post('http://127.0.0.1:8000/api/events/', data={
        #   'start_date': start_date,
        #  'end_date': end_date,
        # 'court': state_data['selected_court'],
        # 'player': state_data['id']
        # })

        if event:
            await callback_query.message.answer(f"Вы записались на {state_data['selected_court']} корт\n"
                                                f"Дата: {state_data['selected_date']}\n"
                                                f"Время начала: {state_data['start_time']}\n"
                                                f"Время окончания: {state_data['end_time']}\n"
                                                "Хорошей игры!")

        await state.set_state()

        await main_menu(callback_query.message)
    except Exception as e:
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
