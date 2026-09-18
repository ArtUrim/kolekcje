"""Unit tests for /languages/stats and /language/<id> API endpoints."""
import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def mock_db_connection():
    """Create a mock database connection."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    # Make the cursor iterable - will be set per test
    mock_cursor.__iter__ = Mock(return_value=iter([]))
    return mock_conn, mock_cursor


class TestLanguagesStatsAPI:
    """Test cases for the /languages/stats API endpoint."""

    def test_get_languages_stats_success(self, client, mock_db_connection):
        """Test successful retrieval of language statistics."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('polski', 'pl_', 12),
            ('angielski', 'en_', 3),
            ('koreański', 'kr_', 0),
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/languages/stats')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        assert data[0] == {'value': 'polski', 'id': 'pl_', 'count': 12}
        assert data[1] == {'value': 'angielski', 'id': 'en_', 'count': 3}
        assert data[2] == {'value': 'koreański', 'id': 'kr_', 'count': 0}

        # Languages are counted directly through the Books.language_id column
        sql = mock_cursor.execute.call_args[0][0]
        assert 'LEFT JOIN Books' in sql
        assert 'language_id' in sql

    def test_get_languages_stats_empty_result(self, client, mock_db_connection):
        """Test when no languages exist."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/languages/stats')

        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    def test_get_languages_stats_database_connection_failed(self, client):
        """Test handling of database connection failure."""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/languages/stats')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    def test_get_languages_stats_database_error(self, client, mock_db_connection):
        """Test handling of database query error."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(side_effect=Exception("Database query failed"))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/languages/stats')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database query failed' in data['error']


class TestLanguageBooksAPI:
    """Test cases for the /language/<id> API endpoint."""

    def test_get_language_books_success(self, client, mock_db_connection):
        """Test successful retrieval of books for a language."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            (1, 'Solaris'),
            (2, 'Cyberiada'),
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/language/pl_')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0] == {'id': 1, 'title': 'Solaris'}
        assert data[1] == {'id': 2, 'title': 'Cyberiada'}

        # Books are looked up through the Books.language_id column; language
        # ids are char(3) codes, so the id is passed as a string
        sql = mock_cursor.execute.call_args[0][0]
        assert 'language_id' in sql
        assert mock_cursor.execute.call_args[0][1] == ['pl_']

    def test_get_language_books_empty_result(self, client, mock_db_connection):
        """Test retrieval of books for a language with no books."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/language/zz_')

        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    def test_get_language_books_database_connection_failed(self, client):
        """Test handling of database connection failure."""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/language/pl_')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    def test_get_language_books_database_error(self, client, mock_db_connection):
        """Test handling of database query error."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(side_effect=Exception("Database query failed"))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/language/pl_')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database query failed' in data['error']
