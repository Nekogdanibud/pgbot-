from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from typing import Union, Optional

class RoleFilter(BaseFilter):
    def __init__(self, required_role: str):
        self.required_role = required_role.upper()

    async def __call__(
        self, 
        event: Union[Message, CallbackQuery], 
        role: Optional[str] = None, 
        **kwargs
    ) -> bool:
        return role and role.upper() == self.required_role

class HasAnyRole(BaseFilter):
    def __init__(self, roles: list | tuple | set):
        self.allowed_roles = {r.upper() for r in roles}

    async def __call__(
        self, 
        event: Union[Message, CallbackQuery], 
        role: Optional[str] = None, 
        **kwargs
    ) -> bool:
        return role and role.upper() in self.allowed_roles

# Готовые экземпляры фильтров
IsAdmin = RoleFilter("ADMIN")
IsSupport = RoleFilter("SUPPORT")
IsUser = RoleFilter("USER")
IsBanned = RoleFilter("BANNED")
IsStaff = HasAnyRole({"ADMIN", "SUPPORT"})
IsNotBanned = HasAnyRole({"USER", "ADMIN", "SUPPORT"})
