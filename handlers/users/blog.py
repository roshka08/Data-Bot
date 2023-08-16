from aiogram import types
from loader import db, dp, bot
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.blog import back_button_markup
from keyboards.default.main_page import main_page
from states.blog_state import Blog

@dp.message_handler(text="🆕 Blog", state="*")
async def get_blogs(message: types.Message, state: FSMContext):
    blogs = await db.select_all_blogs()
    
    if len(blogs) >= 1:
        for item in blogs:
            blog_title = item.get("blog_title")
            blog_description = item.get("blog_description")
            blog_date = item.get('blog_date')

            await bot.send_message(chat_id=message.chat.id, text=f"<i>{blog_date}</i>\n\n<b>{blog_title}</b>\n\n<i>{blog_description}</i>", reply_markup=back_button_markup)
        await Blog.next()
    else:
        await message.answer(text="Yaqin orada hech narsa bo'lmaydi!", reply_markup=back_button_markup)
        await Blog.next()

@dp.message_handler(text="🔙 Orqaga qaytish", state=Blog.go_back)
async def go_back(message: types.Message, state: FSMContext):
    await message.answer(text="Siz bosh menyuga qaytingiz!", reply_markup=main_page)
    await state.finish()