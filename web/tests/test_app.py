import pytest
import allure
import os

os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'your_db_name'
os.environ['DB_USER'] = 'your_username'
os.environ['DB_PASSWORD'] = 'your_password'

@allure.feature('Web Application')
class TestWebApp:
    
    @allure.story('Homepage')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_index_page(self, client, mock_db_connection):
        """Test if the index page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b"Users List" in response.data
        assert b"Test User" in response.data
        assert b"test@example.com" in response.data

    @allure.story('Database')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_db_connection_environment_variables(self):
        """Test if all required environment variables are set"""
        required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        for var in required_vars:
            assert var in os.environ, f"Environment variable {var} is not set"
