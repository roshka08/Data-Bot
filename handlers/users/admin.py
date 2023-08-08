import asyncio
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from keyboards.default.admin_panel import admin_markup
from keyboards.default.number_markup import number_markup
from keyboards.inline.yes_or_no import yes_or_no
from states.admin_panel_state import AdminPanelState
from aiogram.dispatcher import FSMContext


# @dp.message_handler(text="/reklama", user_id=ADMINS)
# async def send_ad_to_all(message: types.Message):
#     users = await db.select_all_users()
#     for user in users:
#         user_id = user[-1]
#         await bot.send_message(chat_id=user_id, text="@BekoDev kanaliga obuna bo'ling!")
#         await asyncio.sleep(0.05)


@dp.message_handler(text="/admin", user_id=ADMINS, state="*")
async def get_admin_panel(message: types.Message):
    await message.answer('Siz admin paneldasiz!', reply_markup=admin_markup)

@dp.message_handler(text="👁 Userlarni qo'rish", user_id=ADMINS, state="*")
async def get_all_users(message: types.Message, state: FSMContext):
    users = await db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[-1])
        name.append(user[1])
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

@dp.message_handler(text="🆕 Kurs qo'shish", user_id=ADMINS, state="*")
async def create_course(message: types.Message, state: FSMContext):
    await message.answer(text="Kursni nomini kiriting:", reply_markup=ReplyKeyboardRemove())
    await AdminPanelState.next()

@dp.message_handler(user_id=ADMINS, state=AdminPanelState.course_name)
async def course_name(message: types.Message, state: FSMContext):
    await state.update_data({"course_name": message.text})
    await message.answer(text="Kurs haqida ma'lumotlar: ")
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

callback_data = ['yes', 'no']
@dp.callback_query_handler(text=callback_data, state="*")
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

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("Baza tozalandi!")
