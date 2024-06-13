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
        await message.bot.send_message(tg_user.id, "Привет!😀\n"
                                                   "Меня зовут RentBot, и я буду твоим личным помощником, "
                                                   "когда тебе захочется забронировать корт.\n"
                                                   "Давай для начала познакомимся")

        await state.set_state(state=RegistrationsState.start)

        await start_register(message, state)


async def about(message: types.Message):
    bot_name = await message.bot.get_me()
    await message.answer(f"Привет всем!) На связи 👾 @{bot_name.username})\n"
                         "\n"
                         "Я хотел бы рассказать как со мной поладить куда нажимать, "
                         "чтобы нам обоим было хорошо🥰 и ответить на вопросы чего вообще происходит то!😇)\n"
                         "\n"
                         "Для отмены/просмотра игр зайдите во вкладку - ⚔Мои Игры⚔\n"
                         "\n"
                         "Посмотреть расписание всех игр вкладка - 📜Все Игры📜\n"
                         "\n"
                         "Выходные: запись на 2 часа доступна только до 9 утра🕘\n"
                         "Будни: запись на 2 часа доступна только до 13:30 дня🕑\n"
                         "В остальное время запись возможна только на 1.5 часа или меньше.😓\n"
                         "\n"
                         "У каждого участника есть возможность записаться только два раза в неделю😭,"
                         "неделя считается с понедельника по воскресенье🤓\n"
                         "\n"
                         "Большая просьба - Если не получается придти в записанное время, пожалуйста,"
                         "старайтесь отменять игры заранее!🙌 Все участники сообщества будут вам признательны☺!\n"
                         "\n"
                         "Супер! Спасибо, что прочитал и Хорошей игры!😍))\n"
                         "\n"
                         "А, чуть не забыл - Записаться на корт можно во вкладке - 🎾Записаться!🎾\n",
                         reply_markup=basic.start_button)


async def get_donate(message: types.Message):
    player = await Player.objects.aget(tg_id=415965166)
    await message.answer(f"<b>Дорогие пользователи нашего бота!</b>\n"
                         f"\n"
                         f"Хочу выразить вам огромную благодарность за то, что вы были с нами весь этот месяц!🥳"
                         f" Ваша поддержка была для нас важным опытом. Мы с удовольствием читали каждое ваше сообщение "
                         f"о нашем боте. Каждый день мы задумывались, как сделать его еще более удобным и интересным для вас. "
                         f"Но к сожалению, наш бот являлся временным решением и совсем скоро он будет отключён и его заменят другим ботом\n"
                         f"\n"
                         f"<b>Отдельное спасибо тем, кто активно делился своими отзывами и помогал нам улучшать его."
                         f" Без вашей помощи этот бот не стал бы таким замечательным, какой он есть сейчас!</b> ❤❤️\n"
                         f"\n"
                         f"Если у вас возникнет желание поддержать наши усилия🙌, вы можете сделать перевод по номеру "
                         f"телефона:\n"
                         f"\n"
                         f"<b>8-904-647-20-73</b>\n"
                         f"<b>Виталий Д.</b>, Тинькофф, Сбер.\n"
                         f"\n"
                         f"Мы обещаем использовать ваши пожертвования с пользой!😇\n"
                         f"Например купим нашему боту пару походов к психотерапевту , все таки было не мало историй,"
                         f" с кем то он должен ими поделиться!))\n"
                         f"Или пару бургеров , чтобы просто заесть стресс 😋 ))\n"
                         f"\n"
                         f"Спасибо вам за вашу верность и поддержку ! <b>Вы просто лучшие! </b>🌟\n"
                         f"\n"
                         f"Если у вас есть какие то вопросы, пожелания, предложения можете писать в лс "
                         f"- <a href='https://telegram.me/{player.tg_username}'>{player.name}</a>\n",
                         reply_markup=basic.start_button)


async def main_menu(message: types.Message):
    admin = await admin_check(message)
    text = "Вы в Главном меню\n" \
           "Ребята всем привет! 👋, плиизз🙌))\n" \
           "Прочтите краткие инструкции\правила, вы их сможете найти нажав на кнопку --> /help\n" \
           "Если уже со всем ознакомились нажмите кнопку --> /start 😇\n"

    reply_markup = basic.main_menu_keyboard_admin if admin else basic.main_menu_keyboard_for_donate

    await message.answer(text, reply_markup=reply_markup)


async def redirect_to_bot(message: types.Message, state: FSMContext):
    bot_name = await message.bot.get_me()
    await state.set_state(None)
    await message.answer(f'Для записи на корт пишите в личку бота  @{bot_name.username}',
                         reply_markup=types.ReplyKeyboardRemove())


async def redirect_to_bot_callback(call: types.CallbackQuery, state: FSMContext):
    bot_name = await call.bot.get_me()
    await state.set_state(None)
    await call.message.answer(f'Для записи на корт пишите в личку бота @{bot_name.username}',
                              reply_markup=types.ReplyKeyboardRemove())


async def get_player_tg_username(message: types.Message):
    try:
        tg_id = message.from_user.id
        player = await Player.objects.aget(tg_id=tg_id)

        if not player.tg_username or player.tg_username != message.from_user.username:
            player.tg_username = message.from_user.username
            await player.asave()

        return message.from_user.username

    except Exception as e:
        return f'{e}'


async def admin_check(message: types.Message):
    try:
        value = ''
        black_list = ['MaN1Le', 'kobax12', 'Телеграм', 'Вера', 'Vera_Shuraits', 'slovsky', 'aposazhennikov', 'olegchj']
        if message.from_user.id:
            value = message.from_user.id
        elif message.from_user.username:
            value = message.from_user.username
        elif message.from_user.full_name:
            value = message.from_user.full_name
        return value in black_list

    except Exception as e:
        return False
