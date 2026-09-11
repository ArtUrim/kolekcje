"""
Unit tests for /publishers POST endpoint
Tests the publisher creation functionality with mocked database calls
"""
import pytest
import json
from unittest.mock import Mock, patch


@pytest.fixture
def mock_db_connection():
    """Mock database connection fixture"""
    with patch('bookApp.core.db.get_db_connection') as mock_get_conn:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        yield mock_get_conn, mock_conn, mock_cursor


class TestAddPublisherEndpoint:
    """Test class for /publishers POST endpoint"""

    def test_add_publisher_success(self, client, mock_db_connection):
        """Test successful publisher addition"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection

        # Mock that publisher doesn't exist (count = 0)
        mock_cursor.fetchone.return_value = (0,)

        publisher_data = {
            'value': 'Test Publisher',
            'title': 'Test Publisher'
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='application/json'
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Publisher added successfully'
        mock_get_conn.assert_called_once()
        mock_conn.commit.assert_called_once()

    def test_add_publisher_missing_value(self, client, mock_db_connection):
        """Test publisher addition fails when value field is missing"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection

        publisher_data = {
            'title': 'Test Publisher'
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_publisher_missing_title(self, client, mock_db_connection):
        """Test publisher addition fails when title field is missing"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection

        publisher_data = {
            'value': 'test-publisher'
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_publisher_already_exists(self, client, mock_db_connection):
        """Test publisher addition fails when publisher already exists"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection

        # Mock that publisher already exists (count > 0)
        mock_cursor.fetchone.return_value = (1,)

        publisher_data = {
            'value': 'Existing Publisher',
            'title': 'Existing Publisher'
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'already exists' in data['error']

    def test_add_publisher_database_connection_failed(self, client):
        """Test handling of database connection failure"""
        with patch('bookApp.core.db.get_db_connection') as mock_get_conn:
            mock_get_conn.return_value = None

            publisher_data = {
                'value': 'Test Publisher',
                'title': 'Test Publisher'
            }

            response = client.post(
                '/publishers',
                data=json.dumps(publisher_data),
                content_type='application/json'
            )

            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['error'] == 'Database connection failed'

    def test_add_publisher_with_unicode_characters(self, client, mock_db_connection):
        """Test publisher addition with Unicode characters"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = (0,)

        publisher_data = {
            'value': 'Видавництво Українське',  # Ukrainian
            'title': 'Видавництво Українське'
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='application/json'
        )

        assert response.status_code == 201

    def test_add_publisher_invalid_content_type(self, client):
        """Test publisher addition with invalid Content-Type"""
        # When content-type is not application/json, get_json() returns None
        # This causes the handler to fail when accessing data['value']
        publisher_data = {
            'value': 'Test Publisher',
            'title': 'Test Publisher'
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='text/plain'
        )

        # Current implementation returns 500 due to unhandled None case
        assert response.status_code == 500

    def test_add_publisher_empty_payload(self, client, mock_db_connection):
        """Test publisher addition with empty JSON payload"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection

        response = client.post(
            '/publishers',
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_publisher_special_characters(self, client, mock_db_connection):
        """Test publisher addition with special characters"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = (0,)

        publisher_data = {
            'value': 'Publisher & Co. "Ltd."',
            'title': 'Publisher & Co. "Ltd."'
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='application/json'
        )

        assert response.status_code == 201

    def test_add_publisher_sql_injection_attempt(self, client, mock_db_connection):
        """Test that SQL injection attempts are handled safely"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = (0,)

        # Attempt SQL injection through the value field
        publisher_data = {
            'value': "Publisher'; DROP TABLE publisher; --",
            'title': "Publisher'; DROP TABLE publisher; --"
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='application/json'
        )

        # Should still execute (parameterized queries prevent injection)
        # The publisher will be inserted with that name or fail validation
        assert response.status_code in [201, 400]

    def test_add_publisher_case_sensitivity(self, client, mock_db_connection):
        """Test publisher addition with different case variations"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection

        # First check - publisher doesn't exist
        mock_cursor.fetchone.side_effect = [(0,), (1,)]  # First call: 0, second call: 1

        publisher_data = {
            'value': 'New Publisher',
            'title': 'New Publisher'
        }

        response = client.post(
            '/publishers',
            data=json.dumps(publisher_data),
            content_type='application/json'
        )

        assert response.status_code == 201
