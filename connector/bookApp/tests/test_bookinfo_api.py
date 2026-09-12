"""
Unit tests for GET /books/{book_id} endpoint
Tests book info retrieval by ID
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_db_connection():
    """Mock database connection fixture"""
    with patch('bookApp.core.db.get_db_connection') as mock_get_connection:
        mock_conn = Mock()
        mock_get_connection.return_value = mock_conn
        yield mock_get_connection, mock_conn


class TestBookInfoGET:
    """Test cases for GET /books/{book_id} endpoint"""

    def test_get_bookinfo_success(self, client, mock_db_connection):
        """Test successful retrieval of book info by ID"""
        mock_get_connection, mock_conn = mock_db_connection

        # Mock BookInfoHandler
        with patch('bookApp.services.bookinfo_service.BookInfoRepository') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_book_info.return_value = {
                'id': 1,
                'title': 'Test Book',
                'author': 'Test Author'
            }
            MockHandler.return_value = mock_handler_instance

            response = client.get('/books/1')

            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == 1

    def test_get_bookinfo_invalid_id_format(self, client, mock_db_connection):
        """Test error when book ID is not a valid integer"""
        response = client.get('/books/abc')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'Not found' in data['error']

    def test_get_bookinfo_not_found(self, client, mock_db_connection):
        """Test 404 when book doesn't exist"""
        mock_get_connection, mock_conn = mock_db_connection

        with patch('bookApp.services.bookinfo_service.BookInfoRepository') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_book_info.return_value = None
            MockHandler.return_value = mock_handler_instance

            response = client.get('/books/999')

            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
            assert 'Book not found' in data['error']

    def test_get_bookinfo_database_connection_failed(self, client):
        """Test 500 error when database connection fails"""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/books/1')

            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Database connection failed'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
