from aiogram.fsm.state import StatesGroup, State

class SurveyFSM(StatesGroup):
    add_question = State()
    edit_question_id = State()
    edit_question_text = State()
    edit_question_type = State()
    delete_question = State()




