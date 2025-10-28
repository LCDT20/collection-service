from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_token_dependency
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse
from app.services.item_service import ItemService

router = APIRouter(
    prefix="/api/v1/collections/items",
    tags=["Collection Items"]
)


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new collection item"
)
async def create_item(
    item: ItemCreate,
    current_user: dict = Depends(verify_token_dependency),
    db: AsyncSession = Depends(get_db_session)
) -> ItemResponse:
    """
    Create a new item in the user's collection.
    
    **Authentication Required**
    
    - **card_id**: Reference to the card (UUID)
    - **quantity**: Number of copies (minimum 1)
    - **condition**: Card condition (e.g., 'M', 'NM', 'LP')
    - **language**: Language code (e.g., 'en', 'it')
    - **is_foil**: Whether the card is foil
    """
    user_id = current_user["user_id"]
    
    # Create item
    created_item = await ItemService.create_item(
        db=db,
        user_id=user_id,
        item_data=item.model_dump(exclude_none=True)
    )
    
    return ItemResponse.model_validate(created_item)


@router.get(
    "/",
    response_model=ItemListResponse,
    summary="List collection items"
)
async def list_items(
    limit: int = Query(default=100, ge=1, le=500, description="Maximum items to return"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
    language: Optional[str] = Query(default=None, description="Filter by language"),
    is_foil: Optional[bool] = Query(default=None, description="Filter by foil status"),
    source: Optional[str] = Query(default=None, description="Filter by source"),
    current_user: dict = Depends(verify_token_dependency),
    db: AsyncSession = Depends(get_db_session)
) -> ItemListResponse:
    """
    List items in the user's collection with optional filtering and pagination.
    
    **Authentication Required**
    
    - Returns paginated list of items
    - Supports filtering by language, foil status, and source
    - Results ordered by creation date (newest first)
    """
    user_id = current_user["user_id"]
    
    items, total = await ItemService.list_items(
        db=db,
        user_id=user_id,
        limit=limit,
        offset=offset,
        language=language,
        is_foil=is_foil,
        source=source
    )
    
    return ItemListResponse(
        items=[ItemResponse.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset
    )


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get a specific collection item"
)
async def get_item(
    item_id: UUID,
    current_user: dict = Depends(verify_token_dependency),
    db: AsyncSession = Depends(get_db_session)
) -> ItemResponse:
    """
    Get details of a specific collection item.
    
    **Authentication Required**
    
    - Returns 404 if item not found or access denied
    - Only returns items owned by the authenticated user
    """
    user_id = current_user["user_id"]
    
    item = await ItemService.get_item_by_id(
        db=db,
        item_id=item_id,
        user_id=user_id
    )
    
    return ItemResponse.model_validate(item)


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update a collection item"
)
async def update_item(
    item_id: UUID,
    item_update: ItemUpdate,
    current_user: dict = Depends(verify_token_dependency),
    db: AsyncSession = Depends(get_db_session)
) -> ItemResponse:
    """
    Update an existing collection item.
    
    **Authentication Required**
    
    - Only updates fields provided in the request
    - Returns 404 if item not found or access denied
    - Only allows updates to items owned by the authenticated user
    """
    user_id = current_user["user_id"]
    
    # Update item
    updated_item = await ItemService.update_item(
        db=db,
        item_id=item_id,
        user_id=user_id,
        item_data=item_update.model_dump(exclude_none=True)
    )
    
    return ItemResponse.model_validate(updated_item)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a collection item"
)
async def delete_item(
    item_id: UUID,
    current_user: dict = Depends(verify_token_dependency),
    db: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Delete a collection item.
    
    **Authentication Required**
    
    - Returns 404 if item not found or access denied
    - Only allows deletion of items owned by the authenticated user
    - Returns 204 No Content on success
    """
    user_id = current_user["user_id"]
    
    await ItemService.delete_item(
        db=db,
        item_id=item_id,
        user_id=user_id
    )

