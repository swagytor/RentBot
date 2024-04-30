import requests
from aiogram import types


async def my_events(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Мои игры")

    response = requests.get('http://127.0.0.1:8000/api/events/my_events/',
                            params={'tg_id': message.from_user.id})

    if response.status_code == 200:
        response = response.json()

        for event in response:
            date, start_time = event['start_date'].split()
            _, end_time = event['end_date'].split()

            text = (f"Дата: {date}\n"
                    f"Время: {start_time} - {end_time}\n"
                    f"Корт: {event['_court']}\n")

            await message.bot.send_message(message.from_user.id, text)
