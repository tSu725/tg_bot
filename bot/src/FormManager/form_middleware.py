from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject
from src.FormManager.FormManager import FormManager

class FormMiddleware:
    def __init__(self, form: FormManager):
        self.form = form

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["form"] = self.form
        return await handler(event, data)