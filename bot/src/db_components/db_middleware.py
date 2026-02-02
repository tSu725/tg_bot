from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject
from src.db_components.user_manager import UserManager

class DBMiddleware:
    def __init__(self, user_db: UserManager):
        self.user_db = user_db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["users"] = self.user_db
        return await handler(event, data)