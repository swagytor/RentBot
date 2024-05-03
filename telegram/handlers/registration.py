from aiogram import types
from aiogram.fsm.context import FSMContext

from players.models import Player
from telegram.handlers import basic
from telegram.services.funcs import get_fullname_keyboard
from telegram.states.registration import RegistrationsState


async def start_register(message: types.Message, state: FSMContext):
    tg_user = message.from_user

    player_name_keyboard = get_fullname_keyboard(tg_user.full_name)

    await message.bot.send_message(tg_user.id, "Как я могу к тебе обращаться?", reply_markup=player_name_keyboard)

    await state.set_state(RegistrationsState.name)


async def set_name(message: types.Message, state: FSMContext):
    if not message.text:
        return await message.bot.send_message(message.from_user.id, "Пожалуйста, введите свое имя")
    tg_user = message.from_user
    await Player.objects.acreate(tg_id=tg_user.id, name=message.text)

    await message.bot.send_message(tg_user.id, f"Приятно познакомиться, {message.text}!")

    await message.bot.send_message(tg_user.id, "Теперь укажи свой NTRP-рейтинг",
                                   reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegistrationsState.ntrp)


async def set_ntrp(message: types.Message, state: FSMContext):
    if not message.text:
        return await message.bot.send_message(message.from_user.id, "Пожалуйста, введите свой NTRP-рейтинг")

    tg_user = message.from_user
    player = await Player.objects.aget(tg_id=tg_user.id)

    state_data = await state.get_data()
    state_data['id'] = player.id
    player.ntrp = message.text
    player.asave()

    await message.bot.send_message(tg_user.id, f"Спасибо за регистрацию, {player.name}!")

    await state.set_state()
    await basic.main_menu(message)
