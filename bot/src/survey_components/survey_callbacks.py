from aiogram.filters.callback_data import CallbackData
from enum import StrEnum

class SurveyAction(StrEnum):
    ADD_QUESTION =      'add_question'
    EDIT_QUESTION =     'edit_question'
    EDIT_QUESTION_TEXT = 'edit_question_text'
    QUESTION_TYPE = 'edit_type'
    DELETE_QUESTION =   'delete_question'
    BACK = 'back'

class SurveyCallback(CallbackData, prefix='survey'):
    action: SurveyAction