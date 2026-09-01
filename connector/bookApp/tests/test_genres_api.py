import pytest
import json
from unittest.mock import Mock, patch, MagicMock
import mariadb


class TestGenresAPI:
    """Unit tests for the /genres API endpoint"""

    @pytest.fixture
    def mock_db_connection(self):
        """Create a mock database connection"""
        mock_conn = Mock(spec=mariadb.connections.Connection)
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn, mock_cursor

    def test_get_genres_success_no_query(self, client, mock_db_connection):
        """Test successful retrieval of all genres without query parameter"""
        mock_conn, mock_cursor = mock_db_connection

        # Mock cursor iteration to return genre rows
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Fiction', 1),
            ('Non-Fiction', 2),
            ('Science Fiction', 3)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/genres')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)
            assert len(data) == 3
            assert data[0] == {'title': 'Fiction', 'value': 'Fiction', 'id': 1}
            assert data[1] == {'title': 'Non-Fiction', 'value': 'Non-Fiction', 'id': 2}
            assert data[2] == {'title': 'Science Fiction', 'value': 'Science Fiction', 'id': 3}

    def test_get_genres_with_query(self, client, mock_db_connection):
        """Test retrieval of genres with query parameter"""
        mock_conn, mock_cursor = mock_db_connection

        # Mock cursor iteration to return filtered genre rows
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Science Fiction', 3),
            ('Fantasy Science', 5)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/genres?query=sci-fi')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)
            assert len(data) == 2

            # Verify the query was passed correctly (case-insensitive LIKE)
            mock_cursor.execute.assert_called_once()
            call_args = mock_cursor.execute.call_args
            sql_query = call_args[0][0]
            sql_params = call_args[0][1]

            assert 'LIKE' in sql_query
            assert 'LOWER' in sql_query
            assert '%sci-fi%' in sql_params

    def test_get_genres_empty_result(self, client, mock_db_connection):
        """Test retrieval of genres when no matches found"""
        mock_conn, mock_cursor = mock_db_connection

        # Mock empty result set
        mock_cursor.__iter__ = Mock(return_value=iter([]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/genres?query=nonexistent')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)
            assert len(data) == 0

    def test_get_genres_database_connection_failed(self, client):
        """Test behavior when database connection fails"""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/genres')

            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
            assert data['error'] == 'Database connection failed'

    def test_get_genres_database_error(self, client, mock_db_connection):
        """Test behavior when database error occurs during query"""
        mock_conn, mock_cursor = mock_db_connection

        # Mock database error
        mock_cursor.__iter__ = Mock(side_effect=mariadb.Error("Query failed"))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/genres')

            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
            assert 'Database error' in data['error']

    def test_get_genres_special_characters_in_query(self, client, mock_db_connection):
        """Test retrieval of genres with special characters in query"""
        mock_conn, mock_cursor = mock_db_connection

        # Mock cursor iteration to return genre rows
        mock_cursor.__iter__ = Mock(return_value=iter([
            ("Romance & Drama", 10)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/genres?query=romance%20%26%20drama')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 1
            assert data[0]['title'] == "Romance & Drama"

    def test_get_genres_case_insensitive_search(self, client, mock_db_connection):
        """Test that genre search is case-insensitive"""
        mock_conn, mock_cursor = mock_db_connection

        # Mock cursor iteration - should match regardless of case
        mock_cursor.__iter__ = Mock(return_value=iter([
            ('fiction', 1),
            ('FICTION', 2)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            # Query with uppercase
            response = client.get('/genres?query=FICTION')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 2

    def test_get_genres_single_result(self, client, mock_db_connection):
        """Test retrieval when only one genre matches"""
        mock_conn, mock_cursor = mock_db_connection

        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Mystery', 7)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/genres?query=mystery')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 1
            assert data[0] == {'title': 'Mystery', 'value': 'Mystery', 'id': 7}

    def test_get_genres_unicode_characters(self, client, mock_db_connection):
        """Test retrieval of genres with unicode characters"""
        mock_conn, mock_cursor = mock_db_connection

        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Наукова фантастика', 15),  # Ukrainian
            ('科学幻想小说', 16)  # Chinese
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/genres')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 2
            assert data[0]['title'] == 'Наукова фантастика'
            assert data[1]['title'] == '科学幻想小说'

    def test_get_genres_response_format(self, client, mock_db_connection):
        """Test that response has correct format structure"""
        mock_conn, mock_cursor = mock_db_connection

        mock_cursor.__iter__ = Mock(return_value=iter([
            ('Thriller', 20)
        ]))

        with patch('bookApp.core.db.get_db_connection', return_value=mock_conn):
            response = client.get('/genres')

            assert response.status_code == 200
            data = json.loads(response.data)

            # Each item should have title, value, and id fields
            for item in data:
                assert 'title' in item
                assert 'value' in item
                assert 'id' in item
                # title and value should be the same
                assert item['title'] == item['value']
                # id should be an integer
                assert isinstance(item['id'], int)
