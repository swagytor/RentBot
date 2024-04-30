import os

import django
from aiogram import F

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


async def start():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - '
                                                   '(%(filename)s).%(funcName)s:%(lineno)d - %(message)s')

    bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')

    dp = Dispatcher()

    dp.message.register(basic.start, CommandStart())
    dp.message.register(registration.start_register, RegistrationsState.start)
    dp.message.register(registration.set_name, RegistrationsState.name)
    dp.message.register(registration.set_ntrp, RegistrationsState.ntrp)

    dp.message.register(basic.main_menu, F.text == "Главное меню")

    dp.message.register(events.my_events, F.text == "🥎Мои игры🥎")

    try:
        await dp.start_polling(bot)
        await set_commands(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
