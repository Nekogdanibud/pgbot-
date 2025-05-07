from aiogram import F
from aiogram.types import Message, CallbackQuery
from .texts import MAIN_MENU_TEXT
from .keyboards import get_main_menu
from typing import Union
import logging

logger = logging.getLogger(__name__)

async def start_command(event: Union[Message, CallbackQuery], role: str):
    """Обработчик команды /start и возврата в главное меню"""
    try:
        if isinstance(event, Message):
            # Для новых сообщений
            await event.answer(
                text=MAIN_MENU_TEXT,
                reply_markup=get_main_menu(role)
            )
        else:
            # Для callback-запросов
            await event.message.edit_text(
                text=MAIN_MENU_TEXT,
                reply_markup=get_main_menu(role)
            )
            await event.answer()  # Убираем индикатор загрузки

    except Exception as e:
        logger.error(f"Ошибка в start_command: {str(e)}")
        if isinstance(event, CallbackQuery):
            await event.answer("⚠️ Ошибка загрузки меню", show_alert=True)
