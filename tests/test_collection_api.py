import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from uuid import uuid4, UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import event
from sqlalchemy.pool import StaticPool
import json

from app.main import app
from app.models.database import Base, async_session_maker
from app.models.item import CollectionItem


# Test database URL (use in-memory SQLite for testing, then switch to MySQL for production)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Create test engine
@pytest.fixture(scope="function")
async def test_db_session():
    """Create a test database session."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
        await session.close()
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def client(test_db_session):
    """Create a test client with database override."""
    app.dependency_overrides.clear()
    
    async def get_test_db():
        yield test_db_session
    
    app.dependency_overrides[async_session_maker] = get_test_db
    
    # Mock authentication
    fake_user_id = uuid4()
    
    async def mock_verify_token():
        return {"user_id": fake_user_id, "payload": {"sub": str(fake_user_id)}}
    
    from app.dependencies import verify_token_dependency
    app.dependency_overrides[verify_token_dependency] = mock_verify_token
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    """Test creating a new collection item."""
    item_data = {
        "card_id": str(uuid4()),
        "quantity": 2,
        "condition": "NM",
        "language": "en",
        "is_foil": False,
        "notes": "Test card"
    }
    
    response = await client.post("/api/v1/collections/items/", json=item_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["quantity"] == 2
    assert data["condition"] == "NM"
    assert data["language"] == "en"
    assert data["is_foil"] is False
    assert data["notes"] == "Test card"
    assert "id" in data
    assert "user_id" in data
    assert "added_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_item_validation_error(client: AsyncClient):
    """Test validation error when creating item with invalid data."""
    # Missing required fields
    response = await client.post("/api/v1/collections/items/", json={})
    assert response.status_code == 422
    
    # Invalid quantity
    item_data = {
        "card_id": str(uuid4()),
        "quantity": 0,  # Must be >= 1
        "condition": "NM",
        "language": "en"
    }
    response = await client.post("/api/v1/collections/items/", json=item_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_items_empty(client: AsyncClient):
    """Test listing items when collection is empty."""
    response = await client.get("/api/v1/collections/items/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["limit"] == 100
    assert data["offset"] == 0


@pytest.mark.asyncio
async def test_list_items_with_filtering(client: AsyncClient, test_db_session: AsyncSession):
    """Test listing items with filtering."""
    # Create test items
    user_id = uuid4()
    card_id_1 = uuid4()
    card_id_2 = uuid4()
    
    items = [
        CollectionItem(
            id=uuid4(),
            user_id=user_id,
            card_id=card_id_1,
            quantity=1,
            condition="NM",
            language="en",
            is_foil=False,
            source="cardtrader"
        ),
        CollectionItem(
            id=uuid4(),
            user_id=user_id,
            card_id=card_id_2,
            quantity=2,
            condition="LP",
            language="it",
            is_foil=True,
            source="manual"
        )
    ]
    
    for item in items:
        test_db_session.add(item)
    await test_db_session.commit()
    
    # List all items
    response = await client.get("/api/v1/collections/items/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    
    # Filter by foil status
    response = await client.get("/api/v1/collections/items/?is_foil=true")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["is_foil"] is True
    
    # Filter by language
    response = await client.get("/api/v1/collections/items/?language=en")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["language"] == "en"


@pytest.mark.asyncio
async def test_get_item_success(client: AsyncClient, test_db_session: AsyncSession):
    """Test getting a specific item."""
    item = CollectionItem(
        id=uuid4(),
        user_id=uuid4(),
        card_id=uuid4(),
        quantity=1,
        condition="NM",
        language="en",
        is_foil=False
    )
    test_db_session.add(item)
    await test_db_session.commit()
    
    response = await client.get(f"/api/v1/collections/items/{item.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == str(item.id)
    assert data["condition"] == "NM"


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient):
    """Test getting a non-existent item."""
    fake_id = str(uuid4())
    response = await client.get(f"/api/v1/collections/items/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_item_success(client: AsyncClient, test_db_session: AsyncSession):
    """Test updating an item."""
    item = CollectionItem(
        id=uuid4(),
        user_id=uuid4(),
        card_id=uuid4(),
        quantity=1,
        condition="NM",
        language="en",
        is_foil=False
    )
    test_db_session.add(item)
    await test_db_session.commit()
    
    update_data = {
        "quantity": 3,
        "condition": "LP"
    }
    
    response = await client.patch(f"/api/v1/collections/items/{item.id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["quantity"] == 3
    assert data["condition"] == "LP"


@pytest.mark.asyncio
async def test_update_item_not_found(client: AsyncClient):
    """Test updating a non-existent item."""
    fake_id = str(uuid4())
    response = await client.patch(f"/api/v1/collections/items/{fake_id}", json={"quantity": 2})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_item_success(client: AsyncClient, test_db_session: AsyncSession):
    """Test deleting an item."""
    item = CollectionItem(
        id=uuid4(),
        user_id=uuid4(),
        card_id=uuid4(),
        quantity=1,
        condition="NM",
        language="en",
        is_foil=False
    )
    test_db_session.add(item)
    await test_db_session.commit()
    
    response = await client.delete(f"/api/v1/collections/items/{item.id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_item_not_found(client: AsyncClient):
    """Test deleting a non-existent item."""
    fake_id = str(uuid4())
    response = await client.delete(f"/api/v1/collections/items/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_pagination(client: AsyncClient, test_db_session: AsyncSession):
    """Test pagination."""
    # Create 5 items
    for i in range(5):
        item = CollectionItem(
            id=uuid4(),
            user_id=uuid4(),
            card_id=uuid4(),
            quantity=1,
            condition="NM",
            language="en",
            is_foil=False
        )
        test_db_session.add(item)
    await test_db_session.commit()
    
    # First page with limit 2
    response = await client.get("/api/v1/collections/items/?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["limit"] == 2
    assert data["offset"] == 0
    assert data["total"] == 5


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data

