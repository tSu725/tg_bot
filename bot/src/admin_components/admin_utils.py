from aiogram.types import Message, CallbackQuery
import src.admin_components.admin_keyboards as kb

async def show_admin_main_menu(callback_or_message: CallbackQuery | Message):
    text, keyboard = 'Admin menu:', kb.admin_main_menu_inline_keyboard
    if isinstance(callback_or_message, CallbackQuery):
        await callback_or_message.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
        await callback_or_message.answer()
    else:
        await callback_or_message.answer(
            text=text,
            reply_markup=keyboard
        )