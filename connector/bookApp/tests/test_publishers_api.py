"""Unit tests for /publishers API endpoint."""
import pytest
from unittest.mock import Mock, patch

from ..source.app import app


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


class TestPublishersAPI:
    """Test cases for the /publishers API endpoint."""

    def test_get_publishers_success_no_query(self, client, mock_db_connection):
        """Test successful retrieval of all publishers without a query parameter."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Penguin Random House', 1),
            ('HarperCollins', 2),
            ('Simon & Schuster', 3)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/publishers')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        assert data[0]['title'] == 'Penguin Random House'
        assert data[0]['value'] == 'Penguin Random House'
        assert data[0]['id'] == 1

    def test_get_publishers_with_query(self, client, mock_db_connection):
        """Test filtering publishers with a query parameter."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Penguin Random House', 1)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/publishers?query=Penguin')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Penguin Random House'
        # Verify the query uses LIKE for searching
        mock_cursor.execute.assert_called()
        call_args = mock_cursor.execute.call_args[0][0]
        assert 'LIKE' in call_args.upper()

    def test_get_publishers_empty_result(self, client, mock_db_connection):
        """Test when no publishers match the query."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/publishers?query=NonExistentPublisher')

        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    def test_get_publishers_database_connection_failed(self, client):
        """Test 500 error response when DB connection fails."""
        with patch('bookApp.source.app.get_db_connection', return_value=None):
            response = client.get('/publishers')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database connection failed' in data['error']

    def test_get_publishers_database_error(self, client, mock_db_connection):
        """Test handling of database errors during query execution."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(side_effect=Exception("Database query failed"))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/publishers')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database query failed' in data['error']

    def test_get_publishers_special_characters_in_query(self, client, mock_db_connection):
        """Test handling of special characters in queries."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ("Hachette Livre", 1)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get("/publishers?query=Hachette")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1

    def test_get_publishers_case_insensitive_search(self, client, mock_db_connection):
        """Test case-insensitive search functionality."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Penguin Random House', 1)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/publishers?query=penguin')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Penguin Random House'

    def test_get_publishers_single_result(self, client, mock_db_connection):
        """Test when only one publisher matches."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Macmillan Publishers', 5)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/publishers?query=Macmillan')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Macmillan Publishers'
        assert data[0]['id'] == 5

    def test_get_publishers_unicode_characters(self, client, mock_db_connection):
        """Test support for Unicode characters in publisher names."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('講談社', 1),
            ('Издательство Эксмо', 2)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/publishers')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['title'] == '講談社'
        assert data[1]['title'] == 'Издательство Эксмо'

    def test_get_publishers_response_format(self, client, mock_db_connection):
        """Test that response has correct structure."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Bloomsbury Publishing', 42)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/publishers')

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        publisher = data[0]
        assert 'title' in publisher
        assert 'value' in publisher
        assert 'id' in publisher
        assert publisher['title'] == publisher['value']
        assert publisher['id'] == 42
