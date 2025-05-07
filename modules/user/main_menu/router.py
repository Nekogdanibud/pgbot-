from aiogram import Router, F
from aiogram.filters import Command
from .handlers import start_command
from core.filters import IsNotBanned
from ..profile.router import profile_router
from .texts import MAIN_MENU_CALLBACK
main_menu_router = Router()
main_menu_router.callback_query.filter(IsNotBanned)
main_menu_router.include_router(profile_router)
# Обработка команды /start
main_menu_router.message.register(
    start_command,
    Command("start"),
    IsNotBanned
)
main_menu_router.callback_query.register(
    start_command,
    F.data == MAIN_MENU_CALLBACK,
    IsNotBanned
)

