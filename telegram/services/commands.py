from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='starts',
            description='Запустить бота'
        ),
        BotCommand(
            command='test',
            description='Тестовая команда'
        )
    ]

    await bot.set_my_commands(commands)
