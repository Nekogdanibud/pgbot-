from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from .texts import (
    PROFILE_BUTTON, SUBSCRIPTION_BUTTON, HELP_BUTTON,
    SUPPORT_BUTTON, ADMIN_BUTTON,
    PROFILE_CALLBACK, SUBSCRIPTION_CALLBACK, HELP_CALLBACK,
    SUPPORT_CALLBACK, ADMIN_CALLBACK
)

def get_main_menu(role: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    
    # Основные кнопки первого ряда
    builder.button(text=PROFILE_BUTTON, callback_data=PROFILE_CALLBACK)
    builder.button(text=SUBSCRIPTION_BUTTON, callback_data=SUBSCRIPTION_CALLBACK)
    
    # Кнопки специального доступа
    special_buttons = []
    if role == "SUPPORT":
        special_buttons.append((SUPPORT_BUTTON, SUPPORT_CALLBACK))
    elif role == "ADMIN":
        special_buttons.extend([
            (SUPPORT_BUTTON, SUPPORT_CALLBACK),
            (ADMIN_BUTTON, ADMIN_CALLBACK)
        ])
    
    # Добавляем специальные кнопки
    for text, callback in special_buttons:
        builder.button(text=text, callback_data=callback)
    
    # Кнопка помощи в последнем ряду
    builder.button(text=HELP_BUTTON, callback_data=HELP_CALLBACK)
    
    # Распределение кнопок: 
    # 1-й ряд: 2 кнопки, 2-й ряд: специальные кнопки, 3-й ряд: 1 кнопка
    builder.adjust(2, *[2]*len(special_buttons), 1)
    
    return builder.as_markup()
