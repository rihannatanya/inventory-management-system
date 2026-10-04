import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    response = client.get('/api/inventory')
    assert response.status_code == 200
    assert response.json['success'] is True

def test_create_inventory_item(client):
    payload = {"name": "Test Chips", "brand": "SnackCorp", "quantity": 10, "price": 2.50}
    response = client.post('/api/inventory', json=payload)
    assert response.status_code == 201
    assert response.json['data']['name'] == "Test Chips"

def test_patch_inventory_item(client):
    # Patch existing item #1
    payload = {"quantity": 99}
    response = client.patch('/api/inventory/1', json=payload)
    assert response.status_code == 200
    assert response.json['data']['quantity'] == 99

def test_delete_inventory_item(client):
    response = client.delete('/api/inventory/1')
    assert response.status_code == 200
    
    # Confirm deletion
    get_res = client.get('/api/inventory/1')
    assert get_res.status_code == 404