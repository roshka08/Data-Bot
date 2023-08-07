from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_page = ReplyKeyboardMarkup(resize_keyboard=True)

kurslar = KeyboardButton(text="📚 Kurslar")
about_us = KeyboardButton(text="ℹ️ Biz haqimizda")
blog = KeyboardButton(text="🆕 Blog")
kursga_yozilish = KeyboardButton(text="📩 Ariza qoldirish")

main_page.add(kurslar, kursga_yozilish)
main_page.add(blog, about_us)