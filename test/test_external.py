import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.external_services.requests.get')
def test_import_external_product(mock_get, client):
    # Mocking successful OpenFoodFacts response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mocked Chocolate Bar",
            "brands": "Mock Brand"
        }
    }

    response = client.post('/api/external/import/123456789', json={"quantity": 5, "price": 1.99})
    assert response.status_code == 201
    assert response.json['data']['name'] == "Mocked Chocolate Bar"