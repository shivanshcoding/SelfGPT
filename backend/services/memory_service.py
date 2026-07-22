"""
SelfGPT — Service: Memory

Handles extracting, storing, and retrieving memories.
"""

from typing import List, Optional
from models.memory import Memory
from models.user import User
from ai.model_manager import get_model_manager
import json

class MemoryService:
    @staticmethod
    async def extract_memories(user: User, chat_id: str, identity_id: str, user_message: str):
        """
        Background task to evaluate if a user message contains facts worth remembering.
        """
        # Call a lightweight LLM to decide if there is a fact to remember
        manager = get_model_manager()
        
        prompt = f"""
You are an AI assistant's background memory extractor.
Analyze the user's message. If they state a clear, long-term fact about themselves, their preferences, or their background, extract it.
Output valid JSON only.

User message: "{user_message}"

Format:
{{
  "has_memory": true/false,
  "memories": [
    {{"content": "User lives in New York", "type": "user_fact"}}
  ]
}}
"""
        try:
            res = await manager.generate(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            
            # Very basic JSON parsing from raw output (assuming well-behaved LLM)
            raw = res["content"]
            # Strip markdown code blocks if any
            if raw.startswith("```json"):
                raw = raw[7:-3]
            elif raw.startswith("```"):
                raw = raw[3:-3]
                
            data = json.loads(raw.strip())
            
            if data.get("has_memory") and data.get("memories"):
                for m in data["memories"]:
                    mem = Memory(
                        user_id=str(user.id),
                        identity_id=identity_id,
                        chat_id=chat_id,
                        content=m["content"],
                        memory_type=m.get("type", "user_fact")
                    )
                    await mem.insert()
                    
        except Exception as e:
            # Memory extraction failure should not crash the app
            print(f"Memory extraction failed: {e}")

    @staticmethod
    async def get_memories(user: User, identity_id: Optional[str] = None) -> List[Memory]:
        """Get all memories for a user, optionally filtered by identity."""
        query = {"user_id": str(user.id), "is_active": True}
        if identity_id:
            # Get global memories (None) + identity specific memories
            query["$or"] = [
                {"identity_id": None},
                {"identity_id": identity_id}
            ]
            
        return await Memory.find(query).sort("-created_at").to_list()

    @staticmethod
    async def delete_memory(memory_id: str, user: User) -> bool:
        """Soft delete a memory."""
        mem = await Memory.get(memory_id)
        if mem and mem.user_id == str(user.id):
            mem.is_active = False
            await mem.save()
            return True
        return False
