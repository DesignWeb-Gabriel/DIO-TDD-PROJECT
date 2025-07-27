from typing import List
from unittest.mock import AsyncMock

import pytest
from tests.factories import product_data
from fastapi import status

# Mock data
MOCK_PRODUCT_OUT = {
    "id": "fce6cc37-10b9-4a8e-a8b2-977df327001a",
    "name": "Iphone 14 pro Max",
    "quantity": 10,
    "price": "8.500",
    "status": True,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
}


@pytest.fixture
def mock_usecase():
    return AsyncMock()


@pytest.fixture
def client_with_mock_usecase(mock_usecase):
    from store.main import app
    from store.controllers.product import get_product_usecase
    from fastapi.testclient import TestClient

    # Override the dependency
    app.dependency_overrides[get_product_usecase] = lambda: mock_usecase

    with TestClient(app) as test_client:
        yield test_client, mock_usecase

    # Clean up
    app.dependency_overrides.clear()


def test_controller_create_should_return_success(
    client_with_mock_usecase, products_url
):
    client, mock_usecase = client_with_mock_usecase

    # Arrange
    from store.core.schemas.product import ProductOut
    from uuid import UUID
    from datetime import datetime

    mock_product = ProductOut(
        id=UUID(MOCK_PRODUCT_OUT["id"]),
        name=MOCK_PRODUCT_OUT["name"],
        quantity=MOCK_PRODUCT_OUT["quantity"],
        price=MOCK_PRODUCT_OUT["price"],
        status=MOCK_PRODUCT_OUT["status"],
        created_at=datetime.fromisoformat(
            MOCK_PRODUCT_OUT["created_at"].replace("Z", "+00:00")
        ),
        updated_at=datetime.fromisoformat(
            MOCK_PRODUCT_OUT["updated_at"].replace("Z", "+00:00")
        ),
    )
    mock_usecase.create.return_value = mock_product

    # Act
    response = client.post(products_url, json=product_data())

    # Assert
    content = response.json()
    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


def test_controller_get_should_return_success(client_with_mock_usecase, products_url):
    client, mock_usecase = client_with_mock_usecase

    # Arrange
    from store.core.schemas.product import ProductOut
    from uuid import UUID
    from datetime import datetime

    mock_product = ProductOut(
        id=UUID(MOCK_PRODUCT_OUT["id"]),
        name=MOCK_PRODUCT_OUT["name"],
        quantity=MOCK_PRODUCT_OUT["quantity"],
        price=MOCK_PRODUCT_OUT["price"],
        status=MOCK_PRODUCT_OUT["status"],
        created_at=datetime.fromisoformat(
            MOCK_PRODUCT_OUT["created_at"].replace("Z", "+00:00")
        ),
        updated_at=datetime.fromisoformat(
            MOCK_PRODUCT_OUT["updated_at"].replace("Z", "+00:00")
        ),
    )
    mock_usecase.get.return_value = mock_product

    # Act
    product_id = "fce6cc37-10b9-4a8e-a8b2-977df327001a"
    response = client.get(f"{products_url}{product_id}")

    # Assert
    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": product_id,
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


def test_controller_get_should_return_not_found(client_with_mock_usecase, products_url):
    client, mock_usecase = client_with_mock_usecase

    # Arrange
    from store.core.exceptions import NotFoundException

    product_id = "4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    mock_usecase.get.side_effect = NotFoundException(
        message=f"Product not found with filter: {product_id}"
    )

    # Act
    response = client.get(f"{products_url}{product_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Product not found with filter: {product_id}"}


def test_controller_query_should_return_success(client_with_mock_usecase, products_url):
    client, mock_usecase = client_with_mock_usecase

    # Arrange
    from store.core.schemas.product import ProductOut
    from uuid import UUID
    from datetime import datetime

    mock_product = ProductOut(
        id=UUID(MOCK_PRODUCT_OUT["id"]),
        name=MOCK_PRODUCT_OUT["name"],
        quantity=MOCK_PRODUCT_OUT["quantity"],
        price=MOCK_PRODUCT_OUT["price"],
        status=MOCK_PRODUCT_OUT["status"],
        created_at=datetime.fromisoformat(
            MOCK_PRODUCT_OUT["created_at"].replace("Z", "+00:00")
        ),
        updated_at=datetime.fromisoformat(
            MOCK_PRODUCT_OUT["updated_at"].replace("Z", "+00:00")
        ),
    )
    mock_products = [mock_product, mock_product]
    mock_usecase.query.return_value = mock_products

    # Act
    response = client.get(products_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) == 2


def test_controller_patch_should_return_success(client_with_mock_usecase, products_url):
    client, mock_usecase = client_with_mock_usecase

    # Arrange
    from store.core.schemas.product import ProductUpdateOut
    from uuid import UUID
    from datetime import datetime
    from decimal import Decimal

    # Criar objeto diretamente sem passar pelo validator
    mock_product = ProductUpdateOut.model_construct(
        id=UUID(MOCK_PRODUCT_OUT["id"]),
        name=MOCK_PRODUCT_OUT["name"],
        quantity=MOCK_PRODUCT_OUT["quantity"],
        price=Decimal("7.500"),  # Usar Decimal normal
        status=MOCK_PRODUCT_OUT["status"],
        created_at=datetime.fromisoformat(
            MOCK_PRODUCT_OUT["created_at"].replace("Z", "+00:00")
        ),
        updated_at=datetime.fromisoformat(
            MOCK_PRODUCT_OUT["updated_at"].replace("Z", "+00:00")
        ),
    )
    mock_usecase.update.return_value = mock_product

    # Act
    product_id = "fce6cc37-10b9-4a8e-a8b2-977df327001a"
    response = client.patch(f"{products_url}{product_id}", json={"price": "7.500"})

    # Assert
    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": product_id,
        "quantity": 10,
        "price": "7.500",
        "status": True,
    }


def test_controller_delete_should_return_no_content(
    client_with_mock_usecase, products_url
):
    client, mock_usecase = client_with_mock_usecase

    # Arrange
    mock_usecase.delete.return_value = True

    # Act
    product_id = "fce6cc37-10b9-4a8e-a8b2-977df327001a"
    response = client.delete(f"{products_url}{product_id}")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_controller_delete_should_return_not_found(
    client_with_mock_usecase, products_url
):
    client, mock_usecase = client_with_mock_usecase

    # Arrange
    from store.core.exceptions import NotFoundException

    product_id = "4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    mock_usecase.delete.side_effect = NotFoundException(
        message=f"Product not found with filter: {product_id}"
    )

    # Act
    response = client.delete(f"{products_url}{product_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Product not found with filter: {product_id}"}
