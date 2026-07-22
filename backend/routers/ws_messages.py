"""
SelfGPT — Router: WebSocket Messages

Streaming endpoints for chat generation.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Optional
import json

from core.dependencies import get_current_user_ws
from models.user import User
from models.chat import Chat
from models.message import Message
from models.identity import Identity
from ai.model_manager import get_model_manager
from ai.prompt_builder import build_system_prompt

router = APIRouter(prefix="/api/ws", tags=["WebSockets"])


@router.websocket("/chat/{chat_id}/stream")
async def chat_stream(websocket: WebSocket, chat_id: str, token: str):
    """
    WebSocket endpoint for real-time text streaming.
    Client sends a JSON with {"content": "Hello"}.
    Server streams back text tokens.
    """
    user = await get_current_user_ws(token)
    if not user:
        await websocket.close(code=1008, reason="Unauthorized")
        return

    await websocket.accept()

    try:
        # Load chat & identity
        chat = await Chat.get(chat_id)
        if not chat or chat.user_id != str(user.id):
            await websocket.close(code=4004, reason="Chat not found")
            return

        identity = await Identity.find_one(Identity.slug == chat.identity_id)
        if not identity:
            await websocket.close(code=4004, reason="Identity not found")
            return

        # Receive user message
        data = await websocket.receive_text()
        msg_data = json.loads(data)
        user_text = msg_data.get("content", "").strip()

        if not user_text:
            await websocket.close(code=4000, reason="Empty message")
            return

        # Compile System Prompt
        system_prompt = build_system_prompt(identity.model_dump())

        # Save User Message
        user_msg = Message(
            chat_id=chat_id,
            user_id=str(user.id),
            identity_id=identity.slug,
            role="user",
            content=user_text,
            model_id="user",
            system_prompt_snapshot=system_prompt
        )
        await user_msg.insert()

        # Update chat counts
        chat.message_count += 2
        await chat.save()

        # Build context history
        past_msgs = await Message.find({"chat_id": chat_id}).sort("created_at").to_list()
        ai_messages = [{"role": "system", "content": system_prompt}]
        for m in past_msgs:
            ai_messages.append({"role": m.role, "content": m.content})

        # Start streaming
        manager = get_model_manager()
        full_response = ""
        
        async for chunk in manager.stream(messages=ai_messages, **identity.model_config_override):
            full_response += chunk
            # Send chunk to client
            await websocket.send_json({
                "type": "token",
                "content": chunk
            })

        # Save AI Message
        ai_msg = Message(
            chat_id=chat_id,
            user_id=str(user.id),
            identity_id=identity.slug,
            role="assistant",
            content=full_response,
            parent_message_id=str(user_msg.id),
            model_id=identity.model_config_override.get("model", manager.default_model),
            system_prompt_snapshot=system_prompt
        )
        await ai_msg.insert()

        # Notify done
        await websocket.send_json({
            "type": "done",
            "message_id": str(ai_msg.id)
        })

        await websocket.close()

    except WebSocketDisconnect:
        # Client disconnected early, that's fine
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "content": str(e)
        })
        await websocket.close(code=1011)
