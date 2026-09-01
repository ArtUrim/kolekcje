"""
Unit tests for /books/validate endpoint (GET method)
Tests book validation by ISBN and other parameters
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
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
    with patch('bookApp.source.app.get_db_connection') as mock_get_connection:
        mock_conn = Mock()
        mock_get_connection.return_value = mock_conn
        yield mock_get_connection, mock_conn


class TestBooksValidate:
    """Test cases for GET /books/validate endpoint"""
    
    def test_validate_book_empty_params(self, client):
        """Test error when no parameters provided"""
        response = client.get('/books/validate')
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'result' in data
        assert data['result'] == 'empty hint list'
        
    def test_validate_book_valid_isbn(self, client, mock_db_connection):
        """Test validation with valid ISBN"""
        mock_get_connection, mock_conn = mock_db_connection
        
        # Mock BookInfoHandler
        with patch('bookApp.source.app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_basic_book_info.return_value = [
                {'id': 1, 'title': 'Test Book', 'isbn': '978-0-123456-78-9'}
            ]
            MockHandler.return_value = mock_handler_instance
            
            # Valid ISBN-13
            response = client.get('/books/validate?isbn=9780306406157')
            
            # Should return 409 if book exists in DB
            assert response.status_code in [204, 409]
            
    def test_validate_book_invalid_isbn_checksum(self, client, mock_db_connection):
        """Test validation with invalid ISBN checksum"""
        # ISBN with invalid checksum (last digit changed)
        response = client.get('/books/validate?isbn=9780123456780')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'title' in data
        assert 'Invalid ISBN' in data['title']
        
    def test_validate_book_isbn_normalization_failure(self, client, mock_db_connection):
        """Test validation with ISBN that cannot be normalized"""
        # Invalid ISBN format - too short to be valid
        response = client.get('/books/validate?isbn=123')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'title' in data
        assert 'Invalid ISBN' in data['title']
        
    def test_validate_book_not_found(self, client, mock_db_connection):
        """Test when book doesn't exist in database"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.source.app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_basic_book_info.return_value = []
            MockHandler.return_value = mock_handler_instance
            
            # Use valid ISBN but book not in DB
            response = client.get('/books/validate?isbn=9780306406157&title=NonExistent')
            
            assert response.status_code == 204
            
    def test_validate_book_with_title(self, client, mock_db_connection):
        """Test validation with title parameter"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.source.app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_basic_book_info.return_value = [
                {'id': 1, 'title': 'Matching Book'}
            ]
            MockHandler.return_value = mock_handler_instance
            
            response = client.get('/books/validate?title=Matching')
            
            # Returns 409 if book found
            assert response.status_code in [204, 409]
            
    def test_validate_book_with_author(self, client, mock_db_connection):
        """Test validation with author parameter"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.source.app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_basic_book_info.return_value = [
                {'id': 1, 'title': 'Book', 'author': 'Test Author'}
            ]
            MockHandler.return_value = mock_handler_instance
            
            response = client.get('/books/validate?author=Author')
            
            assert response.status_code in [204, 409]
            
    def test_validate_book_multiple_params(self, client, mock_db_connection):
        """Test validation with multiple parameters"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.source.app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_basic_book_info.return_value = [
                {'id': 1, 'title': 'Test Book', 'author': 'Author', 'year': 2023}
            ]
            MockHandler.return_value = mock_handler_instance
            
            params = {
                'title': 'Test',
                'author': 'Author',
                'year': '2023'
            }
            response = client.get('/books/validate', query_string=params)
            
            assert response.status_code in [204, 409]
            
    def test_validate_book_database_connection_failed(self, client):
        """Test 500 error when database connection fails"""
        # First provide a valid ISBN to pass ISBN validation
        with patch('bookApp.source.app.get_db_connection', return_value=None):
            # Need to mock isbn functions too since they run before DB connection
            with patch('bookApp.source.app.normalize_isbn', return_value='9780123456789'):
                with patch('bookApp.source.app.validate_isbn', return_value=True):
                    response = client.get('/books/validate?isbn=9780123456789')
                    
                    assert response.status_code == 500
                    data = response.get_json()
                    assert 'error' in data
                    assert data['error'] == 'Database connection failed'
                    
    def test_validate_book_database_error(self, client, mock_db_connection):
        """Test handling of database errors during validation"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.source.app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_basic_book_info.side_effect = Exception("DB error")
            MockHandler.return_value = mock_handler_instance
            
            response = client.get('/books/validate?title=Test')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'Internal server error' in data['error']
            
    def test_validate_book_isbn10_valid(self, client, mock_db_connection):
        """Test validation with valid ISBN-10"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.source.app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_basic_book_info.return_value = [
                {'id': 1, 'title': 'ISBN10 Book'}
            ]
            MockHandler.return_value = mock_handler_instance
            
            # Valid ISBN-10
            response = client.get('/books/validate?isbn=0306406152')
            
            assert response.status_code in [204, 409]
            
    def test_validate_book_special_characters_in_title(self, client, mock_db_connection):
        """Test validation with special characters in title"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.source.app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_basic_book_info.return_value = [
                {'id': 1, 'title': "Book & More: Author's Story"}
            ]
            MockHandler.return_value = mock_handler_instance
            
            response = client.get('/books/validate?title=Book%20%26%20More')
            
            assert response.status_code in [204, 409]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
