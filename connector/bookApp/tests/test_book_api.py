"""
Unit tests for /books endpoint (GET method)
Tests book retrieval with query parameters
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_db_connection():
    """Mock database connection fixture"""
    with patch('bookApp.core.db.get_db_connection') as mock_get_connection:
        mock_conn = Mock()
        mock_cursor = Mock()
        
        # Setup cursor to be iterable and support fetchall
        mock_cursor.fetchall.return_value = [(5,)]  # For FOUND_ROWS()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        
        yield mock_get_connection, mock_conn, mock_cursor


class TestGetBooks:
    """Test cases for GET /books endpoint"""
    
    def test_get_books_success_no_params(self, client, mock_db_connection):
        """Test successful retrieval of books without query parameters"""
        mock_get_connection, mock_conn, mock_cursor = mock_db_connection
        
        # Mock cursor iteration to return sample books
        # Default fields are: id, title, author, publisher, release_date, series_name (6 columns)
        sample_books = [
            (1, "Book One", "Author One", "Publisher One", "2023-01-01", "Series One"),
            (2, "Book Two", "Author Two", "Publisher Two", "2023-02-01", "Series Two"),
        ]
        mock_cursor.__iter__ = Mock(return_value=iter(sample_books))
        mock_cursor.fetchall.return_value = [(2,)]  # For FOUND_ROWS()
        
        response = client.get('/books')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'count' in data
        assert 'books' in data
        assert len(data['books']) == 2
        
    def test_get_books_with_query_params(self, client, mock_db_connection):
        """Test book retrieval with various query parameters"""
        mock_get_connection, mock_conn, mock_cursor = mock_db_connection
        
        sample_books = [(1, "Test Book", "Test Author", "Publisher", "2023-01-01", "Series")]
        mock_cursor.__iter__ = Mock(return_value=iter(sample_books))
        mock_cursor.fetchall.return_value = [(1,)]
        
        response = client.get('/books?title=Test&author=Author')
        
        assert response.status_code == 200
        # Verify query was executed
        assert mock_cursor.execute.called
        
    def test_get_books_empty_result(self, client, mock_db_connection):
        """Test when no books match the query"""
        mock_get_connection, mock_conn, mock_cursor = mock_db_connection
        
        # Empty results
        mock_cursor.__iter__ = Mock(return_value=iter([]))
        mock_cursor.fetchall.return_value = [(0,)]
        
        response = client.get('/books?title=NonExistent')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0
        assert data['books'] == []
        
    def test_get_books_database_connection_failed(self, client):
        """Test 500 error when database connection fails"""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/books')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Database connection failed'
            
    def test_get_books_database_error(self, client, mock_db_connection):
        """Test handling of database errors during query execution"""
        mock_get_connection, mock_conn, mock_cursor = mock_db_connection
        
        # Simulate database error
        import mariadb
        mock_cursor.execute.side_effect = mariadb.Error("Database query failed")
        
        response = client.get('/books')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Database error' in data['error']
        
    def test_get_books_multiple_params(self, client, mock_db_connection):
        """Test book retrieval with multiple query parameters"""
        mock_get_connection, mock_conn, mock_cursor = mock_db_connection
        
        sample_books = [(1, "Book", "Author", "Publisher", "2023-01-01", "Series")]
        mock_cursor.__iter__ = Mock(return_value=iter(sample_books))
        mock_cursor.fetchall.return_value = [(1,)]
        
        params = {
            'title': 'Test',
            'author': 'Author',
            'year': '2023',
            'isbn': '1234567890'
        }
        response = client.get('/books', query_string=params)
        
        assert response.status_code == 200
        assert mock_cursor.execute.called
        
    def test_get_books_special_characters_in_query(self, client, mock_db_connection):
        """Test handling of special characters in query parameters"""
        mock_get_connection, mock_conn, mock_cursor = mock_db_connection
        
        sample_books = [(1, "Book & More", "Author's Name", "Publisher", "2023-01-01", "Series")]
        mock_cursor.__iter__ = Mock(return_value=iter(sample_books))
        mock_cursor.fetchall.return_value = [(1,)]
        
        response = client.get('/books?title=Book%20%26%20More')
        
        assert response.status_code == 200
        
    def test_get_books_response_format(self, client, mock_db_connection):
        """Test that response has correct structure"""
        mock_get_connection, mock_conn, mock_cursor = mock_db_connection
        
        sample_books = [(1, "Test Book", "Test Author", "Publisher", "2023-01-01", "Series")]
        mock_cursor.__iter__ = Mock(return_value=iter(sample_books))
        mock_cursor.fetchall.return_value = [(1,)]
        
        response = client.get('/books')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert 'count' in data
        assert 'books' in data
        assert isinstance(data['books'], list)
        
    def test_get_books_single_book(self, client, mock_db_connection):
        """Test retrieval of a single book"""
        mock_get_connection, mock_conn, mock_cursor = mock_db_connection
        
        sample_books = [(1, "Single Book", "Single Author", "Publisher", "2023-01-01", "Series")]
        mock_cursor.__iter__ = Mock(return_value=iter(sample_books))
        mock_cursor.fetchall.return_value = [(1,)]
        
        response = client.get('/books?id=1')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 1
        assert len(data['books']) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
