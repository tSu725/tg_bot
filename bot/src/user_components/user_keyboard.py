from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from src.user_components.user_callbacks import UserCallback, UserAction


user_main_menu_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Заполнить анкету',
            callback_data=UserCallback(action=UserAction.FILL_SURVEY).pack()
        )]
    ]
)

user_filling_survey_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Да',
            callback_data=UserCallback(action=UserAction.YES_NO_ANSWER, value='yes').pack()
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data=UserCallback(action=UserAction.YES_NO_ANSWER, value='no').pack()
        )]
    ]
)

user_survey_check_status = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Статус")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

