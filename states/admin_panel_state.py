from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminPanelState(StatesGroup):
    course_name = State()
    description = State()
    months = State()
    price = State()
    end = State()

class AdminPanelDeleteCourseState(StatesGroup):
    delete_course = State()

class AdminPanelBlogCreate(StatesGroup):
    blog_title = State()
    blog_description = State()
    blog_date = State()
    safe_or_delete = State()
    
class AdminPanelDeleteBlogState(StatesGroup):
    delete_course = State()