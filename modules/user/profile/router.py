from aiogram import Router, F
from .handlers import show_profile
from modules.user.main_menu.texts import PROFILE_CALLBACK

profile_router = Router()

profile_router.callback_query.register(
    show_profile,
    F.data.startswith(PROFILE_CALLBACK)
)
