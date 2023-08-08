from aiogram import types
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from states.kurs_state import KursState
from keyboards.default.course_enroll import course_enroll

@dp.message_handler(text="📚 Kurslar", state="*")
async def get_courses(message: types.Message, state: FSMContext):
    courses = await db.select_all_course()
    courses_markup = types.InlineKeyboardMarkup(row_width=3)

    for info in courses:
        txt = info.get('course_name')
        courses_markup.insert(types.InlineKeyboardButton(text=txt, callback_data=txt))

    await message.answer('Barcha kurslar:', reply_markup=courses_markup)
    await KursState.next()

@dp.callback_query_handler(state=KursState.course_info)
async def get_course_info(call: types.CallbackQuery, state: FSMContext):
    course_name = call.data
    course_info = await db.select_course(course_name=course_name)

    await call.message.delete()
    await call.message.answer(f"Kurs Nomi: {course_info.get('course_name')} - {course_info.get('months')} oy davom etadi\n\n<i>{course_info.get('description')}</i>\n\nKurs oyiga - {course_info.get('price')}", reply_markup=course_enroll)
    await KursState.next()

@dp.message_handler(text="📩 Ariza qoldirish", state=KursState.course_enroll)
async def get_application(message: types.Message, state: FSMContext):
    await message.answer('👤 Ismingizni kiriting: ')
    await KursState.next()

@dp.message_handler(state=KursState.enroll_user_name)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data({'user_name': message.text})
    await message.answer('📞 Telefon raqamingizni qiriting: ')
    await KursState.next()

@dp.message_handler(state=KursState.enroll_phone)
async def get_user_phone(message: types.Message, state: FSMContext):
    data = state.get_data()
    user_name = data.get('user_name')
    user_phone = message.text

    # useerni databasega qoshishi!