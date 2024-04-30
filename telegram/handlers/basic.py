from aiogram import types

from players.models import Player
from telegram.buttons import basic
from telegram.handlers.registration import start_register
from telegram.states.registration import RegistrationsState


async def start(message: types.Message, state):
    tg_user = message.from_user

    try:
        await Player.objects.aget(tg_id=tg_user.id)
        await main_menu(message)
    except Player.DoesNotExist:
        await message.bot.send_message(tg_user.id, "Привет!\n"
                                                   "Меня зовут RentBot, и я буду твоим личным помощником, когда тебе захочется забронировать корт.\n"
                                                   "Давай для начала познакомимся")

        await state.set_state(state=RegistrationsState.start)

        await start_register(message, state)


async def main_menu(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Главное меню", reply_markup=basic.main_menu_keyboard)
