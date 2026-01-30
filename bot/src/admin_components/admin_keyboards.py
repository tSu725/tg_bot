from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from aiogram.utils.keyboard import InlineKeyboardBuilder # для того чтобы кнопки могли быть не статик

from src.admin_components.admin_callbacks import AdminCallback, AdminAction

admin_main_menu_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Анкета',
            callback_data=AdminCallback(action=AdminAction.SURVEY_MENU).pack()
        ),
        InlineKeyboardButton(
          text='Модерация',
          callback_data=AdminCallback(action=AdminAction.MODERATION).pack()
        ),],
        [InlineKeyboardButton(
            text='История решений',
            callback_data=AdminCallback(action=AdminAction.HISTORY).pack()
        )]
    ]
)

