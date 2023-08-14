from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

back_admin_page_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_admin_page = KeyboardButton("🏘 Admin menyu")

back_admin_page_markup.add(back_admin_page)

add_course = KeyboardButton(text="🆕 Kurs qo'shish")
delete_course = KeyboardButton(text="🗑 Kurs o'chirish")

courses_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
courses_markup.add(add_course, delete_course)
courses_markup.add(back_admin_page)

blog = KeyboardButton(text="🖼 Bloglar")
courses = KeyboardButton(text="📕 Kurslar")
see_all_user = KeyboardButton(text="👁 Userlarni qo'rish")
see_all_enroll_users = KeyboardButton(text="📜 Arizalar")
see_all_advices = KeyboardButton(text="✍️ Maslahatlar")

admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.add(see_all_user)
admin_markup.add(courses, blog)
admin_markup.add(see_all_enroll_users, see_all_advices)

add_blog = KeyboardButton(text="🆕 Blog qo'shish")
delete_blog = KeyboardButton(text="🗑 Blog o'chirish")
blog_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

blog_markup.add(add_blog, delete_blog)
blog_markup.add(back_admin_page)