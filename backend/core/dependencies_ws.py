from core.security import decode_token
from models.user import User
from typing import Optional

async def get_current_user_ws(token: str) -> Optional[User]:
    """Dependency for authenticating WebSocket connections via query param."""
    if not token:
        return None
        
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        return None
        
    user_id = payload.get("sub")
    if not user_id:
        return None
        
    user = await User.get(user_id)
    return user
