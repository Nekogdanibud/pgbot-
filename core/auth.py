from sqlalchemy.ext.asyncio import AsyncSession
from core.database.crud import get_user_by_telegram_id, update_user
from core.marzban_api.api import MarzbanAPI
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, marzban_api: MarzbanAPI):
        self.marzban_api = marzban_api

    async def sync_with_marzban(
        self, 
        session: AsyncSession, 
        telegram_id: int
    ) -> Dict[str, Any]:
        result = {
            "marzban_user_exists": False,
            "error": None
        }

        try:
            user = await get_user_by_telegram_id(session, telegram_id)
            if not user:
                result["error"] = "User not found in DB"
                return result

            # Используем telegram_id если username отсутствует
            marzban_username = user.username or str(telegram_id)
            marzban_user = await self.marzban_api.get_user(marzban_username)
            
            result["marzban_user_exists"] = marzban_user is not None

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Sync error: {str(e)}", exc_info=True)
            
        return result
