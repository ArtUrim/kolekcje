import mariadb
from typing import Dict, Any
import json
import sys

class BookDatabase:
    def __init__(self, connection: mariadb.connections.Connection ):
        self.connection = connection

    def _get_or_create_publisher(self, publisher_name: str) -> int:
        """Get publisher ID or create new publisher"""
        cursor = self.connection.cursor()
        try:
            # Check if publisher exists
            cursor.execute("SELECT id FROM publisher WHERE name = ?", (publisher_name,))
            result = cursor.fetchone()

            if result:
                return result[0]

            # Create new publisher
            cursor.execute("INSERT INTO publisher (name) VALUES (?)", (publisher_name,))
            self.connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def _get_or_create_series(self, series_name: str) -> int:
        """Get series ID or create new series"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM series WHERE name = ?", (series_name,))
            result = cursor.fetchone()

            if result:
                return result[0]

            cursor.execute("INSERT INTO series (name) VALUES (?)", (series_name,))
            self.connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def _get_or_create_author(self, author_name: str) -> int:
        """Get author ID or create new author"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM Authors WHERE name = ?", (author_name,))
            result = cursor.fetchone()

            if result:
                return result[0]

            cursor.execute("INSERT INTO Authors (name, nationality_id) VALUES (?, 'pl_')",
                         (author_name,))
            self.connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def insert_book(self, book_data: Dict[str, Any]) -> int:
        """Insert book data into database"""
        cursor = self.connection.cursor()
        try:
            # Get or create required foreign keys
            publisher_id = self._get_or_create_publisher(book_data['publisher'])
            series_id = self._get_or_create_series(book_data['series']) if 'series' in book_data else None

            # Convert format from 'papier' to enum value
            format_mapping = {'papier': 'paperback'}
            format_value = format_mapping.get(book_data['format'], 'unknown')

            # Convert publish year to proper format
            publish_year = int(book_data['publishYear'][:4])

            # Insert book
            query = """
            INSERT INTO Books (
                title, original_title, release_date, format, publisher_id,
                pages, description, series_id, translator, language_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            values = (
                book_data['title'],
                book_data.get('originalTitle'),
                publish_year,
                format_value,
                publisher_id,
                int(book_data['pages']),
                book_data['description'],
                series_id,
                book_data.get('translator'),
                'pl_'  # Assuming Polish language as default
            )

            cursor.execute(query, values)
            book_id = cursor.lastrowid

            # Insert author relationship
            author_id = self._get_or_create_author(book_data['author'])
            cursor.execute(
                "INSERT INTO bookAuthors (book_id, author_id) VALUES (?, ?)",
                (book_id, author_id)
            )

            # Insert genre if present
            if 'genre' in book_data:
                cursor.execute("SELECT id FROM genres WHERE name = ?", (book_data['genre'],))
                genre_result = cursor.fetchone()
                if genre_result:
                    genre_id = genre_result[0]
                    cursor.execute(
                        "INSERT INTO bookGenres (book_id, genre_id) VALUES (?, ?)",
                        (book_id, genre_id)
                    )

            self.connection.commit()
            return book_id

        except mariadb.Error as e:
            self.connection.rollback()
            print(f"Error inserting book: {e}")
            raise
        finally:
            cursor.close()

    def insert_book_from_json_file(self, json_file_path: str) -> int:
        """Insert book data from JSON file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                book_data = json.load(file)
            return self.insert_book(book_data)
        except FileNotFoundError:
            print(f"Error: File {json_file_path} not found")
            raise
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {json_file_path}")
            raise

# Example usage:
if __name__ == "__main__":
    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'katalog'
    }

    # Initialize and connect to database
    db = BookDatabase(**db_params)
    db.connect()

    try:
        # List of JSON files to process
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

    finally:
        db.disconnect()

# Created/Modified files during execution:
# No files are created or modified during execution.
# The script only reads from JSON files and writes to the database.
