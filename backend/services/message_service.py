"""
SelfGPT — Service: Message

Handles sending messages, triggering the AI, saving to DB.
"""

from typing import List, Optional
from fastapi import HTTPException, status
from models.chat import Chat
from models.message import Message
from models.user import User
from models.identity import Identity
from schemas.message import SendMessageRequest, MessageFeedbackRequest, EditMessageRequest
from services.chat_service import ChatService
from ai.model_manager import get_model_manager
from ai.prompt_builder import build_system_prompt
import json


class MessageService:
    @staticmethod
    async def list_messages(
        chat_id: str,
        user: User,
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None,
    ) -> List[Message]:
        """List messages for a chat."""
        # Ensure user owns chat
        await ChatService.get_chat(chat_id, user)

        query = {"chat_id": chat_id}
        if search:
            query["content"] = {"$regex": search, "$options": "i"}

        return await Message.find(query).sort("created_at").skip(skip).limit(limit).to_list()

    @staticmethod
    async def send_message(
        chat_id: str,
        user: User,
        data: SendMessageRequest,
    ) -> Message:
        """
        Non-streaming flow for sending a message.
        Saves user message, calls AI, saves AI message, returns AI message.
        """
        chat = await ChatService.get_chat(chat_id, user)
        identity = await Identity.find_one(Identity.slug == chat.identity_id)
        
        if not identity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Identity not found"
            )

        # 1. Compile System Prompt
        system_prompt = build_system_prompt(identity.model_dump())

        # 2. Get past messages for context
        past_msgs = await Message.find({"chat_id": chat_id}).sort("created_at").to_list()
        
        # 3. Save User Message
        user_msg = Message(
            chat_id=chat_id,
            user_id=str(user.id),
            identity_id=identity.slug,
            role="user",
            content=data.content,
            content_type=data.content_type,
            parent_message_id=data.parent_message_id,
            model_id="user",
            system_prompt_snapshot=system_prompt,
            attachments=data.attachments or []
        )
        await user_msg.insert()
        
        # Extract memories in background
        from services.memory_service import MemoryService
        import asyncio
        asyncio.create_task(MemoryService.extract_memories(user, chat_id, identity.slug, data.content))

        # Update chat timestamp
        chat.message_count += 2
        await chat.save()

        # 4. Format messages for AI
        ai_messages = [{"role": "system", "content": system_prompt}]
        for m in past_msgs:
            ai_messages.append({"role": m.role, "content": m.content})
        ai_messages.append({"role": "user", "content": data.content})

        # 5. Call AI Manager
        manager = get_model_manager()
        ai_response = await manager.generate(
            messages=ai_messages,
            **identity.model_config_override
        )

        # 6. Save AI Response
        ai_msg = Message(
            chat_id=chat_id,
            user_id=str(user.id),
            identity_id=identity.slug,
            role="assistant",
            content=ai_response["content"],
            content_type="text",
            parent_message_id=str(user_msg.id),
            model_id=ai_response.get("model", "unknown"),
            system_prompt_snapshot=system_prompt
        )
        await ai_msg.insert()

        return ai_msg

    @staticmethod
    async def add_feedback(
        chat_id: str,
        message_id: str,
        user: User,
        data: MessageFeedbackRequest,
    ) -> Message:
        """Add feedback to a message (rating, thumbs up/down, correction)."""
        # Verify access
        await ChatService.get_chat(chat_id, user)

        msg = await Message.get(message_id)
        if not msg or msg.chat_id != chat_id:
            raise HTTPException(status_code=404, detail="Message not found")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(msg, key, value)
        
        await msg.save()
        return msg
