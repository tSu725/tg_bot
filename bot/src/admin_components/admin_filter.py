# src/admin_components/admin_filter.py
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
import os

class AdminFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user_id = event.from_user.id if isinstance(event, Message) else event.from_user.id
        admin_id_str = os.getenv("ADMIN_ID")
        if not admin_id_str:
            return False
        try:
            return user_id == int(admin_id_str)
        except ValueError:
            return False