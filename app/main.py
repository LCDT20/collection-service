from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from app.core.config import settings
from app.routers import items
from app.models import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.
    """
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    yield
    
    # Shutdown
    await database.engine.dispose()
    print(f"Shutting down {settings.APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Collection Service for TakeYourTrade platform",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/test/database", tags=["Test"])
async def test_database():
    """Test database connection."""
    try:
        from sqlalchemy import text
        async with database.async_session_maker() as session:
            result = await session.execute(text("SELECT VERSION() as version"))
            version = result.fetchone()[0]
            
            return {
                "status": "success",
                "database": "connected",
                "mysql_version": version,
                "message": "Database connection successful"
            }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e),
            "message": "Database connection failed"
        }


@app.get("/test/config", tags=["Test"])
async def test_config():
    """Test configuration and environment variables."""
    return {
        "status": "success",
        "config": {
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
            "debug": settings.DEBUG,
            "has_database_url": bool(settings.DATABASE_URL),
            "auth_jwks_url": settings.AUTH_JWKS_URL,
            "jwt_audience": settings.JWT_AUDIENCE,
            "jwt_issuer": settings.JWT_ISSUER,
            "cors_origins": settings.CORS_ORIGINS
        }
    }


@app.get("/test/full", tags=["Test"])
async def test_full_system():
    """Full system test including database and configuration."""
    results = {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": str(datetime.now()),
        "tests": {}
    }
    
    # Test Database
    try:
        from sqlalchemy import text
        async with database.async_session_maker() as session:
            result = await session.execute(text("SELECT VERSION() as version, DATABASE() as db"))
            row = result.fetchone()
            results["tests"]["database"] = {
                "status": "success",
                "mysql_version": row[0],
                "current_database": row[1]
            }
    except Exception as e:
        results["tests"]["database"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test Configuration
    try:
        results["tests"]["configuration"] = {
            "status": "success",
            "has_database_url": bool(settings.DATABASE_URL),
            "cors_configured": len(settings.CORS_ORIGINS) > 0,
            "jwt_configured": bool(settings.AUTH_JWKS_URL)
        }
    except Exception as e:
        results["tests"]["configuration"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Overall status
    all_passed = all(
        test["status"] == "success" 
        for test in results["tests"].values()
    )
    
    results["overall_status"] = "healthy" if all_passed else "degraded"
    
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

