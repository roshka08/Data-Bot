from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

maslahat_olish = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✍️ Maslahat olish")],
    [KeyboardButton("🔙 Orqaga qaytish")]
], resize_keyboard=True)

phone = KeyboardButton(text="📞 Telefon raqam yuborish", request_contact=True)
back_button = KeyboardButton(text="🔙 Orqaga qaytish")
back_main_page = KeyboardButton("🏘 Bosh menyu")

advice_phone = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
advice_phone.add(phone)
advice_phone.add(back_main_page)