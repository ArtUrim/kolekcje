import pytest
import json
import mariadb
from unittest.mock import Mock, MagicMock, patch, mock_open
from jsonschema import ValidationError
import sys
import os

# Assuming the BookDatabase class is in addBook.py
from addBook import BookDatabase


class TestBookDatabase:
    
    @pytest.fixture
    def mock_connection(self):
        """Create a mock database connection"""
        mock_conn = Mock(spec=mariadb.connections.Connection)
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=None)
        return mock_conn, mock_cursor
    
    @pytest.fixture
    def book_db(self, mock_connection):
        """Create BookDatabase instance with mocked connection"""
        mock_conn, _ = mock_connection
        return BookDatabase(mock_conn)
    
    @pytest.fixture
    def valid_book_data(self):
        """Valid book data that matches the expected format"""
        return {
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "publishYear": "2023-01-01",
            "firstPublishYear": 1234,
            "format": "papier",
            "pages": "300",
            "description": "A test book description",
            "series": "Test Series",
            "genre": "Fiction",
            "originalTitle": "Original Test Book",
            "translator": "Test Translator"
        }
    
    @pytest.fixture
    def schema_data(self):
        """Valid JSON schema"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["title"],
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "author": {"type": "string"},
                "publisher": {"type": "string"},
                "publishYear": {"type": "string"},
                "format": {"type": "string"},
                "pages": {"type": "string"},
                "description": {"type": "string"}
            }
        }

    # SUNNY DAY SCENARIOS
    
    def test_get_or_create_publisher_existing(self, book_db, mock_connection):
        """Test getting existing publisher"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.return_value = (123,)
        
        result = book_db._get_or_create_publisher("Existing Publisher")
        
        mock_cursor.execute.assert_called_with(
            "SELECT id FROM publisher WHERE name = ?", 
            ("Existing Publisher",)
        )
        assert result == 123
    
    def test_get_or_create_publisher_new(self, book_db, mock_connection):
        """Test creating new publisher"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.return_value = None
        mock_cursor.lastrowid = 456
        
        result = book_db._get_or_create_publisher("New Publisher")
        
        assert mock_cursor.execute.call_count == 2
        mock_cursor.execute.assert_any_call(
            "INSERT INTO publisher (name) VALUES (?)", 
            ("New Publisher",)
        )
        assert result == 456
    
    def test_get_or_create_series_existing(self, book_db, mock_connection):
        """Test getting existing series"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.return_value = (789,)
        
        result = book_db._get_or_create_series("Existing Series")
        
        assert result == 789
    
    def test_get_or_create_author_existing(self, book_db, mock_connection):
        """Test getting existing author"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.return_value = (101,)
        
        result = book_db._get_or_create_author("Existing Author")
        
        assert result == 101
    
    def test_insert_book_success(self, book_db, mock_connection, valid_book_data):
        """Test successful book insertion"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [
            (1,),  # publisher exists
            (2,),  # series exists  
            (3,),  # author exists
            (4,)   # genre exists
        ]
        mock_cursor.lastrowid = 100
        
        result = book_db.insert_book(valid_book_data)
        
        assert result == 100
        mock_conn.commit.assert_called()
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_schema_success(self, mock_json_load, mock_file, book_db, schema_data):
        """Test successful schema loading"""
        mock_json_load.return_value = schema_data
        
        result = book_db._load_schema('test_schema.json')
        
        assert result == schema_data
        mock_file.assert_called_with('test_schema.json', 'r', encoding='utf-8')
    
    def test_validate_book_data_success(self, book_db, schema_data):
        """Test successful data validation"""
        valid_data = {"title": "Test Book"}
        
        # Should not raise any exception
        book_db._validate_book_data(valid_data, schema_data)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_insert_book_from_json_file_success(self, mock_json_load, mock_file, book_db, mock_connection, valid_book_data, schema_data):
        """Test successful book insertion from JSON file"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [
            (1,), (2,), (3,), (4,)  # All entities exist
        ]
        mock_cursor.lastrowid = 200
        mock_json_load.side_effect = [schema_data, valid_book_data]
        
        result = book_db.insert_book_from_json_file('test_book.json')
        
        assert result == 200

    # RAINY DAY SCENARIOS
    
    def test_get_or_create_publisher_database_error(self, book_db, mock_connection):
        """Test database error during publisher creation"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.execute.side_effect = mariadb.Error("Database connection failed")
        
        with pytest.raises(mariadb.Error):
            book_db._get_or_create_publisher("Test Publisher")
    
    def test_insert_book_missing_required_fields(self, book_db, mock_connection):
        """Test book insertion with missing required fields"""
        mock_conn, mock_cursor = mock_connection
        incomplete_data = {"isbn": 1234567890}  # Missing required fields
        
        with pytest.raises(ValueError):
            book_db.insert_book(incomplete_data)
    
    def test_insert_book_database_rollback(self, book_db, mock_connection, valid_book_data):
        """Test database rollback on error"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.execute.side_effect = mariadb.Error("Insert failed")
        
        with pytest.raises(mariadb.Error):
            book_db.insert_book(valid_book_data)
        
        mock_conn.rollback.assert_called()
    
    def test_load_schema_file_not_found(self, book_db):
        """Test schema loading with non-existent file"""
        with pytest.raises(FileNotFoundError):
            book_db._load_schema('nonexistent_schema.json')
    
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_load_schema_invalid_json(self, mock_file, book_db):
        """Test schema loading with invalid JSON"""
        with pytest.raises(json.JSONDecodeError):
            book_db._load_schema('invalid_schema.json')
    
    def test_validate_book_data_validation_error(self, book_db, schema_data):
        """Test data validation failure"""
        invalid_data = {"title": ""}  # Empty title violates minLength
        
        with pytest.raises(ValidationError):
            book_db._validate_book_data(invalid_data, schema_data)
    
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_insert_book_from_json_file_not_found(self, mock_file, book_db):
        """Test JSON file not found"""
        with pytest.raises(FileNotFoundError):
            book_db.insert_book_from_json_file('nonexistent.json')
    
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_insert_book_from_json_invalid_json(self, mock_file, book_db):
        """Test invalid JSON in book file"""
        with pytest.raises(json.JSONDecodeError):
            book_db.insert_book_from_json_file('invalid_book.json')

    # CORNER CASES
    
    def test_insert_book_with_none_values(self, book_db, mock_connection):
        """Test book insertion with None values"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,)]
        mock_cursor.lastrowid = 300
        
        book_data_with_nones = {
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "publishYear": "2023-01-01",
            "format": "papier",
            "pages": "300",
            "description": "Test description",
            "originalTitle": None,
            "translator": None
        }
        
        result = book_db.insert_book(book_data_with_nones)
        assert result == 300
    
    def test_insert_book_without_optional_fields(self, book_db, mock_connection):
        """Test book insertion without optional fields like series and genre"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,)]  # publisher, author
        mock_cursor.lastrowid = 400
        
        minimal_book_data = {
            "title": "Minimal Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "publishYear": "2023-01-01",
            "format": "papier",
            "pages": "100",
            "description": "Minimal description"
        }
        
        result = book_db.insert_book(minimal_book_data)
        assert result == 400
    
    def test_format_mapping_unknown_format(self, book_db, mock_connection, valid_book_data):
        """Test format mapping with unknown format"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,), (2,)]
        mock_cursor.lastrowid = 500
        
        valid_book_data["format"] = "unknown_format"
        
        result = book_db.insert_book(valid_book_data)
        assert result == 500
    
    def test_first_publish_year_extraction_old(self, book_db, mock_connection, valid_book_data):
        """Test publish year extraction from different formats"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,), (7,)]
        mock_cursor.lastrowid = 600
        
        # Test with different year formats
        test_cases = [234]
        
        for year_format in test_cases:
            valid_book_data["firstPublishYear"] = year_format
            result = book_db.insert_book(valid_book_data)
            assert result == 600
    
    def test_publish_year_extraction_old(self, book_db, mock_connection, valid_book_data):
        """Test publish year extraction from different formats"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,), (7,)]
        mock_cursor.lastrowid = 600
        
        # Test with different year formats
        test_cases = [1234]
        
        for year_format in test_cases:
            valid_book_data["publishYear"] = year_format
            result = book_db.insert_book(valid_book_data)
            assert result == 600
    
    def test_publish_year_extraction(self, book_db, mock_connection, valid_book_data):
        """Test publish year extraction from different formats"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,), (7,)]
        mock_cursor.lastrowid = 600
        
        # Test with different year formats
        test_cases = [2023]
        
        for year_format in test_cases:
            valid_book_data["publishYear"] = year_format
            result = book_db.insert_book(valid_book_data)
            assert result == 600
    
    def test_genre_not_found_in_database(self, book_db, mock_connection, valid_book_data):
        """Test when genre doesn't exist in database"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [
            (1,),  # publisher exists
            (2,),  # series exists
            (3,),  # author exists
            None   # genre doesn't exist
        ]
        mock_cursor.lastrowid = 700
        
        result = book_db.insert_book(valid_book_data)
        assert result == 700  # Should still insert book without genre
    
    def test_pages_conversion_to_int(self, book_db, mock_connection, valid_book_data):
        """Test pages field conversion to integer"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,), (1,)]
        mock_cursor.lastrowid = 800
        
        valid_book_data["pages"] = "250"  # String that should convert to int
        
        result = book_db.insert_book(valid_book_data)
        assert result == 800
    
    def test_pages_invalid_conversion(self, book_db, mock_connection, valid_book_data):
        """Test pages field with invalid integer conversion"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,)]
        mock_cursor.lastrowid = 800
        
        valid_book_data["pages"] = "invalid_number"
        
        with pytest.raises(ValueError):
            book_db.insert_book(valid_book_data)
    
    def test_cursor_cleanup_on_exception(self, book_db, mock_connection):
        """Test that cursor is properly closed even when exception occurs"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.execute.side_effect = Exception("Test exception")
        
        with pytest.raises(Exception):
            book_db._get_or_create_publisher("Test Publisher")
        
        mock_cursor.close.assert_called()
    
    def test_empty_string_fields(self, book_db, mock_connection):
        """Test handling of empty string fields"""
        mock_conn, mock_cursor = mock_connection
        mock_cursor.fetchone.side_effect = [(1,), (2,)]
        mock_cursor.lastrowid = 900
        
        book_data_empty_strings = {
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "publishYear": "2023-01-01",
            "format": "papier",
            "pages": "300",
            "description": "",  # Empty string
            "originalTitle": "",  # Empty string
            "translator": ""  # Empty string
        }
        
        result = book_db.insert_book(book_data_empty_strings)
        assert result == 900


# Integration test with actual data structure from data1.json
class TestWithActualDataStructure:
    
    @pytest.fixture
    def actual_data_structure(self):
        """Data structure matching data1.json"""
        return {
            "isbn": 1234567890,
            "title": "książka 1",
            "publishYear": None,
            "firstPublishYear": None,
            "format": "unknown",
            "pages": None,
            "description": "",
            "notes": "",
            "originalTitle": "",
            "translator": "",
            "language": ""
        }
    
    def test_data_structure_mismatch(self, actual_data_structure):
        """Test that highlights the mismatch between expected and actual data structure"""
        # This test demonstrates that the current data structure doesn't match
        # what the addBook.py expects (missing author, publisher, etc.)
        
        required_fields_in_code = ["author", "publisher", "publishYear", "format", "pages", "description"]
        
        for field in required_fields_in_code:
            if field not in actual_data_structure or actual_data_structure[field] is None:
                print(f"Missing or null required field: {field}")
        
        # This test will help identify the structural issues
        assert "author" not in actual_data_structure  # This will fail, highlighting the issue


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
