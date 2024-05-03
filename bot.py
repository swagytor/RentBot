import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import asyncio
import logging

from aiogram.client.bot import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.filters.command import CommandStart
from django.conf import settings
from telegram.handlers import basic, registration, events
from telegram.services.commands import set_commands
from telegram.states.registration import RegistrationsState
from aiogram import F
from aiogram.fsm.storage.redis import RedisStorage
from aiogram3_calendar.calendar_types import SimpleCalendarCallback
from telegram.states.events import EventState


async def start():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - '
                                                   '(%(filename)s).%(funcName)s:%(lineno)d - %(message)s')

    bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')

    storage = RedisStorage.from_url('redis://localhost:6379/0')

    dp = Dispatcher(storage=storage)

    dp.message.register(basic.start, CommandStart())
    dp.message.register(registration.start_register, RegistrationsState.start)
    dp.message.register(registration.set_name, RegistrationsState.name)
    dp.message.register(registration.set_ntrp, RegistrationsState.ntrp)

    dp.message.register(basic.main_menu, F.text == "Главное меню")

    dp.message.register(events.my_events, F.text == "⚔Мои игры⚔")
    dp.message.register(events.all_events, F.text == '📜Все игры📜')
    dp.message.register(events.create_event, F.text == '🎾Записаться🎾')

    # dp.callback_query.register(events.cal, F.func(DetailedTelegramCalendar().func()))

    dp.message.register(events.select_date, EventState.select_court)
    dp.callback_query.register(events.set_date, SimpleCalendarCallback.filter())
    dp.callback_query.register(events.set_start_time, EventState.select_start_time)
    dp.callback_query.register(events.select_end_time, EventState.select_end_time)
    dp.callback_query.register(events.confirm_event, EventState.create_event)

    try:
        await dp.start_polling(bot)
        await set_commands(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
