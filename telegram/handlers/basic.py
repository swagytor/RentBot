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
        tg_username = await get_player_tg_username(message)
        state_data = await state.get_data()
        state_data['id'] = player.id
        state_data['tg_username'] = tg_username
        await state.set_data(state_data)

        await main_menu(message)

    except Player.DoesNotExist:
        await message.bot.send_message(tg_user.id, "Привет!\n"
                                                   "Меня зовут RentBot, и я буду твоим личным помощником, "
                                                   "когда тебе захочется забронировать корт.\n"
                                                   "Давай для начала познакомимся")

        await state.set_state(state=RegistrationsState.start)

        await start_register(message, state)


async def about(message: types.Message):
    bot_name = await message.bot.get_me()
    await message.answer(f"Привет всем!) На связи @{bot_name.username})\n"
                         "\n"
                         "Я хотел бы рассказать как со мной поладить куда нажимать, "
                         "чтобы нам обоим было хорошо и ответить на вопросы чего вообще происходит то!)\n"
                         "\n"
                         "Для отмены/просмотра игр зайдите во вкладку - Мои Игры\n"
                         "\n"
                         "Посмотреть расписание всех игр вкладка - Все Игры\n"
                         "\n"
                         "Выходные: запись на 2 часа доступна только до 9:15 утра\n"
                         "Будни: запись на 2 часа доступна только до 13:45 дня\n"
                         "В остальное время запись возможна только на 1.5 часа или меньше.\n"
                         "\n"
                         "У каждого участника есть возможность записаться только два раза в неделю,"
                         "неделя считается с понедельника по воскресенье\n"
                         "\n"
                         "Супер! Спасибо, что прочитал и Хорошей игры!))\n"
                         "\n"
                         "А, чуть не забыл - Записаться на корт можно во вкладке - Записаться!")


async def main_menu(message: types.Message):
    await message.answer("Вы в Главном меню\n"
                         "\n"
                         "Ребята всем привет!, плиизз))\n"
                         "Прочтите краткие инструкции, вы их сможете найти нажав на кнопку 'Информация о боте',"
                         "она будет там же где и кнопка 'Запустить бота'\n"
                         "\n",
                         reply_markup=basic.main_menu_keyboard)


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


async def get_player_tg_username(message: types.Message):
    tg_id = message.from_user.id
    player = await Player.objects.aget(tg_id=tg_id)

    if not player.tg_username or player.tg_username != message.from_user.username:
        player.tg_username = message.from_user.username
        await player.asave()

    return message.from_user.username


# async def test(message: types.Message):
#     calendar = CustomCalendar()
#     calendar = await calendar.start_calendar()
#
#     await message.answer("Выберите дату:", reply_markup=calendar)
