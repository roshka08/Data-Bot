from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


add_course = KeyboardButton(text="🆕 Kurs qo'shish")
delete_course = KeyboardButton(text="🗑 Kurs o'chirish")

courses_markup = ReplyKeyboardMarkup(keyboard=[[add_course], [delete_course]], resize_keyboard=True, row_width=2)

add_blog = KeyboardButton(text="🖼 Bloglar")
courses = KeyboardButton(text="📕 Kurslar")
see_all_user = KeyboardButton(text="👁 Userlarni qo'rish")
see_all_enroll_users = KeyboardButton(text="📜 Arizalar")
see_all_advices = KeyboardButton(text="✍️ Maslahatlar")

admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.add(see_all_user)
admin_markup.add(courses, add_blog)
admin_markup.add(see_all_enroll_users, see_all_advices)
