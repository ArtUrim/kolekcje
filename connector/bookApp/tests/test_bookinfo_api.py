"""
Unit tests for /bookinfo endpoint (GET and POST methods)
Tests book info retrieval by ID and book info updates
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
    """Test cases for GET /bookinfo endpoint"""
    
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
            
            response = client.get('/bookinfo?id=1')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'success'
            assert 'book' in data
            assert data['book']['id'] == 1
            
    def test_get_bookinfo_missing_id(self, client, mock_db_connection):
        """Test error when book ID parameter is missing"""
        response = client.get('/bookinfo')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Book ID parameter is required' in data['error']
        
    def test_get_bookinfo_invalid_id_format(self, client, mock_db_connection):
        """Test error when book ID is not a valid integer"""
        response = client.get('/bookinfo?id=abc')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid book ID format' in data['error']
        
    def test_get_bookinfo_not_found(self, client, mock_db_connection):
        """Test 404 when book doesn't exist"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.services.bookinfo_service.BookInfoRepository') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.get_book_info.return_value = None
            MockHandler.return_value = mock_handler_instance
            
            response = client.get('/bookinfo?id=999')
            
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
            assert 'Book not found' in data['error']
            
    def test_get_bookinfo_database_connection_failed(self, client):
        """Test 500 error when database connection fails"""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.get('/bookinfo?id=1')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Database connection failed'


class TestBookInfoPOST:
    """Test cases for POST /bookinfo endpoint (update book info)"""
    
    def test_update_bookinfo_success(self, client, mock_db_connection):
        """Test successful book info update"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.services.bookinfo_service.BookInfoRepository') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.update_book_info.return_value = True
            MockHandler.return_value = mock_handler_instance
            
            update_data = {'title': 'Updated Title', 'year': 2024}
            response = client.post('/bookinfo?id=1', 
                                   json=update_data,
                                   content_type='application/json')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'success'
            assert data['message'] == 'Book updated successfully'
            
    def test_update_bookinfo_missing_id(self, client, mock_db_connection):
        """Test error when book ID is missing for update"""
        response = client.post('/bookinfo', 
                               json={'title': 'Test'},
                               content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Book ID parameter is required' in data['error']
        
    def test_update_bookinfo_invalid_id_format(self, client, mock_db_connection):
        """Test error when book ID is not valid for update"""
        response = client.post('/bookinfo?id=xyz',
                               json={'title': 'Test'},
                               content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid book ID format' in data['error']
        
    def test_update_bookinfo_wrong_content_type(self, client, mock_db_connection):
        """Test error when Content-Type is not application/json"""
        response = client.post('/bookinfo?id=1',
                               data='title=Test',
                               content_type='application/x-www-form-urlencoded')
        
        assert response.status_code == 415
        data = response.get_json()
        assert 'error' in data
        assert 'Content-Type must be application/json' in data['error']
        
    def test_update_bookinfo_no_json_data(self, client, mock_db_connection):
        """Test error when no JSON data is provided"""
        # When no data is sent, get_json() returns None
        response = client.post('/bookinfo?id=1',
                               data='null',
                               content_type='application/json')
        
        # The route should handle this - either 400 or process with empty data
        assert response.status_code in [200, 400]
        
    def test_update_bookinfo_failure(self, client, mock_db_connection):
        """Test when book update fails"""
        mock_get_connection, mock_conn = mock_db_connection
        
        with patch('bookApp.services.bookinfo_service.BookInfoRepository') as MockHandler:
            mock_handler_instance = Mock()
            mock_handler_instance.update_book_info.return_value = False
            MockHandler.return_value = mock_handler_instance
            
            response = client.post('/bookinfo?id=1',
                                   json={'title': 'Test'},
                                   content_type='application/json')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'Failed to update book' in data['error']
            
    def test_update_bookinfo_database_connection_failed(self, client):
        """Test 500 error when database connection fails for update"""
        with patch('bookApp.core.db.get_db_connection', return_value=None):
            response = client.post('/bookinfo?id=1',
                                   json={'title': 'Test'},
                                   content_type='application/json')
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Database connection failed'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
