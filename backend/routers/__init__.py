from .auth import router as auth_router
from .chats import router as chats_router
from .messages import router as messages_router
from .identities import router as identities_router
from .ws import router as ws_router
from .stubs import (
    memory_router,
    rag_router,
    uploads_router,
    training_router,
    admin_router,
)

__all__ = [
    "auth_router",
    "chats_router",
    "messages_router",
    "identities_router",
    "ws_router",
    "memory_router",
    "rag_router",
    "uploads_router",
    "training_router",
    "admin_router",
]
