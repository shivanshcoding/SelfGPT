"""
SelfGPT — Service: Identity

Handles listing and managing AI identities (including custom ones).
"""

from typing import List, Optional
from fastapi import HTTPException, status
from models.identity import Identity
from models.user import User
from schemas.identity import CreateCustomIdentityRequest, UpdateCustomIdentityRequest
from ai.prompt_builder import build_system_prompt

class IdentityService:
    @staticmethod
    async def list_identities(
        category: Optional[str] = None,
        search: Optional[str] = None,
        include_coming_soon: bool = True,
        user_id: Optional[str] = None,
    ) -> List[Identity]:
        """List published identities. Custom ones are isolated to the user."""
        query = {}
        
        # Hide coming soon if requested
        if not include_coming_soon:
            query["is_coming_soon"] = False

        # Apply category filter
        if category:
            query["category"] = category

        # Apply search filter
        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        # Combine logic for public vs private
        if user_id:
            # Show public ones + this user's custom one
            query["$or"] = [
                {"is_public": True},
                {"creator_id": user_id}
            ]
        else:
            # Show only public ones
            query["is_public"] = True

        identities = await Identity.find(query).to_list()
        return identities

    @staticmethod
    async def get_identity(slug: str, user_id: Optional[str] = None) -> Identity:
        """Get an identity by slug."""
        identity = await Identity.find_one(Identity.slug == slug)
        if not identity:
            raise HTTPException(status_code=404, detail="Identity not found")
            
        if not identity.is_public and identity.creator_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to view this identity")
            
        return identity

    @staticmethod
    async def create_custom_identity(user: User, data: CreateCustomIdentityRequest) -> Identity:
        """Create a custom identity for a user."""
        slug = f"custom-{user.id}"
        
        existing = await Identity.find_one(Identity.slug == slug)
        if existing:
            raise HTTPException(status_code=400, detail="User already has a custom identity. Update it instead.")

        identity_data = data.model_dump()
        identity_data["name"] = identity_data.get("name") or f"{user.username}'s AI"
        
        identity = Identity(
            slug=slug,
            name=identity_data["name"],
            tagline="Custom AI Identity",
            category="Custom",
            description="Your personal custom AI.",
            is_public=False,
            creator_id=str(user.id),
            profile=identity_data.get("profile", {})
        )
        
        # Compile system prompt
        identity.system_prompt_template = build_system_prompt(identity.model_dump())
        
        await identity.insert()
        return identity

    @staticmethod
    async def update_custom_identity(user: User, data: UpdateCustomIdentityRequest) -> Identity:
        """Update user's custom identity."""
        slug = f"custom-{user.id}"
        identity = await Identity.find_one(Identity.slug == slug)
        
        if not identity:
            raise HTTPException(status_code=404, detail="Custom identity not found")
            
        update_data = data.model_dump(exclude_unset=True)
        
        if "name" in update_data:
            identity.name = update_data["name"]
            
        if "profile" in update_data:
            # Merge profile data
            identity.profile = {**identity.profile, **update_data["profile"]}
            # Recompile prompt
            identity.system_prompt_template = build_system_prompt(identity.model_dump())
            
        await identity.save()
        return identity

    @staticmethod
    async def get_my_custom_identity(user: User) -> Identity:
        """Get the current user's custom identity."""
        slug = f"custom-{user.id}"
        identity = await Identity.find_one(Identity.slug == slug)
        if not identity:
            raise HTTPException(status_code=404, detail="No custom identity found")
        return identity
