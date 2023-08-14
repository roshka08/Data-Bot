from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kursga_yozilish = KeyboardButton("📩 Ariza qoldirish")
back_button_info = KeyboardButton("🔙 Orqaga qaytish")
back_main_page = KeyboardButton("🏘 Bosh menyu")

course_enroll = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

course_enroll.add(kursga_yozilish)
course_enroll.add(back_button_info, back_main_page)

phone = KeyboardButton(text="📞 Telefon raqam yuborish", request_contact=True)
enroll_phone = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

enroll_phone.add(phone)