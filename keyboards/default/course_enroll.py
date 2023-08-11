from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kursga_yozilish = KeyboardButton("📩 Ariza qoldirish")
course_enroll = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

course_enroll.add(kursga_yozilish)

phone = KeyboardButton(text="📞 Telefon raqam yuborish", request_contact=True)
enroll_phone = ReplyKeyboardMarkup(resize_keyboard=True)

enroll_phone.add(phone)