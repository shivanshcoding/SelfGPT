"""
SelfGPT — Database: MongoDB via Motor + Beanie ODM

Provides async MongoDB connection lifecycle management.
"""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import get_settings

_client: AsyncIOMotorClient | None = None


async def init_mongodb():
    """Initialize Motor client and Beanie ODM with all document models."""
    global _client
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.mongodb_url)
    db = _client[settings.mongodb_db_name]

    # Import all document models here to register with Beanie
    from models.user import User
    from models.identity import Identity
    from models.chat import Chat
    from models.message import Message
    from models.memory import Memory
    from models.document import Document
    from models.upload import Upload
    from models.feedback import Feedback
    from models.training_data import TrainingData
    from models.settings import UserSettings

    await init_beanie(
        database=db,
        document_models=[
            User,
            Identity,
            Chat,
            Message,
            Memory,
            Document,
            Upload,
            Feedback,
            TrainingData,
            UserSettings,
        ],
    )


async def close_mongodb():
    """Close the Motor client connection."""
    global _client
    if _client:
        _client.close()
        _client = None


def get_db():
    """Return the active database instance."""
    settings = get_settings()
    if _client is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongodb() first.")
    return _client[settings.mongodb_db_name]
