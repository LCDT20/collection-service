from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class ItemBase(BaseModel):
    """Base schema with common fields for CollectionItem."""
    
    card_id: UUID = Field(..., description="Reference to the card")
    quantity: int = Field(default=1, ge=1, description="Number of copies")
    condition: str = Field(..., max_length=10, description="Card condition")
    language: str = Field(..., max_length=5, description="Language code")
    is_foil: bool = Field(default=False, description="Is foil")
    is_signed: Optional[bool] = Field(default=False, description="Is signed")
    is_altered: Optional[bool] = Field(default=False, description="Is altered")
    notes: Optional[str] = Field(default=None, description="Additional notes")
    tags: Optional[List[str]] = Field(default=None, description="Custom tags")
    source: Optional[str] = Field(default=None, max_length=50, description="Item source")
    cardtrader_id: Optional[int] = Field(default=None, description="CardTrader ID")
    
    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v):
        """Ensure tags is a list if provided."""
        if v is None:
            return None
        if isinstance(v, str):
            # If passed as JSON string, parse it
            import json
            return json.loads(v)
        return v


class ItemCreate(ItemBase):
    """Schema for creating a new CollectionItem."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating a CollectionItem (all fields optional)."""
    
    card_id: Optional[UUID] = None
    quantity: Optional[int] = Field(None, ge=1)
    condition: Optional[str] = Field(None, max_length=10)
    language: Optional[str] = Field(None, max_length=5)
    is_foil: Optional[bool] = None
    is_signed: Optional[bool] = None
    is_altered: Optional[bool] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = Field(None, max_length=50)
    cardtrader_id: Optional[int] = None
    last_synced_at: Optional[datetime] = None


class ItemResponse(ItemBase):
    """Schema for CollectionItem response."""
    
    id: UUID = Field(..., description="Item unique identifier")
    user_id: UUID = Field(..., description="Owner user ID")
    added_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = {"from_attributes": True}


class ItemListResponse(BaseModel):
    """Schema for paginated list of CollectionItems."""
    
    items: List[ItemResponse]
    total: int = Field(..., description="Total number of items")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Current offset")

