from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload
from core.database.model import User, Subscription, Ticket
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)

# Оригинальные функции остаются без изменений
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
        await session.flush()
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
    """Оригинальный метод получения пользователя (без связанных данных)"""
    try:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя {telegram_id}: {str(e)}", exc_info=True)
        return None

# Новый расширенный метод
async def get_user_full_data(
    session: AsyncSession,
    telegram_id: int
) -> Optional[Tuple[User, List[Subscription], List[Ticket]]]:
    """
    Получение полной информации о пользователе:
    - Возвращает кортеж (User, List[Subscription], List[Ticket])
    - Автоматически обрабатывает пустые коллекции
    """
    try:
        result = await session.execute(
            select(User)
            .options(
                selectinload(User.subscriptions),
                selectinload(User.tickets)
            )
            .where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

        if not user:
            logger.debug(f"Пользователь {telegram_id} не найден")
            return None

        # Обработка пустых коллекций
        subscriptions = user.subscriptions if user.subscriptions else []
        tickets = user.tickets if user.tickets else []

        return (user, subscriptions, tickets)

    except Exception as e:
        logger.error(
            f"Ошибка при получении полных данных пользователя {telegram_id}: {str(e)}",
            exc_info=True
        )
        return None
