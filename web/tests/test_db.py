import pytest
import psycopg2
import os

os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'your_db_name'
os.environ['DB_USER'] = 'your_username'
os.environ['DB_PASSWORD'] = 'your_password'

