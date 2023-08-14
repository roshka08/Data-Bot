from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

number_markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
back_admin_page = KeyboardButton("🏘 Admin menyu")

for num in range(1, 10):
    number_markup.insert(str(num))

number_markup.add(back_admin_page)