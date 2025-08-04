import mariadb
from typing import Dict, Any, List, Optional, Union
import json
import sys
import jsonschema
from jsonschema import validate, ValidationError

import logging

class BookDatabase:
    def __init__(self, connection: mariadb.connections.Connection):
        self.connection = connection

    def _get_or_create_publisher(self, publisher_data: Union[str, Dict[str, Any]]) -> int:
        """Get publisher ID or create new publisher"""
        if isinstance(publisher_data, str):
            publisher_name = publisher_data.strip()
            if not publisher_name:
                raise ValueError("Publisher name cannot be empty")
            publisher_id = None
            is_custom = True
        elif isinstance(publisher_data, dict):
            publisher_name = publisher_data.get('title', '').strip()
            if not publisher_name:
                raise ValueError("Publisher name cannot be empty")
            publisher_id = publisher_data.get('id')
            is_custom = publisher_data.get('isCustom', True)
            if publisher_id is not None and not is_custom:
                return publisher_id
        else:
            raise ValueError("Invalid publisher data format")
            
        cursor = self.connection.cursor()
        try:
            # Check if publisher exists
            cursor.execute("SELECT id FROM publisher WHERE name = ?", (publisher_name,))
            result = cursor.fetchone()

            if result:
                return result[0]

            if is_custom:
                cursor.execute("INSERT INTO publisher (name) VALUES (?)", (publisher_name,))
                self.connection.commit()
                return cursor.lastrowid
            else:
                raise ValueError(f"Publisher {publisher_name} not found in database")
        finally:
            cursor.close()

    def _get_or_create_series(self, series_data: Union[str, Dict[str, Any]]) -> int:
        """Get series ID or create new series"""
        if isinstance(series_data, str):
            series_name = series_data.strip()
            if not series_name:
                raise ValueError("Publisher name cannot be empty")
            series_id = None
            is_custom = True
        elif isinstance(series_data, dict):
            series_name = series_data.get('title', '').strip()
            if not series_name:
                raise ValueError("Publisher name cannot be empty")
            series_id = series_data.get('id')
            is_custom = series_data.get('isCustom', True)
            if series_id is not None and not is_custom:
                return series_id
        else:
            raise ValueError("Invalid series data format")
            
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM series WHERE name = ?", (series_name,))
            result = cursor.fetchone()

            if result:
                return result[0]

            if is_custom:
                cursor.execute("INSERT INTO series (name) VALUES (?)", (series_name,))
                self.connection.commit()
                return cursor.lastrowid
            else:
                raise ValueError(f"Serie {series_name} not found in database")
        finally:
            cursor.close()

    def _get_or_create_author(self, author_data: Union[str, Dict[str, Any]]) -> int:
        """Get author ID or create new author"""
        if isinstance(author_data, str):
            author_name = author_data.strip()
            if not author_name:
                raise ValueError("Author name cannot be empty")
            author_id = None
            is_custom = True
        elif isinstance(author_data, dict):
            author_name = author_data.get('title', '').strip()
            if not author_name:
                raise ValueError("Author name cannot be empty")
            author_id = author_data.get('id')
            is_custom = author_data.get('isCustom', True)
            if author_id is not None and not is_custom:
                return author_id
        else:
            raise ValueError("Invalid author data format")

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM Authors WHERE name = ?", (author_name,))
            result = cursor.fetchone()

            if result:
                return result[0]

            if is_custom:
                cursor.execute("INSERT INTO Authors (name, nationality_id) VALUES (?, ?)",
                             (author_name, 'pl_'))
                self.connection.commit()
                return cursor.lastrowid
            else:
                raise ValueError(f"Author {author_name} not found in database")
        finally:
            cursor.close()

    def _get_or_create_label(self, label_name: str) -> Optional[int]:
        """Get label ID or create new label"""
        if not label_name or not label_name.strip():
            return None
            
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM labels WHERE name = ?", (label_name,))
            result = cursor.fetchone()

            if result:
                return result[0]

            cursor.execute("INSERT INTO labels (name) VALUES (?)", (label_name,))
            self.connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def _get_or_create_genre(self, genre_name: str) -> Optional[int]:
        """Get genre ID or create new genre"""
        if not genre_name or not genre_name.strip():
            return None
            
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM genres WHERE name = ?", (genre_name,))
            result = cursor.fetchone()

            if result:
                return result[0]

            cursor.execute("INSERT INTO genres (name) VALUES (?)", (genre_name,))
            self.connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def _process_array_field(self, field_data: Union[List[Dict], str, None]) -> List[str]:
        """Process array fields that can be either array of objects or simple strings"""
        if not field_data:
            return []
        
        if isinstance(field_data, str):
            return [field_data] if field_data.strip() else []
        
        if isinstance(field_data, list):
            result = []
            for item in field_data:
                if isinstance(item, dict) and 'title' in item:
                    title = item['title']
                    if title and title.strip():
                        result.append(title)
                elif isinstance(item, str) and item.strip():
                    result.append(item)
            return result
        
        return []

    def _safe_int_conversion(self, value: Any, field_name: str) -> Optional[int]:
        """Safely convert value to integer"""
        if value is None:
            return None
        
        if isinstance(value, int):
            return value
        
        if isinstance(value, str):
            if not value.strip():
                return None
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"Invalid integer value for {field_name}: {value}")
        
        raise ValueError(f"Cannot convert {type(value)} to integer for {field_name}")

    def _extract_year(self, year_data: Any) -> Optional[int]:
        """Extract year from various formats"""
        if year_data is None:
            return None
        
        if isinstance(year_data, int):
            return year_data
        
        if isinstance(year_data, str):
            if not year_data.strip():
                return None
            # Extract first 4 digits (year) from string like "2023-01-01"
            year_str = year_data[:4]
            try:
                return int(year_str)
            except ValueError:
                raise ValueError(f"Invalid year format: {year_data}")
        
        raise ValueError(f"Cannot extract year from {type(year_data)}: {year_data}")

    def _extract_isbn(self, isbn_data: Any) -> Optional[int]:
        """Extract isbn from various formats"""
        return isbn_data

    def _normalize_format(self, format_value: Any) -> str:
        """Normalize format value"""
        if not format_value:
            return 'unknown'
        
        format_str = str(format_value).lower().strip()
        
        format_mapping = {
            'papier': 'paperback',
            'paperback': 'paperback',
            'hardback': 'hardback',
            'hardcover': 'hardback',
            'ebook': 'ebook',
            'e-book': 'ebook',
            'unknown': 'unknown'
        }
        
        return format_mapping.get(format_str, 'unknown')

    def _get_default_language(self, language_data: Any) -> str:
        """Get language code with validation"""
        if not language_data or not str(language_data).strip():
            return 'pl_'  # Default to Polish
        
        lang_str = str(language_data).strip()
        
        # Basic validation for language code format (e.g., 'en_', 'pl_')
        if len(lang_str) >= 3:
            return lang_str
        elif len(lang_str) == 2:
            return lang_str + '_'
        
        return 'pl_'  # Default fallback

    def insert_book(self, book_data: Dict[str, Any]) -> int:
        """Insert book data into database with improved error handling and data processing"""
        cursor = self.connection.cursor()
        try:
            # Validate required fields
            if not book_data.get('title') or not str(book_data['title']).strip():
                raise ValueError("Title is required and cannot be empty")

            # Process authors (required)
            authors = self._process_array_field(book_data.get('author'))
            if not authors:
                logging.warning("No authors provided for the book")

            # Process publishers (required)
            publishers = self._process_array_field(book_data.get('publisher'))
            if not publishers:
                logging.warning("No publishers provided for the book")

            # Process series (optional)
            series_name = book_data.get('series')
            series_id = self._get_or_create_series(series_name) if series_name else None

            # Process other fields with proper null handling
            title = str(book_data['title']).strip()
            original_title = book_data.get('originalTitle')
            original_title = str(original_title).strip() if original_title else None
            
            # Handle publish year - try both publishYear and firstPublishYear
            publish_year = self._extract_year(book_data.get('publishYear'))
            firstPublYear = self._extract_year(book_data.get('firstPublishYear'))
            isbn = self._extract_isbn(book_data.get('isbn'))
            
            format_value = self._normalize_format(book_data.get('format'))
            pages = self._safe_int_conversion(book_data.get('pages'), 'pages')
            
            description = book_data.get('description', '')
            description = str(description) if description else ''
            
            notes = book_data.get('notes', '')
            notes = str(notes) if notes else ''
            
            translator = book_data.get('translator')
            translator = str(translator).strip() if translator else None
            
            language_id = self._get_default_language(book_data.get('language'))

            size = book_data.get('size')
            size = str(size).strip() if size and str(size).strip() else None

            # Insert book
            query = """
                INSERT INTO Books (
                    title, original_title, release_date, format, note,
                    pages, description, series_id, translator,
                    language_id, first_polish_release_date, isbn, size
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            values = (
                title,
                original_title,
                publish_year,
                format_value,
                notes,
                pages,
                description,
                series_id,
                translator,
                language_id,
                firstPublYear,
                isbn,
                size
            )

            cursor.execute(query, values)
            book_id = cursor.lastrowid


            # Insert author relationships
            for author_item in authors:
                author_id = self._get_or_create_author(author_item)
                cursor.execute(
                    "INSERT INTO bookAuthors (book_id, author_id) VALUES (?, ?)",
                    (book_id, author_id)
                )

            # Process labels (optional)
            labels = self._process_array_field(book_data.get('label'))
            for label_name in labels:
                label_id = self._get_or_create_label(label_name)
                if label_id:
                    cursor.execute(
                        "INSERT INTO bookLabel (book_id, label_id) VALUES (?, ?)",
                        (book_id, label_id)
                    )

            # Process genres (optional)
            genres = self._process_array_field(book_data.get('genre'))
            for genre_name in genres:
                genre_id = self._get_or_create_genre(genre_name)
                if genre_id:
                    cursor.execute(
                        "INSERT INTO bookGenres (book_id, genre_id) VALUES (?, ?)",
                        (book_id, genre_id)
                    )

            # Handle additional publishers if multiple
            for publisher_item in publishers:
                publisher_id = self._get_or_create_publisher(publisher_item)
                # Assuming there's a bookPublishers table for many-to-many relationship
                try:
                    cursor.execute(
                        "INSERT INTO bookPublishers (book_id, publisher_id) VALUES (?, ?)",
                        (book_id, publisher_id)
                    )
                except mariadb.Error:
                    # Table might not exist, skip additional publishers
                    pass

            self.connection.commit()
            return book_id

        except mariadb.Error as e:
            self.connection.rollback()
            print(f"Database error inserting book: {e}")
            raise
        except (ValueError, TypeError) as e:
            self.connection.rollback()
            print(f"Data validation error: {e}")
            raise
        finally:
            cursor.close()

    def _load_schema(self, schema_path: str) -> Dict[str, Any]:
        """Load JSON schema from file with better error handling"""
        try:
            with open(schema_path, 'r', encoding='utf-8') as file:
                schema = json.load(file)
                return schema
        except FileNotFoundError:
            print(f"Error: Schema file {schema_path} not found")
            raise
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in schema file {schema_path}: {e}")
            raise
        except Exception as e:
            print(f"Error loading schema file {schema_path}: {e}")
            raise

    def _validate_book_data(self, book_data: Dict[str, Any], schema: Dict[str, Any]) -> None:
        """Validate book data against JSON schema with detailed error reporting"""
        try:
            validate(instance=book_data, schema=schema)
        except ValidationError as e:
            error_path = ' -> '.join(str(x) for x in e.path) if e.path else 'root'
            print(f"Validation error at {error_path}: {e.message}")
            if e.context:
                print("Additional context:")
                for context_error in e.context:
                    context_path = ' -> '.join(str(x) for x in context_error.path) if context_error.path else 'root'
                    print(f"  {context_path}: {context_error.message}")
            raise

    def insert_book_from_json_file(self, json_file_path: str, schema_path: str = 'schemaBookNew.json') -> int:
        """Insert book data from JSON file with schema validation and better error handling"""
        try:
            # Load the JSON schema
            schema = self._load_schema(schema_path)

            # Load and parse the book data
            with open(json_file_path, 'r', encoding='utf-8') as file:
                book_data = json.load(file)

            # Validate the book data against the schema
            self._validate_book_data(book_data, schema)

            # If validation passes, insert the book
            return self.insert_book(book_data)

        except FileNotFoundError:
            print(f"Error: File {json_file_path} not found")
            raise
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in {json_file_path}: {e}")
            raise
        except ValidationError:
            print(f"Error: JSON data in {json_file_path} does not match the required schema")
            raise
        except Exception as e:
            print(f"Error processing {json_file_path}: {e}")
            raise

    def insert_book_from_dict(self, book_data: Dict[str, Any], schema_path: str = 'schemaBookNew.json') -> int:
        """Insert book data from dictionary with optional schema validation"""
        try:
            # Load and validate against schema if provided
            if schema_path:
                schema = self._load_schema(schema_path)
                self._validate_book_data(book_data, schema)

            return self.insert_book(book_data)

        except Exception as e:
            print(f"Error processing book data: {e}")
            raise

    def create_sample_data_structure(self) -> Dict[str, Any]:
        """Create a sample data structure that matches the expected format"""
        return {
            "isbn": 1234567890123,
            "title": "Sample Book Title",
            "author": [
                {"id": None, "title": "Author Name", "isCustom": True}
            ],
            "publisher": [
                {"id": None, "title": "Publisher Name", "isCustom": True}
            ],
            "publishYear": 2023,
            "firstPublishYear": 2020,
            "format": "paperback",
            "pages": 300,
            "description": "Book description",
            "notes": "Additional notes",
            "series": "Series Name",
            "genre": [
                {"id": None, "title": "Fiction", "isCustom": False}
            ],
            "originalTitle": "Original Title",
            "translator": "Translator Name",
            "language": "en_"
        }

# Example usage and migration helper
def migrate_old_format_to_new(old_data: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to migrate old data format to new expected format"""
    new_data = {}
    
    # Copy direct fields
    direct_fields = ['isbn', 'title', 'publishYear', 'firstPublishYear', 'format', 
                    'pages', 'description', 'notes', 'originalTitle', 'translator', 'language']
    
    for field in direct_fields:
        if field in old_data:
            new_data[field] = old_data[field]
    
    # Handle fields that need to be converted to array format
    # Note: This assumes we have default values since the old format doesn't have these
    if 'author' not in old_data:
        new_data['author'] = [{"id": None, "title": "Unknown Author", "isCustom": True}]
    
    if 'publisher' not in old_data:
        new_data['publisher'] = [{"id": None, "title": "Unknown Publisher", "isCustom": True}]
    
    if 'genre' not in old_data:
        new_data['genre'] = [{"id": None, "title": "Unknown", "isCustom": True}]
    
    return new_data

if __name__ == "__main__":
    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'katalog'
    }

    try:
        # Initialize database connection
        connection = mariadb.connect(**db_params)
        db = BookDatabase(connection)

        # Example of processing the data1.json format
        sample_old_data = {
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

        # Migrate old format to new format
        migrated_data = migrate_old_format_to_new(sample_old_data)
        
        # Insert the migrated data
        book_id = db.insert_book_from_dict(migrated_data, schema_path=None)  # Skip schema validation for migration
        print(f"Successfully inserted migrated book with ID: {book_id}")

        # List of JSON files to process (assuming they follow the new format)
        json_files = [
            'Czarownik.json',
            'ListyMilosne.json',
            'SnyPodFumarola.json',
            'UpadekJerycha.json'
        ]

        # Process each JSON file
        for json_file in json_files:
            try:
                book_id = db.insert_book_from_json_file(json_file)
                print(f"Successfully inserted book from {json_file} with ID: {book_id}")
            except Exception as e:
                print(f"Error processing {json_file}: {e}")

    except mariadb.Error as e:
        print(f"Database connection error: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
