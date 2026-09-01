"""
Unit tests for /keepalive and /restart-router endpoints
Tests keep-alive functionality and router restart with role-based access
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


class TestKeepalive:
    """Test cases for GET/POST /keepalive endpoint"""
    
    def test_keepalive_get_success(self, client):
        """Test successful keep-alive with GET method"""
        response = client.get('/keepalive')
        
        assert response.status_code == 204
        assert response.data == b''
        
    def test_keepalive_post_success(self, client):
        """Test successful keep-alive with POST method"""
        response = client.post('/keepalive')
        
        assert response.status_code == 204
        assert response.data == b''
        
    def test_keepalive_no_content_type_required(self, client):
        """Test that keep-alive works without Content-Type header"""
        response = client.post('/keepalive', data='')
        
        assert response.status_code == 204
        
    def test_keepalive_with_query_params(self, client):
        """Test keep-alive ignores query parameters"""
        response = client.get('/keepalive?test=value')
        
        assert response.status_code == 204


class TestRestartRouter:
    """Test cases for POST /restart-router endpoint"""
    
    def test_restart_router_success_with_admin_role(self, client):
        """Test successful router restart with admin role"""
        with patch('bookApp.source.app.os.makedirs') as mock_makedirs:
            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_file.__enter__ = Mock(return_value=mock_file)
                mock_file.__exit__ = Mock(return_value=False)
                mock_open.return_value = mock_file
                
                response = client.post('/restart-router',
                                       headers={'X-App-Role': 'admin'})
                
                assert response.status_code == 200
                data = response.get_json()
                assert data['status'] == 'success'
                assert 'message' in data
                assert 'task_' in data['message']
                assert '.trigger' in data['message']
                
    def test_restart_router_unauthorized_without_role(self, client):
        """Test 403 when no role header is provided"""
        response = client.post('/restart-router')
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'Unauthorized' in data['error']
        assert 'your_role' in data
        assert data['your_role'] == 'standard'
        
    def test_restart_router_unauthorized_with_standard_role(self, client):
        """Test 403 when standard role is provided"""
        response = client.post('/restart-router',
                               headers={'X-App-Role': 'standard'})
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'Unauthorized' in data['error']
        
    def test_restart_router_unauthorized_with_wrong_role(self, client):
        """Test 403 when wrong role is provided"""
        response = client.post('/restart-router',
                               headers={'X-App-Role': 'user'})
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'Unauthorized' in data['error']
        assert data['your_role'] == 'user'
        
    def test_restart_router_only_accepts_post(self, client):
        """Test that restart-router only accepts POST method"""
        response = client.get('/restart-router',
                              headers={'X-App-Role': 'admin'})
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405
        
    def test_restart_router_creates_unique_filename(self, client):
        """Test that each request creates a unique trigger file"""
        with patch('bookApp.source.app.os.makedirs') as mock_makedirs:
            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_file.__enter__ = Mock(return_value=mock_file)
                mock_file.__exit__ = Mock(return_value=False)
                mock_open.return_value = mock_file
                
                response1 = client.post('/restart-router',
                                        headers={'X-App-Role': 'admin'})
                response2 = client.post('/restart-router',
                                        headers={'X-App-Role': 'admin'})
                
                assert response1.status_code == 200
                assert response2.status_code == 200
                
                # Messages should be different (unique UUIDs)
                msg1 = response1.get_json()['message']
                msg2 = response2.get_json()['message']
                assert msg1 != msg2
                
    def test_restart_router_file_write_error(self, client):
        """Test 500 error when file write fails"""
        with patch('bookApp.source.app.os.makedirs') as mock_makedirs:
            with patch('builtins.open', create=True) as mock_open:
                mock_open.side_effect = Exception("Permission denied")
                
                response = client.post('/restart-router',
                                       headers={'X-App-Role': 'admin'})
                
                assert response.status_code == 500
                data = response.get_json()
                assert data['status'] == 'error'
                assert 'message' in data
                
    def test_restart_router_uses_shared_dir(self, client):
        """Test that trigger file is created in shared directory"""
        with patch('bookApp.source.app.os.makedirs') as mock_makedirs:
            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_file.__enter__ = Mock(return_value=mock_file)
                mock_file.__exit__ = Mock(return_value=False)
                mock_open.return_value = mock_file
                
                response = client.post('/restart-router',
                                       headers={'X-App-Role': 'admin'})
                
                assert response.status_code == 200
                # Verify makedirs was called with SHARED_DIR
                mock_makedirs.assert_called_once()
                args, kwargs = mock_makedirs.call_args
                assert args[0] == '/app/shared'
                
    def test_restart_router_writes_run_content(self, client):
        """Test that trigger file contains 'run' content"""
        with patch('bookApp.source.app.os.makedirs'):
            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_file.__enter__ = Mock(return_value=mock_file)
                mock_file.__exit__ = Mock(return_value=False)
                mock_open.return_value = mock_file
                
                response = client.post('/restart-router',
                                       headers={'X-App-Role': 'admin'})
                
                assert response.status_code == 200
                # Verify file.write was called with 'run'
                mock_file.write.assert_called_once_with('run')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
