from datetime import datetime, timedelta
from bot import Bot
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import SimpleCalendar
from asgiref.sync import sync_to_async
from courts.models import Court
from events.models import Event
from players.models import Player
from telegram.handlers.basic import main_menu, get_player_tg_username
from telegram.services.funcs import get_event_duration, get_inlined_date_keyboard, get_court_keyboard, get_max_duration, \
    get_available_periods_keyboard, is_user_limit_expired
from telegram.states.events import EventState


async def my_events(message: types.Message):
    try:
        tg_username = await get_player_tg_username(message)
        # response = requests.get('http://127.0.0.1:8000/api/events/my_events/',
        #                         params={'tg_id': message.from_user.id,
        #                                 'ordering': 'start_date'})
        #
        # if response.status_code == 200:
        #     response = response.json()
        #
        #     if response:
        #         await message.bot.send_message(message.from_user.id, "Ваши игры:")
        #
        #         for event in response:
        #             date, start_time = event['start_date'].split()
        #             _, end_time = event['end_date'].split()
        events = await sync_to_async(Event.objects.filter)(
            player__tg_id=message.from_user.id,
            end_date__gte=datetime.now()
        )
        events = events.order_by('start_date')
        if await sync_to_async(events.exists)():
            await message.bot.send_message(message.from_user.id, "Ваши игры:")
            async for event in events:
                date, start_time = event.start_date.strftime('%d.%m.%Y %H:%M').split()
                _, end_time = event.end_date.strftime('%d.%m.%Y %H:%M').split()
                text = (f"Дата: {date}\n"
                        f"Время: {start_time} - {end_time}\n"
                        f"Корт: {event.court_id}\n")

                inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text="Отменить", callback_data=f"cancel_event_{event.id}")],
                ], resize_keyboard=True)

                await message.bot.send_message(message.from_user.id, text, reply_markup=inline_keyboard)
        else:
            await message.bot.send_message(message.from_user.id, "У вас нет активных игр")
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении данных. Попробуйте позже. {e}")


async def cancel_event(callback_query: types.CallbackQuery, bot: Bot):
    *_, event_id = callback_query.data.split('_')

    event = await Event.objects.aget(id=event_id)
    court = await Court.objects.aget(id=event.court_id)
    player = await Player.objects.aget(tg_id=callback_query.from_user.id)

    date_time, start_time = event.start_date.strftime("%d.%m.%Y %H:%M").rsplit()
    end_time = event.end_date.strftime("%Y.%m.%d %H:%M").split()[1]

    if player.tg_username:
        message_text = f"Игрок - <a href='https://telegram.me/{player.tg_username}'>{player.name}</a> отменил(a) игру на {court}e\n" \
                       f"Дата: {date_time}\n" \
                       f"Время: {start_time} - {end_time}"
    else:
        message_text = f"Игрок - {player.name} отменил(a) игру на {court}e\n" \
                       f"Дата: {date_time}\n" \
                       f"Время: {start_time} - {end_time}"

    if event.start_date < datetime.now():
        await callback_query.message.answer("Нельзя отменить прошедшую игру")
        return await main_menu(callback_query.message)

    try:
        await sync_to_async(event.delete)()
        await callback_query.message.answer("Игра отменена")
        await bot.send_message(-1001599764524, message_text, reply_to_message_id=14255, disable_web_page_preview=True)
    except Exception as e:
        await callback_query.message.answer("Произошла ошибка при отмене игры. Попробуйте позже.")

    await main_menu(callback_query.message)


async def all_events(message: types.Message, state: FSMContext):
    try:
        calendar = SimpleCalendar()
        if not message.from_user.is_bot:
            tg_username = await get_player_tg_username(message)

        await state.set_state(EventState.select_all_events_date)
        await message.answer(
            "Выберите дату:",
            reply_markup=await calendar.start_calendar()
        )

    except Exception as e:
        await message.answer(f"Произошла ошибка при отмене игры. Попробуйте позже. {e} - all_events")


async def select_all_events_date(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        if not today <= date.date() <= next_week:
            await callback_query.message.answer(
                f"Укажите дату между {today.strftime('%d.%m.%Y')} и {next_week.strftime('%d.%m.%Y')}")
            await all_events(callback_query.message, state)
        else:
            await callback_query.message.answer(f"Вы выбрали дату: {date.strftime('%d.%m.%Y')}")

            courts = await sync_to_async(Court.objects.all)()

            result = []
            text = ''

            async for court in courts:
                text += f"Корт: {court.title}\n"

                events = await sync_to_async(Event.objects.filter)(
                    start_date__date=date.strftime('%Y-%m-%d'),
                    court=court.id
                )
                events = events.order_by('start_date')
                if await sync_to_async(events.exists)():
                    async for event in events:
                        _, start_time = event.start_date.strftime("%d-%m-%Y %H:%M").rsplit()
                        _, end_time = event.end_date.strftime("%Y-%m-%d %H:%M").split()
                        player_id = event.player_id
                        # response = requests.get('http://127.0.0.1:8000/api/events/',
                        #                         params={
                        #                             'start_date': f'{date.strftime("%Y-%m-%d")}',
                        #                             'court': court.id,
                        #                             'ordering': 'start_date'
                        #                         })
                        #
                        # if response.status_code == 200:
                        #     if response.json():
                        #         for event in response.json():
                        #             _, start_time = event['start_date'].split()
                        #             _, end_time = event['end_date'].split()
                        #
                        #             player_id = event['player']
                        player = await Player.objects.aget(id=player_id)
                        if player.tg_username:
                            text += f"{start_time}-{end_time} <a href='https://telegram.me/{player.tg_username}'>{player.name}</a> \n"
                        else:
                            text += f"{start_time}-{end_time} {player.name}\n"
                else:
                    text += "В этот день нет активных игр\n"

                text += '\n'

            await callback_query.message.answer(f'<b>Расписание игр на {date.strftime("%d.%m.%Y")}:</b>\n\n'
                                                f'{text}', disable_web_page_preview=True)


async def create_event(message: types.Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        courts = await sync_to_async(Court.objects.all)()
        if not message.from_user.is_bot:
            tg_username = await get_player_tg_username(message)

        keyboard = await get_court_keyboard(courts)

        await message.answer("Выберите корт", reply_markup=keyboard)
        await state.set_state(EventState.select_court)

    except Exception as e:
        await message.answer(f"Произошла ошибка при получении данных. Попробуйте позже. {e} - create_event")


async def select_date(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    try:
        if message.text == 'Назад':
            await state.set_state(EventState.main_menu)
            return await main_menu(message)
        else:
            court = await Court.objects.aget(title=message.text)
            await message.answer(
                f'Выбран корт "{message.text}"',
                reply_markup=types.ReplyKeyboardRemove()
            )

        state_data['selected_court'] = court.id
        await state.set_data(state_data)
        return await draw_calendar(message, state)


    except Court.DoesNotExist:
        await state.set_state(None)
        await message.answer("Выберите корт из списка")


async def draw_calendar(message: types.Message, state: FSMContext):
    try:
        await state.set_state(EventState.select_date)
        calendar = SimpleCalendar()
        await message.answer(
            "Выберите дату:\n"
            "Вернуться в главное меню - /start",
            reply_markup=await calendar.start_calendar()
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении данных. Попробуйте позже. {e} - draw_calendar")


async def set_date(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    try:
        state_data = await state.get_data()
        calendar = SimpleCalendar()
        selected, date = await calendar.process_selection(callback_query, callback_data)
        if selected:
            today = datetime.now().date()
            next_week = today + timedelta(days=7)
            if not today <= date.date() <= next_week:
                await callback_query.message.reply(
                    f"Укажите дату между {today.strftime('%d.%m.%Y')} и {next_week.strftime('%d.%m.%Y')}")
                # await state.set_state(EventState.select_court)
                await create_event(callback_query.message, state)
            elif await is_user_limit_expired(callback_query.from_user.id, date):
                await callback_query.message.reply(
                    "Превышен лимит ваших игр на этой неделе."
                )
                return await main_menu(callback_query.message)
            else:
                date = date.strftime('%d.%m.%Y')
                await callback_query.message.reply(f"Вы выбрали дату: {date}")

                state_data = await state.get_data()
                state_data['selected_date'] = date
                await state.set_data(state_data)

                await state.set_state(EventState.select_start_time)
                await set_start_time(callback_query, state)


    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка при получении данных. Попробуйте позже. {e}")


async def set_start_time(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    date = datetime.strptime(state_data['selected_date'], '%d.%m.%Y')
    court = state_data['selected_court']

    start_period = date.replace(hour=7, minute=0, second=0, microsecond=0)
    end_period = date.replace(hour=23, minute=0, second=0, microsecond=0)
    interval = timedelta(minutes=15)

    date_periods = []
    current_time = start_period

    while current_time < end_period:
        if current_time >= datetime.now():
            date_periods.append(current_time.strftime('%H:%M'))
        current_time += interval

    try:
        events = await sync_to_async(Event.objects.filter)(
            court_id=court, start_date__date=date.strftime('%Y-%m-%d'),
        )

        async for event in events:
            start_time = datetime.strptime(event.start_date.strftime('%d.%m.%Y %H:%M'), '%d.%m.%Y %H:%M')
            end_time = datetime.strptime(event.end_date.strftime('%d.%m.%Y %H:%M'), '%d.%m.%Y %H:%M')
            event_duration = get_event_duration(start_time, end_time)

            for time in event_duration:
                if time in date_periods:
                    date_periods.remove(time)

        sorted_events = [date for date in sorted(date_periods, key=lambda x: datetime.strptime(x, '%H:%M'))]

        state_data['available_times'] = sorted_events
        await state.set_data(state_data)

        inlined_date = get_inlined_date_keyboard(sorted_events)

        await callback_query.message.answer(f"Доступное время начало игры:\n"
                                            f"\n"
                                            f"Окончание игры необходимимо выбрать из окна со врменем ниже под названием "
                                            f"- Доступное время для завершения:\n"
                                            f"Оно появится после выбора времени начала игры", reply_markup=inlined_date)

        await state.set_state(EventState.select_end_time)

    except Exception as e:
        await state.set_state(None)
        await callback_query.message.answer(f"Произошла ошибка при отмене игры. Попробуйте позже {e}.")


async def select_end_time(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'Назад':
        await callback_query.bot.delete_message(chat_id=callback_query.message.chat.id,
                                                message_id=callback_query.message.message_id)
        await state.set_state(EventState.select_date)
        return await draw_calendar(callback_query.message, state)
    state_data = await state.get_data()
    start_time = callback_query.data

    if start_time != ' ':

        state_data['start_time'] = start_time
        await state.set_data(state_data)
        is_weekend = datetime.strptime(state_data['selected_date'], '%d.%m.%Y').weekday()

        available_times = state_data['available_times']
        max_time = get_max_duration(start_time, available_times, is_weekend, start_time)

        available_periods = []

        current_time = datetime.strptime(start_time, "%H:%M")

        while current_time < max_time:
            current_time += timedelta(minutes=15)
            available_periods.append(current_time.strftime("%H:%M"))

        inlined_date = get_available_periods_keyboard(available_periods)
        await callback_query.bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                                   message_id=callback_query.message.message_id,
                                                   text=f"Вы выбрали время начала игры: {start_time}\n"
                                                        f"Доступное время для завершения:")

        await callback_query.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                                           message_id=callback_query.message.message_id,
                                                           reply_markup=inlined_date)

        await state.set_state(EventState.create_event)


async def confirm_event(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'Назад':
        await callback_query.bot.delete_message(chat_id=callback_query.message.chat.id,
                                                message_id=callback_query.message.message_id)
        await state.set_state(EventState.select_start_time)
        await set_start_time(callback_query, state)
    else:
        await callback_query.bot.delete_message(chat_id=callback_query.message.chat.id,
                                                message_id=callback_query.message.message_id)
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

            if event:
                await callback_query.message.answer(f"Вы записались на {state_data['selected_court']} корт.\n"
                                                    f"Дата: {state_data['selected_date']}\n"
                                                    f"Время начала: {state_data['start_time']}\n"
                                                    f"Время окончания: {state_data['end_time']}\n"
                                                    "Хорошей игры!💥\n"
                                                    "\n"
                                                    "Вернуться в главное меню - /start\n"
                                                    "\n"
                                                    "Ознакомиться с правилами - /help\n"
                                                    "\n"
                                                    "<b>Большая просьба - Если не получается придти в записанное время, "
                                                    "пожалуйста, старайтесь отменять игры заранее!🙌 "
                                                    "Все участники сообщества будут вам признательны☺!</b>\n"
                                                    )

            await state.set_state()

        except Exception as e:
            await callback_query.message.answer(f"Произошла ошибка при создании события. Попробуйте позже. {e}")
