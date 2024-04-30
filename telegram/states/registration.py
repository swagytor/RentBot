from aiogram.fsm.state import State, StatesGroup


class RegistrationsState(StatesGroup):
    start = State()
    name = State()
    ntrp = State()

