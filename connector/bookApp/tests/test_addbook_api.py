"""
Unit tests for /addbook POST endpoint
Tests the book creation functionality with mocked database calls
"""
import pytest
import json
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
    with patch('bookApp.source.app.get_db_connection') as mock_get_conn:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        yield mock_get_conn, mock_conn, mock_cursor


class TestAddBookEndpoint:
    """Test class for /addbook POST endpoint"""

    def test_add_book_success_minimal_data(self, client, mock_db_connection):
        """Test successful book addition with minimal required data"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        # Mock cursor behavior for lastrowid
        mock_cursor.lastrowid = 1
        
        book_data = {
            'title': 'Test Book'
        }
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        assert response.status_code == 204
        mock_get_conn.assert_called_once()
        mock_conn.cursor.assert_called()
        mock_conn.commit.assert_called()

    def test_add_book_success_complete_data(self, client, mock_db_connection):
        """Test successful book addition with complete data"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 42
        
        book_data = {
            'title': 'Complete Test Book',
            'subtitle': 'A Complete Test',
            'author': ['Author One', 'Author Two'],
            'publisher': [{'title': 'Test Publisher', 'isCustom': True}],
            'series': {'title': 'Test Series', 'isCustom': True},
            'genre': ['Fiction', 'Adventure'],
            'label': ['New', 'Featured'],
            'publishYear': 2024,
            'isbn': '978-3-16-148410-0',
            'format': 'paperback',
            'pages': 300,
            'description': 'A test book description',
            'language': 'en_'
        }
        
        # Mock fetchone for various lookups
        mock_cursor.fetchone.side_effect = [
            None,  # publisher not found
            (1,),  # publisher insert lastrowid
            None,  # series not found
            (2,),  # series insert lastrowid
            None,  # author not found
            (3,),  # author insert lastrowid
            None,  # author not found
            (4,),  # author insert lastrowid
            None,  # label not found
            (5,),  # label insert lastrowid
            None,  # label not found
            (6,),  # label insert lastrowid
            None,  # genre not found
            (7,),  # genre insert lastrowid
            None,  # genre not found
            (8,),  # genre insert lastrowid
        ]
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        assert response.status_code == 204

    def test_add_book_missing_title(self, client, mock_db_connection):
        """Test book addition fails when title is missing"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        book_data = {
            'author': ['Some Author']
        }
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        assert response.status_code == 415
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_book_empty_title(self, client, mock_db_connection):
        """Test book addition fails when title is empty string"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        book_data = {
            'title': '   ',
            'author': ['Some Author']
        }
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        assert response.status_code == 415
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_book_invalid_content_type(self, client):
        """Test book addition fails with invalid Content-Type"""
        book_data = {
            'title': 'Test Book'
        }
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='text/plain'
        )
        
        assert response.status_code == 415
        data = json.loads(response.data)
        assert data['error'] == 'Unsupported Media Type'

    def test_add_book_database_connection_failed(self, client):
        """Test handling of database connection failure"""
        with patch('bookApp.source.app.get_db_connection') as mock_get_conn:
            mock_get_conn.return_value = None
            
            book_data = {
                'title': 'Test Book'
            }
            
            response = client.post(
                '/addbook',
                data=json.dumps(book_data),
                content_type='application/json'
            )
            
            # When DB connection fails, the code logs a warning but still returns 204
            # This is current behavior in app.py line 115-116
            assert response.status_code == 204

    def test_add_book_invalid_isbn(self, client, mock_db_connection):
        """Test book addition with invalid ISBN format"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        
        book_data = {
            'title': 'Test Book with Bad ISBN',
            'isbn': 'invalid-isbn-format'
        }
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        assert response.status_code == 415
        data = json.loads(response.data)
        assert 'error' in data
        assert 'ISBN' in data['error']

    def test_add_book_with_existing_author(self, client, mock_db_connection):
        """Test book addition with existing author (no new insert)"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 1
        
        # Mock that author already exists
        mock_cursor.fetchone.return_value = (99,)  # Existing author ID
        
        book_data = {
            'title': 'Test Book',
            'author': ['Existing Author']
        }
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        assert response.status_code == 204

    def test_add_book_with_unicode_characters(self, client, mock_db_connection):
        """Test book addition with Unicode characters in title and author"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 1
        mock_cursor.fetchone.return_value = None
        
        book_data = {
            'title': 'Книга з Україною',  # Ukrainian
            'author': ['Автор 中文名字'],  # Chinese
            'description': 'Description with émojis 📚'
        }
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        assert response.status_code == 204

    def test_add_book_multiple_publishers(self, client, mock_db_connection):
        """Test book addition with multiple publishers"""
        mock_get_conn, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 1
        
        # Mock for multiple publishers
        mock_cursor.fetchone.side_effect = [
            None,  # First publisher not found
            (1,),  # First publisher insert
            None,  # Second publisher not found
            (2,),  # Second publisher insert
        ]
        
        book_data = {
            'title': 'Test Book',
            'publisher': [
                {'title': 'Publisher One', 'isCustom': True},
                {'title': 'Publisher Two', 'isCustom': True}
            ]
        }
        
        response = client.post(
            '/addbook',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        assert response.status_code == 204

    def test_add_book_json_parsing_error(self, client):
        """Test handling of malformed JSON
        
        After fixing the bug in app.py, this should return 400 Bad Request.
        """
        response = client.post(
            '/addbook',
            data='not valid json{',
            content_type='application/json'
        )
        
        # After fixing the bug, should return 400 Bad Request for invalid JSON
        assert response.status_code == 400
        assert 'error' in response.get_json()
        assert 'Bad Request' in response.get_json()['error']
