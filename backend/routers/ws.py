"""
SelfGPT — Router: WebSocket

Real-time streaming chat via WebSocket connections.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/chat/{chat_id}")
async def chat_websocket(
    websocket: WebSocket,
    chat_id: str,
    token: str = Query(...),
):
    """
    WebSocket endpoint for streaming chat.

    Client sends: {"content": "...", "content_type": "text"}
    Server streams: {"type": "token", "content": "..."} per token
    Server final:   {"type": "done", "message": {...full message...}}
    """
    await websocket.accept()
    logger.info(f"WebSocket connected: chat_id={chat_id}")

    try:
        while True:
            data = await websocket.receive_json()
            # Phase 4 — streaming implementation
            await websocket.send_json({
                "type": "error",
                "content": "Streaming not yet implemented. Coming in Phase 4.",
            })
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: chat_id={chat_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011)
