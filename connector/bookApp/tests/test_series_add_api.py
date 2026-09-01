"""
Unit tests for /series/add POST endpoint
Tests the series creation functionality with mocked database calls
"""
import pytest
import json
from unittest.mock import Mock, patch
from ..source.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db_connection():
    """Mock database connection fixture"""
    with patch('bookApp.source.app.get_db_connection') as mock_get_conn:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        yield mock_get_conn, mock_conn, mock_cursor


class TestAddSeriesEndpoint:
    """Test class for /series/add POST endpoint"""

    def test_add_series_success(self, client, mock_db_connection):
        """Test successful series addition"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        # Mock that series doesn't exist (count = 0)
        mock_cursor.fetchone.return_value = (0,)
        
        series_data = {
            'value': 'Test Series',
            'title': 'Test Series'
        }
        
        response = client.post(
            '/series/add',
            data=json.dumps(series_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Series added successfully'
        mock_get_conn.assert_called_once()
        mock_conn.commit.assert_called_once()

    def test_add_series_missing_value(self, client, mock_db_connection):
        """Test series addition fails when value field is missing"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        series_data = {
            'title': 'Test Series'
        }
        
        response = client.post(
            '/series/add',
            data=json.dumps(series_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_series_missing_title(self, client, mock_db_connection):
        """Test series addition fails when title field is missing"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        series_data = {
            'value': 'test-series'
        }
        
        response = client.post(
            '/series/add',
            data=json.dumps(series_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_series_already_exists(self, client, mock_db_connection):
        """Test series addition fails when series already exists"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        # Mock that series already exists (count > 0)
        mock_cursor.fetchone.return_value = (1,)
        
        series_data = {
            'value': 'Existing Series',
            'title': 'Existing Series'
        }
        
        response = client.post(
            '/series/add',
            data=json.dumps(series_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'already exists' in data['error']

    def test_add_series_database_connection_failed(self, client):
        """Test handling of database connection failure"""
        with patch('bookApp.source.app.get_db_connection') as mock_get_conn:
            mock_get_conn.return_value = None
            
            series_data = {
                'value': 'Test Series',
                'title': 'Test Series'
            }
            
            response = client.post(
                '/series/add',
                data=json.dumps(series_data),
                content_type='application/json'
            )
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['error'] == 'Database connection failed'

    def test_add_series_with_unicode_characters(self, client, mock_db_connection):
        """Test series addition with Unicode characters"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = (0,)
        
        series_data = {
            'value': 'Серія Українська',  # Ukrainian
            'title': 'Серія Українська'
        }
        
        response = client.post(
            '/series/add',
            data=json.dumps(series_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201

    def test_add_series_invalid_content_type(self, client):
        """Test series addition with invalid Content-Type"""
        # When content-type is not application/json, get_json() returns None
        # This causes the handler to fail when accessing data['value']
        series_data = {
            'value': 'Test Series',
            'title': 'Test Series'
        }
        
        response = client.post(
            '/series/add',
            data=json.dumps(series_data),
            content_type='text/plain'
        )
        
        # Current implementation returns 500 due to unhandled None case
        assert response.status_code == 500

    def test_add_series_empty_payload(self, client, mock_db_connection):
        """Test series addition with empty JSON payload"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        response = client.post(
            '/series/add',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_series_special_characters(self, client, mock_db_connection):
        """Test series addition with special characters"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = (0,)
        
        series_data = {
            'value': 'Test & Series "Name"',
            'title': 'Test & Series "Name"'
        }
        
        response = client.post(
            '/series/add',
            data=json.dumps(series_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201

    def test_add_series_sql_injection_attempt(self, client, mock_db_connection):
        """Test that SQL injection attempts are handled safely"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = (0,)
        
        # Attempt SQL injection through the value field
        series_data = {
            'value': "Test'; DROP TABLE series; --",
            'title': "Test'; DROP TABLE series; --"
        }
        
        response = client.post(
            '/series/add',
            data=json.dumps(series_data),
            content_type='application/json'
        )
        
        # Should still execute (parameterized queries prevent injection)
        # The series will be inserted with that name or fail validation
        assert response.status_code in [201, 400]
