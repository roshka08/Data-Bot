from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminPanelState(StatesGroup):
    course_name = State()
    description = State()
    months = State()
    price = State()