from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    choosing_year = State()
    choosing_book = State()
    choosing_variant = State()
    solving_tasks = State()