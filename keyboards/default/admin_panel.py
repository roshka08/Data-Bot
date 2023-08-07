from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


add_course = KeyboardButton(text="🆕 Kurs qo'shish")
add_blog = KeyboardButton(text="🖼 Blog qo'shish")
see_all_user = KeyboardButton(text="👁 Userlarni qo'rish")

admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.add(see_all_user)
admin_markup.add(add_course, add_blog)
