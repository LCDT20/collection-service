"""Initial migration for collection items

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import UUID, JSON
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'collection_items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False, comment='Unique identifier for the collection item'),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False, comment='Owner of this collection item'),
        sa.Column('card_id', UUID(as_uuid=True), nullable=False, comment='Reference to the card'),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1', comment='Number of copies of this card'),
        sa.Column('condition', sa.String(length=10), nullable=False, comment='Condition of the card (e.g., \'M\', \'NM\', \'LP\', \'MP\', \'HP\')'),
        sa.Column('language', sa.String(length=5), nullable=False, comment='Language code (e.g., \'en\', \'it\', \'jp\')'),
        sa.Column('is_foil', sa.Boolean(), nullable=False, server_default='0', comment='Whether the card is foil'),
        sa.Column('is_signed', sa.Boolean(), nullable=False, server_default='0', comment='Whether the card is signed by artist or player'),
        sa.Column('is_altered', sa.Boolean(), nullable=False, server_default='0', comment='Whether the card has been altered'),
        sa.Column('notes', sa.Text(), nullable=True, comment='Additional notes about the card'),
        sa.Column('tags', JSON(), nullable=True, comment='Custom tags for categorization (stored as JSON array)'),
        sa.Column('source', sa.String(length=50), nullable=True, comment='Source of the item (e.g., \'cardtrader\', \'manual\')'),
        sa.Column('cardtrader_id', sa.BigInteger(), nullable=True, unique=True, comment='External ID from CardTrader platform'),
        sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=True, comment='Last synchronization timestamp with external source'),
        sa.Column('added_at', sa.DateTime(timezone=True), nullable=False, server_default=func.now(), comment='Creation timestamp'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=func.now(), comment='Last update timestamp'),
        sa.Index('idx_user_card', 'user_id', 'card_id'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('quantity > 0', name='check_positive_quantity')
    )
    
    # Create indexes
    op.create_index('ix_collection_items_user_id', 'collection_items', ['user_id'])
    op.create_index('ix_collection_items_card_id', 'collection_items', ['card_id'])
    op.create_index('ix_collection_items_condition', 'collection_items', ['condition'])
    op.create_index('ix_collection_items_language', 'collection_items', ['language'])
    op.create_index('ix_collection_items_source', 'collection_items', ['source'])
    op.create_index('ix_collection_items_cardtrader_id', 'collection_items', ['cardtrader_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_collection_items_cardtrader_id', table_name='collection_items')
    op.drop_index('ix_collection_items_source', table_name='collection_items')
    op.drop_index('ix_collection_items_language', table_name='collection_items')
    op.drop_index('ix_collection_items_condition', table_name='collection_items')
    op.drop_index('ix_collection_items_card_id', table_name='collection_items')
    op.drop_index('ix_collection_items_user_id', table_name='collection_items')
    
    op.drop_table('collection_items')

