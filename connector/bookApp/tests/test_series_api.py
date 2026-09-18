"""Unit tests for /series API endpoint."""
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


class TestSeriesAPI:
    """Test cases for the /series API endpoint."""

    def test_get_series_success_no_query(self, client, mock_db_connection):
        """Test successful retrieval of all series without a query parameter."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Harry Potter', 1),
            ('The Lord of the Rings', 2),
            ('A Song of Ice and Fire', 3)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        assert data[0]['title'] == 'Harry Potter'
        assert data[0]['value'] == 'Harry Potter'
        assert data[0]['id'] == 1

    def test_get_series_with_query(self, client, mock_db_connection):
        """Test filtering series with a query parameter."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Harry Potter', 1)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series?query=Potter')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Harry Potter'
        # Verify the query uses LIKE for searching
        mock_cursor.execute.assert_called()
        call_args = mock_cursor.execute.call_args[0][0]
        assert 'LIKE' in call_args.upper()

    def test_get_series_empty_result(self, client, mock_db_connection):
        """Test when no series match the query."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series?query=NonExistentSeries')

        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    def test_get_series_database_connection_failed(self, client):
        """Test 500 error response when DB connection fails."""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/series')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database connection failed' in data['error']

    def test_get_series_database_error(self, client, mock_db_connection):
        """Test handling of database errors during query execution."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(side_effect=Exception("Database query failed"))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database query failed' in data['error']

    def test_get_series_special_characters_in_query(self, client, mock_db_connection):
        """Test handling of special characters in queries."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ("The Hitchhiker's Guide to the Galaxy", 1)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get("/series?query=Hitchhiker's")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1

    def test_get_series_case_insensitive_search(self, client, mock_db_connection):
        """Test case-insensitive search functionality."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Harry Potter', 1)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series?query=harry potter')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Harry Potter'

    def test_get_series_single_result(self, client, mock_db_connection):
        """Test when only one series matches."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('The Wheel of Time', 5)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series?query=Wheel')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'The Wheel of Time'
        assert data[0]['id'] == 5

    def test_get_series_unicode_characters(self, client, mock_db_connection):
        """Test support for Unicode characters in series names."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('三体', 1),
            ('Ведьмак', 2)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['title'] == '三体'
        assert data[1]['title'] == 'Ведьмак'

    def test_get_series_response_format(self, client, mock_db_connection):
        """Test that response has correct structure."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('The Hunger Games', 42)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series')

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        series = data[0]
        assert 'title' in series
        assert 'value' in series
        assert 'id' in series
        assert series['title'] == series['value']
        assert series['id'] == 42


class TestSeriesStatsAPI:
    """Test cases for the /series/stats API endpoint."""

    def test_get_series_stats_success(self, client, mock_db_connection):
        """Test successful retrieval of series statistics."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Harry Potter', 1, 7),
            ('The Hunger Games', 2, 0),
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series/stats')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0] == {'value': 'Harry Potter', 'id': 1, 'count': 7}
        assert data[1] == {'value': 'The Hunger Games', 'id': 2, 'count': 0}

        # Series are counted directly through the Books.series_id column
        sql = mock_cursor.execute.call_args[0][0]
        assert 'LEFT JOIN Books' in sql

    def test_get_series_stats_database_connection_failed(self, client):
        """Test handling of database connection failure."""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/series/stats')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    def test_get_series_stats_database_error(self, client, mock_db_connection):
        """Test handling of database query error."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(side_effect=Exception("Database query failed"))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series/stats')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data


class TestSeriesBooksAPI:
    """Test cases for the /series/<id> API endpoint."""

    def test_get_series_books_success(self, client, mock_db_connection):
        """Test successful retrieval of books for a series."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([
            (1, "Harry Potter and the Philosopher's Stone"),
            (2, 'Harry Potter and the Chamber of Secrets'),
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series/1')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0] == {'id': 1, 'title': "Harry Potter and the Philosopher's Stone"}
        assert data[1] == {'id': 2, 'title': 'Harry Potter and the Chamber of Secrets'}

    def test_get_series_books_empty_result(self, client, mock_db_connection):
        """Test retrieval of books for a series with no books."""
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.__iter__ = Mock(return_value=iter([]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/series/999')

        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    def test_get_series_books_database_connection_failed(self, client):
        """Test handling of database connection failure."""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/series/1')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
