from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os  

# Загрузка переменных окружения
load_dotenv()

# Получаем URL БД из .env
DATABASE_URL = os.getenv("DATABASE_URL")  # Добавляем эту строку

#Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL)

Base = declarative_base()

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)
