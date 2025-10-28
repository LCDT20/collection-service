from typing import AsyncGenerator, Annotated
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.config import settings
from app.core.security import verify_token


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    
    Uses the session maker from app.models.database
    
    Yields:
        AsyncSession: Database session
    """
    from app.models.database import async_session_maker
    
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def verify_token_dependency(
    authorization: Annotated[str, Header(description="Bearer token")]
) -> dict:
    """
    FastAPI dependency to verify JWT token from Authorization header.
    
    Args:
        authorization: Authorization header value
        
    Returns:
        Decoded JWT payload containing user_id
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected: Bearer <token>"
        )
    
    token = parts[1]
    
    # Verify token
    payload = await verify_token(
        token=token,
        jwks_url=settings.AUTH_JWKS_URL,
        audience=settings.JWT_AUDIENCE,
        issuer=settings.JWT_ISSUER
    )
    
    # Extract user_id from 'sub' claim
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing 'sub' claim"
        )
    
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid 'sub' claim format (must be UUID)"
        )
    
    return {
        "user_id": user_id,
        "payload": payload
    }

