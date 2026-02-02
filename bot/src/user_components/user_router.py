from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from src.FormManager.FormManager import FormManager
from src.user_components.user_callbacks import UserCallback, UserAction
from src.user_components.user_keyboard import user_main_menu_inline_keyboard as user_main_kb, \
user_filling_survey_inline_keyboard as yes_no_kb, user_survey_check_status as status_kb
from src.user_components.user_states import UserFSM
from src.db_components.user_manager import UserManager
from src.db_components.db_middleware import DBMiddleware

user_router = Router(name="user_router")

user_db = UserManager()
user_router.message.middleware(DBMiddleware(user_db))
user_router.callback_query.middleware(DBMiddleware(user_db))

@user_router.message(CommandStart())
async def start(message: Message, users: UserManager):
    if users.get_user_index(message.from_user.id):
        await message.answer(
            text="статус: ",  # zero-width space
            reply_markup=status_kb
        )
    else:
        await message.answer(
            text="Здравствуйте! Заполните анкету.",
            reply_markup=user_main_kb)

async def handler_answers_survey(
    event: Message | CallbackQuery,
    state: FSMContext,
    users: UserManager,
    form: FormManager,
    event_data: UserCallback | None = None,
):
    data = await state.get_data()
    answer = event.text if isinstance(event, Message) else event_data.value
    user_id = event.from_user.id
    question_id = data["question_id"]
    total = data["total_questions"]
    users.add_answer(user_id, question_id, answer)
    if question_id + 1 > total:
        if isinstance(event, Message):
            await event.answer("Анкета отправлена!")
        else:
            await event.message.edit_text("Анкета отправлена!")
        await state.clear()
        return
    next_id = question_id + 1
    next_question = form.get_question_by_id(next_id)
    await state.update_data(question_id=next_id)
    text = (
        f"Вопрос {next_id}/{total}:\n"
        f"{next_question['text']}"
    )
    kb = yes_no_kb if next_question["type"] == "yes_no" else None
    if isinstance(event, Message):
        await event.answer(text, reply_markup=kb)
    else:
        await event.message.edit_text(text, reply_markup=kb)

@user_router.callback_query(UserCallback.filter(F.action == UserAction.FILL_SURVEY))
async def start_filling_survey(callback: CallbackQuery, state: FSMContext, form: FormManager, users: UserManager):
    if len(form) < 1:
        await callback.answer(
            text='Анкеты пока нет',
            reply_markup=user_main_kb
        )
    else:
        users.add_user(callback.from_user.id)
        current_index = 1
        total_questions = len(form)
        question = form.get_question_by_id(current_index)
        await state.set_state(UserFSM.filling_survey)
        await state.update_data(
            total_questions=total_questions,
            question_id=current_index,
        )
        await callback.message.edit_text(
            text=f'Вопрос {current_index}/{total_questions}:\n{question['text']}',
            reply_markup=yes_no_kb if question['type'] == 'yes_no' else None
        )
    await callback.answer()

@user_router.message(UserFSM.filling_survey)
async def survey_text(message: Message, state: FSMContext, users: UserManager, form: FormManager,):
    await handler_answers_survey(
        event=message,
        state=state,
        users=users,
        form=form,
    )

@user_router.callback_query(UserFSM.filling_survey, UserCallback.filter(F.action == UserAction.YES_NO_ANSWER))
async def survey_yes_no(callback: CallbackQuery, callback_data: UserCallback, state: FSMContext, users: UserManager, form: FormManager,):
    await handler_answers_survey(
        event=callback,
        event_data=callback_data,
        state=state,
        users=users,
        form=form,
    )
    await callback.answer()











