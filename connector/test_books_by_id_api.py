"""
Unit tests for /books/<book_id> endpoint (GET, PUT, DELETE methods)
Tests retrieval, update, and deletion of specific books by ID
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db_connection():
    """Mock database connection fixture"""
    with patch('app.get_db_connection') as mock_get_connection:
        mock_conn = Mock()
        mock_get_connection.return_value = mock_conn
        yield mock_get_connection, mock_conn


class TestBooksByIdGET:
    """Test cases for GET /books/<book_id> endpoint"""
    
    def test_get_book_by_id_success(self, client, mock_db_connection):
        """Test successful retrieval of book by ID"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_book_info.return_value = {
                'id': 1,
                'title': 'Test Book',
                'author': 'Test Author',
                'year': 2023
            }
            MockHandler.return_value = mock_handler_instance
            
            response = client.get('/books/1')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == 1
            assert data['title'] == 'Test Book'
            
    def test_get_book_by_id_not_found(self, client, mock_db_connection):
        """Test 404 when book doesn't exist"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_book_info.return_value = None
            MockHandler.return_value = mock_handler_instance
            
            response = client.get('/books/999')
            
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
            assert 'Book not found' in data['error']
            
    def test_get_book_by_id_database_connection_failed(self, client):
        """Test 500 error when database connection fails"""
        with patch('app.get_db_connection', return_value=None):
            response = client.get('/books/1')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Database connection failed'
            
    def test_get_book_by_id_database_error(self, client, mock_db_connection):
        """Test handling of database errors during retrieval"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookInfoHandler') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_book_info.side_effect = Exception("DB error")
            MockHandler.return_value = mock_handler_instance
            
            response = client.get('/books/1')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'Internal server error' in data['error']


class TestBooksByIdPUT:
    """Test cases for PUT /books/<book_id> endpoint (update book)"""
    
    def test_update_book_by_id_success(self, client, mock_db_connection):
        """Test successful book update by ID"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookUpdateDatabase') as MockDB:
            mock_db_instance = Mock()
            mock_db_instance.update_book.return_value = {'success': True}
            MockDB.return_value = mock_db_instance
            
            update_data = {'title': 'Updated Title', 'year': 2024}
            response = client.put('/books/1',
                                  json=update_data,
                                  content_type='application/json')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'success'
            assert data['book_id'] == 1
            
    def test_update_book_by_id_not_found(self, client, mock_db_connection):
        """Test 404 when updating non-existent book"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookUpdateDatabase') as MockDB:
            mock_db_instance = Mock()
            mock_db_instance.update_book.return_value = {'not_found': True}
            MockDB.return_value = mock_db_instance
            
            response = client.put('/books/999',
                                  json={'title': 'Test'},
                                  content_type='application/json')
            
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
            assert 'Book not found' in data['error']
            
    def test_update_book_by_id_wrong_content_type(self, client, mock_db_connection):
        """Test error when Content-Type is not application/json"""
        response = client.put('/books/1',
                              data='title=Test',
                              content_type='application/x-www-form-urlencoded')
        
        assert response.status_code == 415
        data = response.get_json()
        assert 'error' in data
        assert 'Content-Type must be application/json' in data['error']
        
    def test_update_book_by_id_no_json_data(self, client, mock_db_connection):
        """Test error when no JSON data is provided"""
        # Send empty body with correct content type
        response = client.put('/books/1',
                              data='',
                              content_type='application/json')
        
        # Flask/app returns 500 when get_json() fails to parse empty body
        # This is caught by the exception handler in the route
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        
    def test_update_book_by_id_validation_error(self, client, mock_db_connection):
        """Test 400 error on validation failure"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookUpdateDatabase') as MockDB:
            mock_db_instance = Mock()
            mock_db_instance.update_book.side_effect = ValueError("Invalid data")
            MockDB.return_value = mock_db_instance
            
            response = client.put('/books/1',
                                  json={'invalid': 'data'},
                                  content_type='application/json')
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
            assert 'Invalid data' in data['error']
            
    def test_update_book_by_id_database_error(self, client, mock_db_connection):
        """Test 500 error on database failure"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookUpdateDatabase') as MockDB:
            mock_db_instance = Mock()
            mock_db_instance.update_book.side_effect = Exception("DB error")
            MockDB.return_value = mock_db_instance
            
            response = client.put('/books/1',
                                  json={'title': 'Test'},
                                  content_type='application/json')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'Internal server error' in data['error']
            
    def test_update_book_by_id_database_connection_failed(self, client):
        """Test 500 error when database connection fails"""
        with patch('app.get_db_connection', return_value=None):
            response = client.put('/books/1',
                                  json={'title': 'Test'},
                                  content_type='application/json')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Database connection failed'


class TestBooksByIdDELETE:
    """Test cases for DELETE /books/<book_id> endpoint"""
    
    def test_delete_book_by_id_success(self, client, mock_db_connection):
        """Test successful book deletion by ID"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookUpdateDatabase') as MockDB:
            mock_db_instance = Mock()
            mock_db_instance.delete_book.return_value = {'success': True}
            MockDB.return_value = mock_db_instance
            
            response = client.delete('/books/1')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'success'
            assert data['book_id'] == 1
            
    def test_delete_book_by_id_not_found(self, client, mock_db_connection):
        """Test 404 when deleting non-existent book"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookUpdateDatabase') as MockDB:
            mock_db_instance = Mock()
            mock_db_instance.delete_book.return_value = {'not_found': True}
            MockDB.return_value = mock_db_instance
            
            response = client.delete('/books/999')
            
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
            assert 'Book not found' in data['error']
            
    def test_delete_book_by_id_database_connection_failed(self, client):
        """Test 500 error when database connection fails"""
        with patch('app.get_db_connection', return_value=None):
            response = client.delete('/books/1')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Database connection failed'
            
    def test_delete_book_by_id_database_error(self, client, mock_db_connection):
        """Test 500 error on database failure during deletion"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('app.BookUpdateDatabase') as MockDB:
            mock_db_instance = Mock()
            mock_db_instance.delete_book.side_effect = Exception("DB error")
            MockDB.return_value = mock_db_instance
            
            response = client.delete('/books/1')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'Internal server error' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
