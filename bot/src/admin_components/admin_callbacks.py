from aiogram.filters.callback_data import CallbackData
from enum import StrEnum

class AdminAction(StrEnum):
    SURVEY_MENU = "survey_menu"
    MODERATION = "moderation"
    HISTORY = "history"
    SURVEY_BACK = 'back'

class AdminCallback(CallbackData, prefix="admin"):
    action: AdminAction