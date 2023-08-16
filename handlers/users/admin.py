import asyncio
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
from loader import dp, db, bot
from utils.extra_datas import make_title
import pandas as pd
from keyboards.default.admin_panel import admin_markup, courses_markup, blog_markup, back_admin_page_markup
from keyboards.default.number_markup import number_markup
from keyboards.inline.yes_or_no import yes_or_no
from states.admin_panel_state import AdminPanelState, AdminPanelDeleteCourseState, AdminPanelBlogCreate, AdminPanelDeleteBlogState
from aiogram.dispatcher import FSMContext
from keyboards.inline.delete_advice import delete_advice
from datetime import date

# @dp.message_handler(text="/reklama", user_id=ADMINS)
# async def send_ad_to_all(message: types.Message):
#     users = await db.select_all_users()
#     for user in users:
#         user_id = user[-1]
#         await bot.send_message(chat_id=user_id, text="@BekoDev kanaliga obuna bo'ling!")
#         await asyncio.sleep(0.05)

@dp.message_handler(text="🏘 Admin menyu", state="*")
async def to_admin_page(message: types.Message, state: FSMContext):
    await message.answer("Siz admin menyudasiz!", reply_markup=admin_markup)
    await state.finish()

@dp.message_handler(text="/admin", user_id=ADMINS, state="*")
async def get_admin_panel(message: types.Message):
    await message.answer('Siz admin paneldasiz!', reply_markup=admin_markup)

user_name = []

@dp.message_handler(text="👁 Userlarni qo'rish", user_id=ADMINS, state="*")
async def get_all_users(message: types.Message, state: FSMContext):
    users = await db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[-1])
        name.append(user[1])
        user_name.append(user[1])

    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 150:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
            await state.finish()
    else:
        await bot.send_message(message.chat.id, df)
        await state.finish()

@dp.message_handler(text="📕 Kurslar", state="*")
async def get_course_add_or_delete(message: types.Message, state: FSMContext):
    await message.answer(text="Tanlang: ", reply_markup=courses_markup)
    await AdminPanelState.next()

@dp.message_handler(text="🆕 Kurs qo'shish", user_id=ADMINS, state="*")
@dp.message_handler(text="🗑 Kurs o'chirish", user_id=ADMINS, state="*")
async def create_course(message: types.Message, state: FSMContext):
    if message.text == "🗑 Kurs o'chirish":
        courses = await db.select_all_course()
        courses_markup = types.InlineKeyboardMarkup(row_width=3)
        for info in courses:
            txt = info.get('course_name')
            courses_markup.insert(types.InlineKeyboardButton(text=txt, callback_data=txt))
        await message.answer("Qaysi kursni o'chirmoqchisiz:", reply_markup=courses_markup)
        await AdminPanelDeleteCourseState.delete_course.set()
    else:
        await message.answer(text="Kursni nomini kiriting:", reply_markup=ReplyKeyboardRemove())
        await AdminPanelState.course_name.set()

@dp.callback_query_handler(state=AdminPanelDeleteCourseState.delete_course, user_id=ADMINS)
async def delete_course(call: types.CallbackQuery, state: FSMContext):
    course = call.data
    await db.delete_course(course_name=course)
    await call.message.delete()
    await call.message.answer(text="Kurs o'chdi!", reply_markup=admin_markup)
    await state.finish()

@dp.message_handler(user_id=ADMINS, state=AdminPanelState.course_name)
async def course_name(message: types.Message, state: FSMContext):
    await state.update_data({"course_name": message.text})
    await message.answer(text="Kurs haqida ma'lumotlar: ", reply_markup=back_admin_page_markup)
    await AdminPanelState.next()

@dp.message_handler(user_id=ADMINS, state=AdminPanelState.description)
async def course_description(message: types.Message, state: FSMContext):
    await state.update_data({"description": message.text})
    await message.answer(text="Kurs qancha oy davom etadi: ", reply_markup=number_markup)
    await AdminPanelState.next()

@dp.message_handler(user_id=ADMINS, state=AdminPanelState.months)
async def course_month(message: types.Message, state: FSMContext):
    await state.update_data({"months": message.text})
    await message.answer(text="Kursni narxini kiriting: ", reply_markup=ReplyKeyboardRemove())
    await AdminPanelState.next()

@dp.message_handler(user_id=ADMINS, state=AdminPanelState.price)
async def course_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    course_name = data.get('course_name')
    course_description = data.get('description')
    course_months = data.get('months')
    course_price = message.text

    await state.update_data({'course_price': course_price})
    await message.answer(text=f"Course Params:\nCourse Name: {course_name}\nCourse Desription: {course_description}\nCourse Momths: {course_months} oy\nCourse Price: {course_price} so'm / oyiga\n\n<b>Kurs to'gri kiritilganmi?</b>", reply_markup=yes_or_no)
    await AdminPanelState.next()

callback_data = ['yes', 'no']
@dp.callback_query_handler(text=callback_data, state=AdminPanelState.end)
async def get_course_params(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    course_name = data.get('course_name')
    course_description = data.get('description')
    course_months = data.get('months')
    course_price = data.get("course_price")
    
    if call.data == "yes":
        await call.message.delete()
        await db.add_course(course_name=course_name, description=course_description, months=course_months, price=course_price)
        await call.message.answer('Sizning kursingiz qoshildi!', reply_markup=admin_markup)
    else:
        await call.message.delete()
        await call.message.answer("Sizning kursingiz o'chirildi!", reply_markup=admin_markup)
    await state.finish()

@dp.message_handler(text="📜 Arizalar", user_id=ADMINS, state="*")
async def get_all_enroll_users(message: types.Message, state: FSMContext):
    all_enroll_users = await db.select_all_enroll_users()

    course_name = []
    user_name = []
    user_phone = []

    for user in all_enroll_users:
        course_name.append(user[-1])
        user_name.append(user[1])
        user_phone.append(user[2])
    data = {
        "Name": user_name,
        "Phone": user_phone,
        "Course": course_name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)

    if len(df) > 150:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
            await state.finish()
    else:
        await bot.send_message(message.chat.id, df)
        await state.finish()

@dp.message_handler(text="✍️ Maslahatlar", state="*", user_id=ADMINS)
async def get_all_advices(message: types.Message):
    advices = await db.select_all_advices()
    for user in advices:
        id = user.get('id')
        user_name = user.get('user_name')
        user_id = user.get('user_id')
        user_phone = user.get('user_phone')
        user_advice = user.get('user_advice')

        await bot.send_message(message.chat.id, text=f"{id}\. [{make_title(user_name)}](tg://user?id={user_id})\nPhone: \{user_phone}\nMaslahat: {user_advice}", parse_mode=types.ParseMode.MARKDOWN_V2, reply_markup=delete_advice)

@dp.callback_query_handler(text="delete")
async def advice_delete(call: types.CallbackQuery):
    await call.message.delete()
    user_advice = call.message.text[41:]
    await db.delete_advice(user_advice=user_advice)
    await call.message.answer(text="O'chirirldi!", reply_markup=admin_markup)

@dp.message_handler(text="🖼 Bloglar", state="*", user_id=ADMINS)
async def get_blogs(message: types.Message, state: FSMContext):
    await message.answer(text="Tanlang: ", reply_markup=blog_markup)
    await AdminPanelBlogCreate.blog_title.set()

@dp.message_handler(text="🆕 Blog qo'shish", state=AdminPanelBlogCreate.blog_title, user_id=ADMINS)
@dp.message_handler(text="🗑 Blog o'chirish", state=AdminPanelBlogCreate.blog_title, user_id=ADMINS)
async def add_or_delete(message: types.Message, state: FSMContext):
    if message.text == "🗑 Blog o'chirish":
        courses = await db.select_all_blogs()
        courses_markup = types.InlineKeyboardMarkup(row_width=3)
        for info in courses:
            txt = info.get('blog_title')
            courses_markup.insert(types.InlineKeyboardButton(text=txt, callback_data=txt))
        await message.answer("Qaysi kursni o'chirmoqchisiz:", reply_markup=courses_markup)
        await AdminPanelDeleteBlogState.delete_course.set()
    else:
        await message.answer(text="Blogni sarlavhasini yozing: ", reply_markup=types.ReplyKeyboardRemove())
        await AdminPanelBlogCreate.next()

@dp.callback_query_handler(state=AdminPanelDeleteBlogState.delete_course, user_id=ADMINS)
async def delete_blog(call: types.CallbackQuery, state: FSMContext):
    blog = call.data
    await db.delete_blog(blog_title=blog)
    await call.message.delete()
    await call.message.answer(text="Blog o'chdi!", reply_markup=admin_markup)
    await state.finish()

@dp.message_handler(state=AdminPanelBlogCreate.blog_description, user_id=ADMINS)
async def get_blog_description(message: types.Message, state: FSMContext):
    await state.update_data({"blog_title": message.text})
    await message.answer(text="Blogni ma'lumotlarini kiriting: ", reply_markup=back_admin_page_markup)
    await AdminPanelBlogCreate.next()

@dp.message_handler(state=AdminPanelBlogCreate.blog_date, user_id=ADMINS)
async def get_blog_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    blog_title = data.get("blog_title")
    blog_description = message.text
    today = date.today()
    month = today.strftime("%B")
    blog_date = format(f"{today.day}-{month}, {today.year}")
    await state.update_data({"blog_title": blog_title, "blog_description": blog_description, "blog_date": blog_date})
    await message.answer(text=f"Blog Nomi: {blog_title}\nBlog Ma'lumoti: {blog_description}\nBlog Date: {blog_date}", reply_markup=yes_or_no)
    await AdminPanelBlogCreate.next()

@dp.callback_query_handler(text=callback_data, state=AdminPanelBlogCreate.safe_or_delete, user_id=ADMINS)
async def get_safe_or_delete(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == "yes":
        data = await state.get_data()
        blog_title = data.get('blog_title')
        blog_description = data.get('blog_description')
        blog_date = data.get('blog_date') 
        await call.message.answer(text="Sizning blogingiz qo'shildi!", reply_markup=admin_markup)
        await db.add_blog(blog_title=blog_title, blog_description=blog_description, blog_date=blog_date)
    else:
        await call.message.answer(text="Siznig blogingiz o'chirildi!", reply_markup=admin_markup)
        await state.finish()

@dp.message_handler(text="👤 Adminlar", state="*", user_id=ADMINS)
async def get_all_admins(message: types.Message, state: FSMContext):
    admin_id = []
    for id in ADMINS:    
        admin_id.append(f"[{make_title('ADMIN')}](tg://user?id={id})")
    data = {
        "ADMINS": admin_id
    }
    
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 150:
        for x in range(1, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50], parse_mode=types.ParseMode.MARKDOWN_V2)
            await state.finish()
    else:
        await bot.send_message(message.chat.id, df, parse_mode=types.ParseMode.MARKDOWN_V2)
        await state.finish()

@dp.message_handler(text="/cleandb", user_id=ADMINS[0])
async def get_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("Baza tozalandi!")
