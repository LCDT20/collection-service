-- ============================================================
-- CREATE TABLE: collection_items
-- ============================================================
-- Description: Card collection items for users
-- Database: MySQL 8.0+
-- Generated from: app/models/item.py (CollectionItem model)
-- ============================================================

CREATE TABLE IF NOT EXISTS `collection_items` (
    -- Primary Key
    `id` CHAR(36) NOT NULL COMMENT 'Unique identifier for the collection item',
    
    -- Foreign Keys & Relationships
    `user_id` CHAR(36) NOT NULL COMMENT 'Owner of this collection item',
    `card_id` CHAR(36) NOT NULL COMMENT 'Reference to the card',
    
    -- Core Fields
    `quantity` INT NOT NULL DEFAULT 1 COMMENT 'Number of copies of this card',
    `condition` VARCHAR(10) NOT NULL COMMENT 'Condition of the card (e.g., ''M'', ''NM'', ''LP'', ''MP'', ''HP'')',
    `language` VARCHAR(5) NOT NULL COMMENT 'Language code (e.g., ''en'', ''it'', ''jp'')',
    `is_foil` BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Whether the card is foil',
    
    -- Optional Fields
    `is_signed` BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Whether the card is signed by artist or player',
    `is_altered` BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Whether the card has been altered',
    `notes` TEXT NULL COMMENT 'Additional notes about the card',
    `tags` JSON NULL COMMENT 'Custom tags for categorization (stored as JSON array)',
    
    -- CardTrader Integration Fields
    `source` VARCHAR(50) NULL COMMENT 'Source of the item (e.g., ''cardtrader'', ''manual'')',
    `cardtrader_id` BIGINT NULL COMMENT 'External ID from CardTrader platform',
    `last_synced_at` DATETIME NULL COMMENT 'Last synchronization timestamp with external source',
    
    -- Timestamps
    `added_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation timestamp',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update timestamp',
    
    -- Constraints
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_cardtrader_id` (`cardtrader_id`),
    CHECK (`quantity` > 0),
    
    -- Indexes
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_card_id` (`card_id`),
    INDEX `idx_condition` (`condition`),
    INDEX `idx_language` (`language`),
    INDEX `idx_source` (`source`),
    INDEX `idx_user_card` (`user_id`, `card_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Card collection items for users';

