import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that index page loads correctly"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Users List' in rv.data

def test_db_connection(client):
    """Test database connection and data retrieval"""
    rv = client.get('/')
    assert rv.status_code == 200
    # Check if the test user is in the response
    assert b'Popov Aleksandr' in rv.data
    assert b'hochu_otl.com' in rv.data

@pytest.mark.parametrize("route", [
    '/nonexistent',
    '/api/users',
    '/admin'
])
def test_nonexistent_routes(client, route):
    """Test handling of nonexistent routes"""
    rv = client.get(route)
    assert rv.status_code == 404
