from aiogram import types
from loader import db, dp, bot
from aiogram.dispatcher.storage import FSMContext

@dp.message_handler(text="🆕 Bloglar", state="*")
async def get_blogs(message: types.Message, state: FSMContext):
    print("YESS")