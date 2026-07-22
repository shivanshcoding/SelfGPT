"""
SelfGPT — Router: Memory, RAG, Uploads, Training, Admin

Stub routers defining API contracts — implemented in later phases.
"""

from fastapi import APIRouter, Depends, status
from core.dependencies import get_current_user, get_current_admin
from models.user import User

# ── Memory Router ───────────────────────────────────────────────────────
memory_router = APIRouter(prefix="/api/memories", tags=["Memory"])


@memory_router.get("/")
async def list_memories(user: User = Depends(get_current_user)):
    """List all active memories for the current user."""
    pass


@memory_router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def forget_memory(memory_id: str, user: User = Depends(get_current_user)):
    """Hard-delete a memory — truly forgotten."""
    pass


@memory_router.patch("/{memory_id}")
async def update_memory(memory_id: str, user: User = Depends(get_current_user)):
    """Edit a memory's value."""
    pass


# ── RAG / Documents Router ─────────────────────────────────────────────
rag_router = APIRouter(prefix="/api/identities/{identity_id}/documents", tags=["RAG"])


@rag_router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_document(identity_id: str, user: User = Depends(get_current_user)):
    """Upload a document to an identity's knowledge base."""
    pass


@rag_router.get("/")
async def list_documents(identity_id: str, user: User = Depends(get_current_user)):
    """List documents in an identity's knowledge base."""
    pass


@rag_router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    identity_id: str, document_id: str, user: User = Depends(get_current_user)
):
    """Delete a document and its embeddings."""
    pass


# ── Uploads Router ──────────────────────────────────────────────────────
uploads_router = APIRouter(prefix="/api/uploads", tags=["Uploads"])


@uploads_router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_file(user: User = Depends(get_current_user)):
    """Upload a file attachment for chat messages."""
    pass


# ── Training Router ─────────────────────────────────────────────────────
training_router = APIRouter(prefix="/api/training", tags=["Training"])


@training_router.get("/export")
async def export_training_data(user: User = Depends(get_current_admin)):
    """Export training data as ChatML JSONL."""
    pass


@training_router.get("/stats")
async def training_stats(user: User = Depends(get_current_admin)):
    """Get training data statistics."""
    pass


# ── Admin Router ────────────────────────────────────────────────────────
admin_router = APIRouter(prefix="/api/admin", tags=["Admin"])


@admin_router.get("/users")
async def list_users(user: User = Depends(get_current_admin)):
    """List all users (admin only)."""
    pass


@admin_router.get("/analytics")
async def get_analytics(user: User = Depends(get_current_admin)):
    """Get platform usage analytics."""
    pass


@admin_router.get("/health")
async def health_check():
    """Health check endpoint — no auth required."""
    from ai.model_manager import get_model_manager
    manager = get_model_manager()
    llm_healthy = await manager.health_check()
    return {
        "status": "healthy",
        "llm_provider": "connected" if llm_healthy else "disconnected",
    }
