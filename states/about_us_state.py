from aiogram.dispatcher.filters.state import State, StatesGroup

class AboutUsState(StatesGroup):
    start = State()
    user_phone = State()
    advice = State()