from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, BigInteger, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.sql import func
from uuid import uuid4
import uuid

from app.models.database import Base


class CollectionItem(Base):
    """
    Model representing a card in a user's collection.
    
    Maps to the 'collection_items' table in MySQL database.
    """
    
    __tablename__ = "collection_items"
    
    # Primary Key
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
        nullable=False,
        comment="Unique identifier for the collection item"
    )
    
    # Foreign Keys & Relationships
    user_id = Column(
        String(36),
        nullable=False,
        index=True,
        comment="Owner of this collection item"
    )
    
    card_id = Column(
        String(36),
        nullable=False,
        index=True,
        comment="Reference to the card"
    )
    
    # Core Fields
    quantity = Column(
        Integer,
        nullable=False,
        default=1,
        comment="Number of copies of this card"
    )
    
    condition = Column(
        String(10),
        nullable=False,
        index=True,
        comment="Condition of the card (e.g., 'M', 'NM', 'LP', 'MP', 'HP')"
    )
    
    language = Column(
        String(5),
        nullable=False,
        index=True,
        comment="Language code (e.g., 'en', 'it', 'jp')"
    )
    
    is_foil = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether the card is foil"
    )
    
    # Optional Fields
    is_signed = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether the card is signed by artist or player"
    )
    
    is_altered = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether the card has been altered"
    )
    
    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes about the card"
    )
    
    tags = Column(
        JSON,
        nullable=True,
        comment="Custom tags for categorization (stored as JSON array)"
    )
    
    # CardTrader Integration Fields
    source = Column(
        String(50),
        nullable=True,
        index=True,
        comment="Source of the item (e.g., 'cardtrader', 'manual')"
    )
    
    cardtrader_id = Column(
        BigInteger,
        nullable=True,
        unique=True,
        index=True,
        comment="External ID from CardTrader platform"
    )
    
    last_synced_at = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Last synchronization timestamp with external source"
    )
    
    # Timestamps
    added_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="Creation timestamp"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Last update timestamp"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
        Index('idx_user_card', 'user_id', 'card_id'),
    )
    
    def __repr__(self):
        return (
            f"<CollectionItem(id={self.id}, user_id={self.user_id}, "
            f"card_id={self.card_id}, quantity={self.quantity})>"
        )

