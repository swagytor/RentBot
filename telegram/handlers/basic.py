from aiogram import types
from aiogram.fsm.context import FSMContext

from players.models import Player
from telegram.buttons import basic
from telegram.handlers.registration import start_register
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
    await message.answer("Вы в Главном меню\n"
                         "\n"
                         "Для отмены/просмотра игр зайдите во вкладку Мои Игры\n"
                         "\n"
                         "Посмотреть расписание всех игр - вкладка Все Игры\n"
                         "\n"
                         "Выходные: запись на 2 часа до 9 утра "
                         "Будни: запись на 2 часа до 14 дня\n"
                         "В остальное время запись возмонжна только на 1.5 часа", reply_markup=basic.main_menu_keyboard)


async def redirect_to_bot(message: types.Message, state: FSMContext):
    bot_name = await message.bot.get_me()
    await state.set_state(None)
    await message.answer(f'Для записи на корт пишите в личку бота @{bot_name.username}',
                         reply_markup=types.ReplyKeyboardRemove())


async def redirect_to_bot_callback(call: types.CallbackQuery, state: FSMContext):
    bot_name = await call.bot.get_me()
    await state.set_state(None)
    await call.message.answer(f'Для записи на корт пишите в личку бота @{bot_name.username}',
                              reply_markup=types.ReplyKeyboardRemove())

# async def test(message: types.Message):
#     calendar = CustomCalendar()
#     calendar = await calendar.start_calendar()
#
#     await message.answer("Выберите дату:", reply_markup=calendar)
