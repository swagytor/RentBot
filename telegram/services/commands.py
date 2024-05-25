from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запустить бота'
        ),
        BotCommand(
            command='help',
            description='Информация о боте'
        )
    ]

    await bot.set_my_commands(commands)
