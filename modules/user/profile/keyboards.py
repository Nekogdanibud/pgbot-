from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from .texts import BACK_BUTTON
from modules.user.main_menu.texts import MAIN_MENU_CALLBACK

def get_profile_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text=BACK_BUTTON, callback_data=MAIN_MENU_CALLBACK)
    return builder.as_markup()
