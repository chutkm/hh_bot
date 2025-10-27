import asyncio
import uvicorn
from app.api import app as api_app  # Импорт твоего FastAPI приложения
from bot.bot import main as start_bot  # Импорт функции, запускающей бота

async def run_api():
    """Запускаем FastAPI сервер"""
    config = uvicorn.Config(api_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def run_bot():
    """Запускаем aiogram бота"""
    await start_bot()

async def main():
    # Запускаем API и бота параллельно
    await asyncio.gather(
        run_api(),
        run_bot()
    )

if __name__ == "__main__":  
    asyncio.run(main())
