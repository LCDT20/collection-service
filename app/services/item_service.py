from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy import select, func as sql_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.item import CollectionItem


class ItemService:
    """Service layer for CollectionItem operations."""
    
    @staticmethod
    async def create_item(
        db: AsyncSession,
        user_id: UUID,
        item_data: dict
    ) -> CollectionItem:
        """
        Create a new collection item.
        
        Args:
            db: Database session
            user_id: Owner's user ID
            item_data: Dictionary containing item fields
            
        Returns:
            Created CollectionItem
            
        Raises:
            HTTPException: If creation fails
        """
        try:
            item = CollectionItem(
                user_id=user_id,
                **item_data
            )
            db.add(item)
            await db.commit()
            await db.refresh(item)
            return item
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create item: {str(e)}"
            )
    
    @staticmethod
    async def get_item_by_id(
        db: AsyncSession,
        item_id: UUID,
        user_id: UUID
    ) -> Optional[CollectionItem]:
        """
        Get a specific item by ID, verifying ownership.
        
        Args:
            db: Database session
            item_id: Item ID
            user_id: Owner's user ID for ownership verification
            
        Returns:
            CollectionItem or None
            
        Raises:
            HTTPException: If item not found or access denied
        """
        result = await db.execute(
            select(CollectionItem)
            .where(CollectionItem.id == item_id)
            .where(CollectionItem.user_id == user_id)
        )
        item = result.scalar_one_or_none()
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found or access denied"
            )
        
        return item
    
    @staticmethod
    async def list_items(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 100,
        offset: int = 0,
        language: Optional[str] = None,
        is_foil: Optional[bool] = None,
        source: Optional[str] = None
    ) -> Tuple[List[CollectionItem], int]:
        """
        List items for a user with optional filtering and pagination.
        
        Args:
            db: Database session
            user_id: Owner's user ID
            limit: Maximum number of items to return
            offset: Number of items to skip
            language: Optional language filter
            is_foil: Optional foil filter
            source: Optional source filter
            
        Returns:
            Tuple of (items list, total count)
        """
        # Build base query
        query = select(CollectionItem).where(CollectionItem.user_id == user_id)
        
        # Apply filters
        if language is not None:
            query = query.where(CollectionItem.language == language)
        
        if is_foil is not None:
            query = query.where(CollectionItem.is_foil == is_foil)
        
        if source is not None:
            query = query.where(CollectionItem.source == source)
        
        # Get total count
        count_query = select(sql_func.count()).select_from(
            query.subquery()
        )
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()
        
        # Apply pagination and ordering
        query = query.order_by(CollectionItem.added_at.desc())
        query = query.limit(limit).offset(offset)
        
        # Execute query
        result = await db.execute(query)
        items = result.scalars().all()
        
        return list(items), total
    
    @staticmethod
    async def update_item(
        db: AsyncSession,
        item_id: UUID,
        user_id: UUID,
        item_data: dict
    ) -> CollectionItem:
        """
        Update an existing item, verifying ownership.
        
        Args:
            db: Database session
            item_id: Item ID
            user_id: Owner's user ID for ownership verification
            item_data: Dictionary containing fields to update
            
        Returns:
            Updated CollectionItem
            
        Raises:
            HTTPException: If item not found, access denied, or update fails
        """
        # Get item first to verify ownership
        item = await ItemService.get_item_by_id(db, item_id, user_id)
        
        # Update fields
        for key, value in item_data.items():
            if value is not None:
                setattr(item, key, value)
        
        try:
            await db.commit()
            await db.refresh(item)
            return item
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update item: {str(e)}"
            )
    
    @staticmethod
    async def delete_item(
        db: AsyncSession,
        item_id: UUID,
        user_id: UUID
    ) -> bool:
        """
        Delete an item, verifying ownership.
        
        Args:
            db: Database session
            item_id: Item ID
            user_id: Owner's user ID for ownership verification
            
        Returns:
            True if deleted successfully
            
        Raises:
            HTTPException: If item not found, access denied, or deletion fails
        """
        # Get item first to verify ownership
        item = await ItemService.get_item_by_id(db, item_id, user_id)
        
        try:
            await db.delete(item)
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete item: {str(e)}"
            )

