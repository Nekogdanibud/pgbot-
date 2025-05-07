from typing import Callable, Dict, Awaitable, Any, Union
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, Update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from core.database.crud import get_user_by_telegram_id, create_user
from core.database.model import User
import logging

logger = logging.getLogger(__name__)

class RoleMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker[AsyncSession]):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.debug(f"RoleMiddleware called for event: {event}")
        data.update({"user": None, "role": "USER"})

        # Извлекаем конкретное событие из Update
        if isinstance(event, Update):
            if event.message:
                actual_event = event.message
            elif event.callback_query:
                actual_event = event.callback_query
            else:
                logger.debug(f"Skipping middleware: unsupported event type in Update: {event}")
                return await handler(event, data)
        else:
            actual_event = event

        # Проверяем, что событие — Message или CallbackQuery и есть from_user
        if not isinstance(actual_event, (Message, CallbackQuery)) or not actual_event.from_user:
            logger.warning(f"Skipping middleware: event={actual_event}, from_user={getattr(actual_event, 'from_user', None)}")
            return await handler(event, data)

        user = actual_event.from_user
        telegram_id = user.id
        logger.debug(f"Processing user: telegram_id={telegram_id}")

        try:
            async with self.session_pool() as session:
                async with session.begin():
                    db_user = await get_user_by_telegram_id(session, telegram_id)
                    logger.debug(f"Found user: {db_user}")
                    
                    if not db_user:
                        db_user = await create_user(session, telegram_id, user.username)
                        logger.debug(f"Created user: {db_user}")
                        if db_user:
                            await session.commit()
                        else:
                            logger.error(f"Failed to create user for telegram_id {telegram_id}")
                            await session.rollback()

                    data.update({
                        "user": db_user,
                        "role": db_user.role.upper() if db_user else "USER"
                    })
                    logger.debug(f"Updated data: user={db_user}, role={data['role']}")

        except Exception as e:
            logger.error(f"Middleware error for telegram_id {telegram_id}: {str(e)}", exc_info=True)
            data.update({"user": None, "role": "USER"})

        return await handler(event, data)
