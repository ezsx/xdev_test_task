from contextlib import asynccontextmanager

import uvicorn
from api.routers import main_router
from core.config import settings
from core.logger import LOGGING
from db import redis_service_instance
from db.postgres import engine
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous lifespan manager for FastAPI app.

    Initializes Redis and PostgreSQL connections on startup
    and closes them on shutdown.
    """
    await redis_service_instance.init()
    yield

    await redis_service_instance.close()
    await engine.dispose()


app = FastAPI(
    description="Mush service for managing mush and basckets.",
    version="1.0.0",
    title=settings.project_name,
    docs_url="/store/api/openapi",
    openapi_url="/store/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.get("/health", include_in_schema=False)
def health():
    """
    Health check endpoint.

    Returns a simple status message indicating that the service is running.

    Returns:
        dict: A dictionary containing a status key with value 'ok'.
    """
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global unexpected error handler.
    """
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred. Please try again later."},
    )


app.include_router(main_router)


if __name__ == "__main__":
    """
    Entry point for running the FastAPI application with Uvicorn.

    The application listens on all available IPs on port 8000 and uses a
    custom logging configuration. The `reload` option is enabled for development.
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level="debug",
        reload=True,
    )
