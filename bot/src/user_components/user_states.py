from aiogram.fsm.state import StatesGroup, State

class UserFSM(StatesGroup):
    filling_survey = State()