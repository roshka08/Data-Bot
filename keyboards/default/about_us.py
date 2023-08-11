from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

maslahat_olish = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✍️ Maslahat olish")]
], resize_keyboard=True)

phone = KeyboardButton(text="📞 Telefon raqam yuborish", request_contact=True)
advice_phone = ReplyKeyboardMarkup(resize_keyboard=True)

advice_phone.add(phone)