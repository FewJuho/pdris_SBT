import pytest
import os
import psycopg2
from app import app

@pytest.fixture(scope='session')
def database():
    params = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'database': os.environ.get('DB_NAME', 'postgres'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'passwd')
    }
    
    conn = psycopg2.connect(**params)
    yield conn
    
    conn.close()

@pytest.fixture(scope='function')
def db_cursor(database):
    cursor = database.cursor()
    yield cursor
    cursor.close()

@pytest.fixture(scope='session')
def app_context():
    with app.app_context():
        yield app
