from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

yes = InlineKeyboardButton(text="✅ Ha", callback_data="yes")
no = InlineKeyboardButton(text="❌ Yo'q", callback_data="no")

yes_or_no = InlineKeyboardMarkup(row_width=2)
yes_or_no.add(yes, no)
