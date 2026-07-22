"""
SelfGPT — Service: Chat

CRUD logic for chat sessions.
"""

from typing import List, Optional
from fastapi import HTTPException, status
from models.chat import Chat
from models.user import User
from schemas.chat import CreateChatRequest, UpdateChatRequest


class ChatService:
    @staticmethod
    async def create_chat(user: User, data: CreateChatRequest) -> Chat:
        """Create a new chat session."""
        chat = Chat(
            user_id=str(user.id),
            identity_id=data.identity_id,
            title=data.title or "New Chat"
        )
        await chat.insert()
        return chat

    @staticmethod
    async def list_chats(
        user: User,
        folder: Optional[str] = None,
        is_archived: bool = False,
        is_deleted: bool = False,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[List[Chat], int]:
        """List user's chats with filtering."""
        query = {
            "user_id": str(user.id),
            "is_archived": is_archived,
            "is_deleted": is_deleted,
        }
        if folder:
            query["folder"] = folder
        if search:
            query["title"] = {"$regex": search, "$options": "i"}

        chats = await Chat.find(query).sort("-updated_at").skip(skip).limit(limit).to_list()
        total = await Chat.find(query).count()
        return chats, total

    @staticmethod
    async def get_chat(chat_id: str, user: User) -> Chat:
        """Get a specific chat belonging to the user."""
        chat = await Chat.get(chat_id)
        if not chat or chat.user_id != str(user.id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )
        return chat

    @staticmethod
    async def update_chat(chat_id: str, user: User, data: UpdateChatRequest) -> Chat:
        """Update chat metadata."""
        chat = await ChatService.get_chat(chat_id, user)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(chat, key, value)
        await chat.save()
        return chat

    @staticmethod
    async def delete_chat(chat_id: str, user: User) -> None:
        """Soft delete a chat."""
        chat = await ChatService.get_chat(chat_id, user)
        chat.is_deleted = True
        await chat.save()

    @staticmethod
    async def restore_chat(chat_id: str, user: User) -> Chat:
        """Restore a soft-deleted chat."""
        chat = await ChatService.get_chat(chat_id, user)
        chat.is_deleted = False
        await chat.save()
        return chat

    @staticmethod
    async def permanently_delete_chat(chat_id: str, user: User) -> None:
        """Hard delete a chat and all its messages."""
        chat = await ChatService.get_chat(chat_id, user)
        
        # Delete associated messages
        from models.message import Message
        await Message.find(Message.chat_id == str(chat.id)).delete()
        
        # Delete the chat itself
        await chat.delete()
