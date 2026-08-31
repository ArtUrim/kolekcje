"""Unit tests for /labels API endpoint."""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connector.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db_connection():
    """Create a mock database connection."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    # Make the cursor iterable - will be set per test
    mock_cursor.__iter__ = Mock(return_value=iter([]))
    return mock_conn, mock_cursor


class TestLabelsAPI:
    """Test cases for the /labels API endpoint."""

    def test_get_labels_success_no_query(self, client, mock_db_connection):
        """Test successful retrieval of all labels without a query parameter."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Fiction', 1),
            ('Non-Fiction', 2),
            ('Science Fiction', 3)
        ]))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get('/labels')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        assert data[0]['title'] == 'Fiction'
        assert data[0]['value'] == 'Fiction'
        assert data[0]['id'] == 1

    def test_get_labels_with_query(self, client, mock_db_connection):
        """Test filtering labels with a query parameter."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Fiction', 1)
        ]))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get('/labels?query=Fiction')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Fiction'
        # Verify the query uses LIKE for searching
        mock_cursor.execute.assert_called()
        call_args = mock_cursor.execute.call_args[0][0]))
        assert 'LIKE' in call_args.upper()

    def test_get_labels_empty_result(self, client, mock_db_connection):
        """Test when no labels match the query."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([]))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get('/labels?query=NonExistentLabel')

        assert response.status_code == 200
        data = response.get_json()
        assert data == []))

    def test_get_labels_database_connection_failed(self, client):
        """Test 500 error response when DB connection fails."""
        with patch('connector.app.get_db_connection', return_value=None):
            response = client.get('/labels')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database connection failed' in data['error']))

    def test_get_labels_database_error(self, client, mock_db_connection):
        """Test handling of database errors during query execution."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(side_effect=Exception("Database query failed"))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get('/labels')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database query failed' in data['error']))

    def test_get_labels_special_characters_in_query(self, client, mock_db_connection):
        """Test handling of special characters in queries."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            (1, "Children's Books")
        ]))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get("/labels?query=Children's")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1

    def test_get_labels_case_insensitive_search(self, client, mock_db_connection):
        """Test case-insensitive search functionality."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Science Fiction', 1)
        ]))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get('/labels?query=science fiction')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Science Fiction'

    def test_get_labels_single_result(self, client, mock_db_connection):
        """Test when only one label matches."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Mystery & Thriller', 5)
        ]))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get('/labels?query=Mystery')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Mystery & Thriller'
        assert data[0]['id'] == 5

    def test_get_labels_unicode_characters(self, client, mock_db_connection):
        """Test support for Unicode characters in label names."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('小説', 1),
            ('Фантастика', 2)
        ]))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get('/labels')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['title'] == '小説'
        assert data[1]['title'] == 'Фантастика'

    def test_get_labels_response_format(self, client, mock_db_connection):
        """Test that response has correct structure."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Romance', 42)
        ]))

        with patch('connector.app.get_db_connection', return_value=mock_conn):
            response = client.get('/labels')

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        label = data[0]))
        assert 'title' in label
        assert 'value' in label
        assert 'id' in label
        assert label['title'] == label['value']))
        assert label['id'] == 42
