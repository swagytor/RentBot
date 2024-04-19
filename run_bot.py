import asyncio
import logging

from bot.core.handlers import basic
from bot.core.services.commands import set_commands
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from app.config import settings


async def start():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - '
                                                   '(%(filename)s).%(funcName)s:%(lineno)d - %(message)s')

    bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')

    dp = Dispatcher()

    dp.message.register(basic.start, CommandStart())

    try:
        await dp.start_polling(bot)
        await set_commands(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
