from .auth import router as auth_router
from .root import router as root_router
from .faker import router as faker_router

__all__ = [
    "root_router",
    "auth_router",
    "faker_router"
]
