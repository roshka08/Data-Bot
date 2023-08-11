from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_page = ReplyKeyboardMarkup(resize_keyboard=True)

kurslar = KeyboardButton(text="📚 Kurslar")
about_us = KeyboardButton(text="ℹ️ Biz haqimizda")
blog = KeyboardButton(text="🆕 Blog")

main_page.add(kurslar)
main_page.add(blog, about_us)