import pytest
from app import app
import psycopg2
import os

os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'your_db_name'
os.environ['DB_USER'] = 'your_username'
os.environ['DB_PASSWORD'] = 'your_password'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db_connection(monkeypatch):
    class MockCursor:
        def execute(self, query):
            pass
            
        def fetchall(self):
            return [
                (1, "Test User", "test@example.com"),
                (2, "Another User", "another@example.com")
            ]
            
        def close(self):
            pass
    
    class MockConnection:
        def cursor(self):
            return MockCursor()
            
        def close(self):
            pass
    
    def mock_get_connection(*args, **kwargs):
        return MockConnection()
    
    monkeypatch.setattr(psycopg2, "connect", mock_get_connection)
