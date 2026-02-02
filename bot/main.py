import asyncio
import os
from aiogram import Bot, Dispatcher
from src.admin_components.admin_router import admin_router
from src.user_components.user_router import user_router
from src.FormManager.FormManager import FormManager
from src.FormManager.form_middleware import FormMiddleware

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    form = FormManager()

    dp.update.middleware(FormMiddleware(form))
    dp.include_routers(admin_router, user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
