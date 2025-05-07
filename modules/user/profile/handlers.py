from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from core.database.crud import get_user_full_data
from .texts import PROFILE_TEXT
from .keyboards import get_profile_kb
from core.database.database import async_session
import logging

logger = logging.getLogger(__name__)

async def show_profile(callback: CallbackQuery):
    """Обработчик показа профиля пользователя"""
    try:
        # Убираем индикатор загрузки сразу
        await callback.answer()

        async with async_session() as session:
            user_data = await get_user_full_data(session, callback.from_user.id)
            
            if not user_data:
                return await callback.answer("❌ Ошибка загрузки профиля", show_alert=True)
            
            user, subscriptions, _ = user_data
            
            profile_text = PROFILE_TEXT.format(
                username=f"@{user.username}" if user.username else "Не установлен",
                balance=getattr(user, 'balance', 0),
                subscriptions_count=len(subscriptions)
            )
            try:
                # Редактируем сообщение
                await callback.message.edit_text(
                    text=profile_text,
                    reply_markup=get_profile_kb()
                )
            except TelegramBadRequest:
                # Если сообщение не изменилось, игнорируем
                pass
                
    except Exception as e:
        logger.error(f"Ошибка в show_profile: {str(e)}", exc_info=True)
        await callback.answer("⚠️ Произошла ошибка при загрузке профиля", show_alert=True)
