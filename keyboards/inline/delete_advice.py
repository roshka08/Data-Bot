from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

delete_button = InlineKeyboardButton(text="🗑 O'chirish", callback_data="delete")
delete_advice = InlineKeyboardMarkup(row_width=1)

delete_advice.add(delete_button)