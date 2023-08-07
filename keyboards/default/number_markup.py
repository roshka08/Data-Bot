from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

number_markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

for num in range(1, 10):
    number_markup.insert(str(num))
