"""Unit tests for /authors API endpoint."""
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


class TestAuthorsAPI:
    """Test cases for the /authors API endpoint."""

    def test_get_authors_success_no_query(self, client, mock_db_connection):
        """Test successful retrieval of all authors without a query parameter."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('J.K. Rowling', 1),
            ('George Orwell', 2),
            ('Jane Austen', 3)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/authors')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        assert data[0]['title'] == 'J.K. Rowling'
        assert data[0]['value'] == 'J.K. Rowling'
        assert data[0]['id'] == 1

    def test_get_authors_with_query(self, client, mock_db_connection):
        """Test filtering authors with a query parameter."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('J.K. Rowling', 1)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/authors?query=Rowling')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'J.K. Rowling'
        # Verify the query uses LIKE for searching
        mock_cursor.execute.assert_called()
        call_args = mock_cursor.execute.call_args[0][0]
        assert 'LIKE' in call_args.upper()

    def test_get_authors_empty_result(self, client, mock_db_connection):
        """Test when no authors match the query."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/authors?query=NonExistentAuthor')

        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    def test_get_authors_database_connection_failed(self, client):
        """Test 500 error response when DB connection fails."""
        with patch('bookApp.source.app.get_db_connection', return_value=None):
            response = client.get('/authors')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database connection failed' in data['error']

    def test_get_authors_database_error(self, client, mock_db_connection):
        """Test handling of database errors during query execution."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(side_effect=Exception("Database query failed"))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/authors')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database query failed' in data['error']

    def test_get_authors_special_characters_in_query(self, client, mock_db_connection):
        """Test handling of special characters in queries."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ("O'Connor, Patrick", 1)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get("/authors?query=O'Connor")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1

    def test_get_authors_case_insensitive_search(self, client, mock_db_connection):
        """Test case-insensitive search functionality."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('J.K. Rowling', 1)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/authors?query=rowling')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'J.K. Rowling'

    def test_get_authors_single_result(self, client, mock_db_connection):
        """Test when only one author matches."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Stephen King', 5)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/authors?query=King')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Stephen King'
        assert data[0]['id'] == 5

    def test_get_authors_unicode_characters(self, client, mock_db_connection):
        """Test support for Unicode characters in author names."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('村上春樹', 1),
            ('Гоголь', 2)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/authors')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['title'] == '村上春樹'
        assert data[1]['title'] == 'Гоголь'

    def test_get_authors_response_format(self, client, mock_db_connection):
        """Test that response has correct structure."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Agatha Christie', 42)
        ]))

        with patch('bookApp.source.app.get_db_connection', return_value=mock_conn):
            response = client.get('/authors')

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        author = data[0]
        assert 'title' in author
        assert 'value' in author
        assert 'id' in author
        assert author['title'] == author['value']
        assert author['id'] == 42
