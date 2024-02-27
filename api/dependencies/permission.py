from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from loguru import logger

from api.exceptions import CustomException, UnauthorizedException, UnauthorizedAdminException


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user is not None
    

class IsAuthenticatedAdministrator(BasePermission):
    exception = UnauthorizedAdminException
    
    async def has_permission(self, request: Request) -> bool:
        if request.user is None:
            return False
        user_roles = request.user.roles
        for role in user_roles:
            if role.name == 'admin':
                return True

        return False
    



class AlowAll(BasePermission):

    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions
        self.model = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for perm in self.permissions:
            cls = perm()
            if not await cls.has_permission(request=request):
                raise cls.exception
