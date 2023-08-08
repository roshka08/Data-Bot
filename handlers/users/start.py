from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS
from utils.extra_datas import make_title
from keyboards.default.main_page import main_page
from aiogram.dispatcher import FSMContext

@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    """
            MARKDOWN V2                     |     HTML
    link:   [Google](https://google.com/)   |     <a href='https://google.com/'>Google</a>
    bold:   *Qalin text*                    |     <b>Qalin text</b>
    italic: _Yotiq shriftdagi text_         |     <i>Yotiq shriftdagi text</i>



                    **************     Note     **************
    Markdownda _ * [ ] ( ) ~ ` > # + - = | { } . ! belgilari to'g'ridan to'g'ri ishlatilmaydi!!!
    Bu belgilarni ishlatish uchun oldidan \ qo'yish esdan chiqmasin. Masalan  \.  ko'rinishi . belgisini ishlatish uchun yozilgan.
    """

    await state.finish()
    full_name = message.from_user.full_name
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=full_name,
            username=message.from_user.username,
        )
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"[{make_title(user['full_name'])}](tg://user?id={user['telegram_id']}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\."
        await bot.send_message(chat_id=ADMINS[0], text=msg, parse_mode=types.ParseMode.MARKDOWN_V2)
    else:
        await bot.send_message(chat_id=ADMINS[0], text=f"[{make_title(full_name)}](tg://user?id={message.from_user.id}) bazaga oldin qo'shilgan", disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN_V2)
    await message.answer(f"Xush kelibsiz\! {make_title(full_name)}", parse_mode=types.ParseMode.MARKDOWN_V2)
    await message.answer(f"*Biz sizni:\n*• _IT bo\'yicha_\n• _Talabgir sohalarada_\n• _Ingliz titi bo\'yicha_\n• _Marketing bo\'yicha_\n• _Media yonalishlarida_\n\n*BILIMGA TO\'LDIRAMIZ\!*\n\nDATA endi \- ta\'lim stansiyasi", reply_markup=main_page, parse_mode=types.ParseMode.MARKDOWN_V2)