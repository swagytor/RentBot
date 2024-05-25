from aiogram.fsm.state import StatesGroup, State


class EventState(StatesGroup):
    main_menu = State()
    select_court = State()
    select_date = State()
    select_all_events_date = State()
    select_start_time = State()
    select_end_time = State()
    create_event = State()
