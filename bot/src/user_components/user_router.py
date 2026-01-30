# user_router.py
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

user_router = Router(name="user_router")

@user_router.message(CommandStart())
async def cmd_start_user(message: Message):
    await message.answer("Ты обычный пользователь 👤")


