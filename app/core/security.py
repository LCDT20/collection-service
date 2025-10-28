from typing import Optional
from fastapi import HTTPException, status
from jose import jwt, JWTError
from cachetools import TTLCache
import httpx


# Cache for JWKS (24 hour TTL)
_jwks_cache = TTLCache(maxsize=1, ttl=86400)
_jwks_client = None


async def get_jwks(jwks_url: str) -> dict:
    """
    Fetch JWKS (JSON Web Key Set) with caching.
    
    Args:
        jwks_url: URL to fetch JWKS from
        
    Returns:
        Dict containing the JWKS
    """
    global _jwks_cache, _jwks_client
    
    if jwks_url in _jwks_cache:
        return _jwks_cache[jwks_url]
    
    if _jwks_client is None:
        _jwks_client = httpx.AsyncClient(timeout=10.0)
    
    try:
        response = await _jwks_client.get(jwks_url)
        response.raise_for_status()
        jwks = response.json()
        _jwks_cache[jwks_url] = jwks
        return jwks
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch JWKS: {str(e)}"
        )


def get_signing_key(token: str, jwks: dict) -> Optional[dict]:
    """
    Find the signing key from JWKS based on token's 'kid'.
    
    Args:
        token: JWT token string
        jwks: JWKS dict
        
    Returns:
        Public key dict or None
    """
    try:
        # Decode unverified header to get 'kid'
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        
        if not kid:
            return None
        
        # Find matching key in JWKS
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return key
        
        return None
    except JWTError:
        return None


async def verify_token(
    token: str,
    jwks_url: str,
    audience: str,
    issuer: str
) -> dict:
    """
    Verify JWT token using JWKS and extract payload.
    
    Args:
        token: JWT token string (without 'Bearer ' prefix)
        jwks_url: URL to fetch JWKS from
        audience: Expected audience value
        issuer: Expected issuer value
        
    Returns:
        Decoded JWT payload (dict)
        
    Raises:
        HTTPException: If token is invalid
    """
    from app.core.config import settings
    
    # Fetch JWKS
    jwks = await get_jwks(jwks_url)
    
    # Get signing key
    key = get_signing_key(token, jwks)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: could not find signing key"
        )
    
    try:
        # Verify and decode token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=audience,
            issuer=issuer
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

