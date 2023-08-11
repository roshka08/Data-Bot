from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.main_page import main_page
from keyboards.default.about_us import maslahat_olish, advice_phone
from states.about_us_state import AboutUsState

@dp.message_handler(text="ℹ️ Biz haqimizda", state="*")
async def get_about_us(message: types.Message):
    await message.answer(text=f"<b>Bizning qadriyatlar</b>\n\n<b>• Dars jarayonida o'quvchilarga kerakli jihozlar beriladi</b>\n<i>O'quvchilarimiz dars mobaynida kompyuter, kamera, VR ko'zoynak va grafik planshetlar bilan ta'minlanadi. Ular darsdan tashqari vaqtda ham kelib, shug'ullanishlari mumkin.</i>\n\n<b>• Ustozlarimiz katta tajribaga ega</b>\n<i>O'quv markazimizda o'z sohasida 1 yildan 22 yilgacha tajribaga ega ustozlar ta'lim berishadi. Darslarimiz 90% amaliyotga asoslangan.</i>\n\n<b>• Loyihangizni rivojlantirish uchun kuchli kompyuterlar mavjud</b>\n<i>Markazimizda o'z loyihasiga ega o'quvchilar va bitiruvchilar uchun 80 ta iMac kompyuterlaridan birida ishlash imkoniyati yaratilgan.</i>\n\n<b>• O'z hamfikrlaringizni topish uchun bepul kofebreyk tashkil qilingan</b>\n<i>Darslar davomida 15 daqiqa tanaffus qilib, do'stlar orttirish va ko'zlarga dam berish uchun bepul kofebreykka chiqishingiz mumkin.</i>\n\n<b>• IT Park bilan hamkorlikdagi sertifikat beramiz</b>\n<i>Kurs yakunidagi imtihonlardan muvaffaqiyatli o'tgan har bir o'quvchiga IT Park tomonidan tasdiqlangan sertifikat topshiriladi.</i>\n\n<b>• Ish topishingizga yordam beramiz</b>\n<i>Markazimizda zamonaviy sohalar bo'yicha ish vakansiyalarini topib beruvchi Bandlik bo'limi tashkil qilingan.</i>\n\n{'-' * 60}\n<b>Stansiyamiz yoki kurslar haqida chuqurroq bilib olmoqchi bo'lsangiz \"Maslahat olish\" tugmasiga bosing 👇</b>", reply_markup=maslahat_olish)
    await AboutUsState.next()

@dp.message_handler(text="✍️ Maslahat olish", state=AboutUsState.start)
async def get_start_advice(message: types.Message, state: FSMContext):
    await message.answer(text="Telefon raqamni yuboring: ", reply_markup=advice_phone)
    await AboutUsState.next()

@dp.message_handler(state=AboutUsState.user_phone, content_types=["contact"])
async def get_user_phone(message: types.Message, state: FSMContext):
    await state.update_data({"user_phone": message.contact.phone_number})
    await message.answer("Nima haqida maslahat olmoqchisiz / bermoqchisiz: ", reply_markup=types.ReplyKeyboardRemove())
    await AboutUsState.next()

@dp.message_handler(state=AboutUsState.advice)
async def get_user_advice(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    user_phone = data.get('user_phone') 
    user_advice = message.text

    await db.add_advice(user_name=user_name, user_id=user_id, user_phone=user_phone, user_advice=user_advice)
    await message.answer("Siz bilan tez orada bog'lanamiz!", reply_markup=main_page)
    await state.finish()