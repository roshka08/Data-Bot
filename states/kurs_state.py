from aiogram.dispatcher.filters.state import State, StatesGroup

class KursState(StatesGroup):
    course_info = State()
    course_enroll = State()
    enroll_user_name = State()
    enroll_phone = State()