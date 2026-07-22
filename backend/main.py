"""
SelfGPT — FastAPI Application Entry Point

Starts the API server with all routers, middleware, database connections,
and seed data initialization.
"""

import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.settings import get_settings
from database import init_mongodb, close_mongodb, init_redis, close_redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def seed_identities():
    """Load seed identities from JSON if they don't exist yet."""
    from models.identity import Identity

    existing = await Identity.find_one(Identity.slug == "marcus-aurelius")
    if existing:
        logger.info("Seed identities already exist — skipping")
        return

    seed_path = Path(__file__).parent / "seed" / "identities" / "seed_identities.json"
    if not seed_path.exists():
        logger.warning(f"Seed file not found: {seed_path}")
        return

    with open(seed_path, "r", encoding="utf-8") as f:
        identities_data = json.load(f)

    from ai.prompt_builder import build_system_prompt

    for data in identities_data:
        # Compile system prompt from profile for non-coming-soon identities
        if not data.get("is_coming_soon", False) and data.get("profile"):
            data["system_prompt_template"] = build_system_prompt(data)

        identity = Identity(**data)
        await identity.insert()
        logger.info(f"Seeded identity: {data['name']} ({data['slug']})")

    logger.info(f"Seeded {len(identities_data)} identities")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    settings = get_settings()

    # ── Startup ──
    logger.info(f"Starting {settings.app_name} in {settings.app_env} mode")

    # Initialize databases
    await init_mongodb()
    logger.info("MongoDB connected")

    try:
        await init_redis()
        logger.info("Redis connected")
    except Exception as e:
        logger.warning(f"Redis connection failed (non-fatal in dev): {e}")

    # Seed data
    await seed_identities()

    # Ensure upload directory exists
    Path(settings.storage_local_dir).mkdir(parents=True, exist_ok=True)

    logger.info(f"{settings.app_name} is ready on {settings.api_host}:{settings.api_port}")

    yield

    # ── Shutdown ──
    await close_mongodb()
    await close_redis()
    logger.info(f"{settings.app_name} shut down cleanly")


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="AI Identity Platform — Every conversation. A new perspective.",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # ── CORS ──
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Static files (uploads, avatars) ──
    data_dir = Path(settings.storage_local_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(data_dir)), name="static")

    # ── Routers ──
    from routers import (
        health,
        identities,
        auth,
        chats,
        messages,
        ws_messages,
        memory,
    )
    from routers.stubs import (
        rag_router,
        uploads_router,
        training_router,
        admin_router,
    )

    app.include_router(health.router)
    app.include_router(identities.router)
    app.include_router(auth.router)
    app.include_router(chats.router)
    app.include_router(messages.router)
    app.include_router(ws_messages.router)
    app.include_router(memory.router)
    
    app.include_router(rag_router)
    app.include_router(uploads_router)
    app.include_router(training_router)
    app.include_router(admin_router)

    @app.get("/")
    async def root():
        return {
            "name": settings.app_name,
            "tagline": "Every conversation. A new perspective.",
            "version": "0.1.0",
            "docs": "/docs" if settings.debug else None,
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
