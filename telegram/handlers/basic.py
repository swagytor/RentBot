from aiogram import types

from players.models import Player
from telegram.buttons import basic
from telegram.custom_calendar.app import CustomCalendar
from telegram.handlers.registration import start_register
from telegram.services.funcs import get_user_state_data
from telegram.states.registration import RegistrationsState


async def start(message: types.Message, state):
    tg_user = message.from_user

    try:
        player = await Player.objects.aget(tg_id=tg_user.id)

        state_data = await state.get_data()
        state_data['id'] = player.id
        await state.set_data(state_data)

        await main_menu(message)

    except Player.DoesNotExist:
        await message.bot.send_message(tg_user.id, "Привет!\n"
                                                   "Меня зовут RentBot, и я буду твоим личным помощником, когда тебе захочется забронировать корт.\n"
                                                   "Давай для начала познакомимся")

        await state.set_state(state=RegistrationsState.start)

        await start_register(message, state)


async def main_menu(message: types.Message):
    await message.answer("Главное меню", reply_markup=basic.main_menu_keyboard)


# async def test(message: types.Message):
#     calendar = CustomCalendar()
#     calendar = await calendar.start_calendar()
#
#     await message.answer("Выберите дату:", reply_markup=calendar)