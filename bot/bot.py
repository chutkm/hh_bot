import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.config import API_TOKEN
from bot.handlers import router
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router=router)
     # 👇 Устанавливаем список доступных команд
    await bot.set_my_commands([
        BotCommand(command="start", description="Приветствие и описание возможностей"),
        BotCommand(command="resume", description="Отправить резюме (PDF/DOCX)"),
        BotCommand(command="search", description="Показать примеры вакансий"),
    ])
    print("Бот запущен...")
    await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(main())
