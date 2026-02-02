from aiogram.filters.callback_data import CallbackData
from enum import StrEnum

class UserAction(StrEnum):
    FILL_SURVEY = 'fill_survey'
    YES_NO_ANSWER = 'yes_no'

class UserCallback(CallbackData, prefix="user"):
    action: UserAction
    value: str | None = None