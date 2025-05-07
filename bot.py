import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.middleware import RoleMiddleware
from core.database.model import Base

# Настройка логгера для SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    # Проверка переменных окружения
    if not (BOT_TOKEN := os.getenv("BOT_TOKEN")) or not (DATABASE_URL := os.getenv("DATABASE_URL")):
        logger.error("Требуемые переменные окружения не установлены!")
        return

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Настройка подключения к БД
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    
    # Создаем таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Инициализация пула сессий
    session_pool = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    # Регистрация middleware
    dp.update.outer_middleware(RoleMiddleware(session_pool=session_pool))

    # Подключение роутеров
    from modules.user.main_menu.router import main_menu_router
    dp.include_router(main_menu_router)

    try:
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        logger.info("Подключения к БД закрыты")

if __name__ == "__main__":
    asyncio.run(main())
