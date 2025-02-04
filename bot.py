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

    dp.message.register(basic.redirect_to_bot, F.chat.type != 'private', CommandStart())

    dp.message.register(basic.redirect_to_bot, F.chat.type != 'private',
                        F.text.in_(['В Главное меню', '⚔Мои игры⚔', '📜Все игры📜', '🎾Записаться🎾']))

    dp.callback_query.register(basic.redirect_to_bot_callback, F.state == '*', F.chat.type != 'private')

    dp.message.register(basic.start, CommandStart())

    dp.message.register(basic.about, F.text == "/help")
    dp.message.register(basic.main_menu, F.text == "🔙В Главное меню🔙", F.chat.type == 'private')

    dp.message.register(registration.start_register, RegistrationsState.start)
    dp.message.register(registration.set_name, RegistrationsState.name)
    dp.message.register(registration.set_ntrp, RegistrationsState.ntrp)

    dp.message.register(basic.main_menu, F.text == "🔙В Главное меню🔙", F.chat.type == 'private')

    dp.message.register(events.my_events, F.text == "⚔Мои игры⚔", F.chat.type == 'private')

    dp.message.register(basic.get_tools, F.text == "❤Сбор на сетки❤", F.chat.type == 'private')

    dp.callback_query.register(events.cancel_event, F.data.startswith('cancel_event'))

    dp.message.register(events.all_events, F.text == '📜Все игры📜', F.chat.type == 'private')

    dp.callback_query.register(events.select_all_events_date, EventState.select_all_events_date,
                               SimpleCalendarCallback.filter())

    dp.message.register(events.draw_calendar, F.text == '🎾Записаться🎾', F.chat.type == 'private')
    dp.callback_query.register(events.set_date, EventState.select_date, SimpleCalendarCallback.filter())
    dp.message.register(events.create_court, EventState.select_court)
    dp.message.register(events.select_court, EventState.set_court)
    dp.message.register(events.set_start_time, EventState.select_start_time)
    dp.callback_query.register(events.select_end_time, EventState.select_end_time)
    dp.callback_query.register(events.confirm_event, EventState.create_event)

    try:
        await set_commands(bot)
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
