from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from core.database.model import User
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def create_user(
    session: AsyncSession,
    telegram_id: int,
    username: Optional[str] = None
) -> Optional[User]:
    """Создание пользователя с автоматическим назначением роли 'USER'"""
    try:
        user = User(
            telegram_id=telegram_id,
            username=username
        )
        session.add(user)
        await session.flush()  # Сохраняем объект, чтобы получить ID, но без коммита
        await session.refresh(user)
        logger.info(f"Создан пользователь: {user.telegram_id}")
        return user
    except exc.IntegrityError as e:
        logger.warning(f"IntegrityError при создании пользователя {telegram_id}: {str(e)}")
        await session.rollback()
        return await get_user_by_telegram_id(session, telegram_id)
    except Exception as e:
        logger.error(f"Ошибка при создании пользователя {telegram_id}: {str(e)}", exc_info=True)
        await session.rollback()
        return None

async def get_user_by_telegram_id(
    session: AsyncSession,
    telegram_id: int
) -> Optional[User]:
    try:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя {telegram_id}: {str(e)}", exc_info=True)
        return None
