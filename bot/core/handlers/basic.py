from aiogram import types

from app.database import get_async_session
from app.player.models import Player


# def start(message: types.Message):
#     tg_id = message.from_user.id
#
#     session = get_async_session()
#     try:
#         session.query(Player).get(tg_id=tg_id)
#     except sqlalchemy.expr