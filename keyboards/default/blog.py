from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

back_button = KeyboardButton("🔙 Orqaga qaytish")

back_button_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_button_markup.add(back_button)