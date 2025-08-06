import mariadb
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BookInfoHandler:
    """Handler for managing book information updates."""

    def __init__(self, db_connection):
        self.connection = db_connection

    def get_book_info(self, book_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve complete book information from MariaDB.
        
        Args:
            book_id: Unique identifier of the book
            
        Returns:
            Dictionary containing complete book information or None if not found
        """
        cursor = self.connection.cursor()
        try:
            # Main book query with series and language information
            book_query = """
            SELECT 
                b.id,
                b.isbn,
                b.title,
                b.release_date,
                b.first_polish_release_date,
                b.format,
                b.pages,
                b.description,
                b.note,
                b.series_id,
                b.original_title,
                b.translator,
                b.language_id,
                b.size,
                s.name as series_name,
                l.name as language_name
            FROM Books b
            LEFT JOIN series s ON b.series_id = s.id
            LEFT JOIN language l ON b.language_id = l.id
            WHERE b.id = ?
            """
            
            cursor.execute(book_query, (book_id,))
            book_row = cursor.fetchone()
            
            if not book_row:
                logger.warning(f"Book with ID {book_id} not found")
                return None
            
            # Build book info dictionary with all fields
            book_info = {
                'id': book_row[0],
                'isbn': book_row[1],
                'title': book_row[2],
                'release_date': book_row[3],
                'first_polish_release_date': book_row[4],
                'format': book_row[5],
                'pages': book_row[6],
                'description': book_row[7],
                'note': book_row[8],
                'series_id': book_row[9],
                'original_title': book_row[10],
                'translator': book_row[11],
                'language_id': book_row[12],
                'size': book_row[13],
                'series_name': book_row[14],
                'language_name': book_row[15]
            }
            
            # Get authors with their names
            authors_query = """
            SELECT a.id, a.name, a.nationality_id, a.description, a.birth_date, a.death_date, a.note
            FROM Authors a
            JOIN bookAuthors ba ON a.id = ba.author_id
            WHERE ba.book_id = ?
            ORDER BY a.name
            """
            cursor.execute(authors_query, (book_id,))
            authors_rows = cursor.fetchall()
            
            authors_list = []
            authors_names = []
            for author_row in authors_rows:
                authors_list.append({
                    'id': author_row[0],
                    'name': author_row[1],
                    'nationality_id': author_row[2],
                    'description': author_row[3],
                    'birth_date': author_row[4],
                    'death_date': author_row[5],
                    'note': author_row[6]
                })
                authors_names.append(author_row[1])
            
            book_info['authors'] = ', '.join(authors_names) if authors_names else None
            book_info['authors_details'] = authors_list
            
            # Get publishers with their names
            publishers_query = """
            SELECT p.id, p.name, p.description, p.note, p.webpage
            FROM publisher p
            JOIN bookPublishers bp ON p.id = bp.publisher_id
            WHERE bp.book_id = ?
            ORDER BY p.name
            """
            cursor.execute(publishers_query, (book_id,))
            publishers_rows = cursor.fetchall()
            
            publishers_list = []
            publishers_names = []
            for publisher_row in publishers_rows:
                publishers_list.append({
                    'id': publisher_row[0],
                    'name': publisher_row[1],
                    'description': publisher_row[2],
                    'note': publisher_row[3],
                    'webpage': publisher_row[4]
                })
                publishers_names.append(publisher_row[1])
            
            book_info['publishers'] = ', '.join(publishers_names) if publishers_names else None
            book_info['publishers_details'] = publishers_list
            
            # Get labels with their names
            labels_query = """
            SELECT l.id, l.name
            FROM labels l
            JOIN bookLabel bl ON l.id = bl.label_id
            WHERE bl.book_id = ?
            ORDER BY l.name
            """
            cursor.execute(labels_query, (book_id,))
            labels_rows = cursor.fetchall()
            
            labels_list = []
            labels_names = []
            for label_row in labels_rows:
                labels_list.append({
                    'id': label_row[0],
                    'name': label_row[1]
                })
                labels_names.append(label_row[1])
            
            book_info['labels'] = ', '.join(labels_names) if labels_names else None
            book_info['labels_details'] = labels_list
            
            # Get genres with their names
            genres_query = """
            SELECT g.id, g.name
            FROM genres g
            JOIN bookGenres bg ON g.id = bg.genre_id
            WHERE bg.book_id = ?
            ORDER BY g.name
            """
            cursor.execute(genres_query, (book_id,))
            genres_rows = cursor.fetchall()
            
            genres_list = []
            genres_names = []
            for genre_row in genres_rows:
                genres_list.append({
                    'id': genre_row[0],
                    'name': genre_row[1]
                })
                genres_names.append(genre_row[1])
            
            book_info['genres'] = ', '.join(genres_names) if genres_names else None
            book_info['genres_details'] = genres_list
            
            logger.info(f"Successfully retrieved book info for ID {book_id}")
            return book_info
            
        except mariadb.Error as e:
            logger.error(f"Database error getting book info for ID {book_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting book info for ID {book_id}: {e}")
            raise
        finally:
            cursor.close()

    def update_book_info(self, book_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update book information in the database.

        Args:
            book_id: Unique identifier of the book
            updates: Dictionary containing fields to update

        Returns:
            Boolean indicating success/failure
        """
        try:
            current_info = self.get_book_info(int(book_id))
            if not current_info:
                logger.error(f"Book {book_id} not found")
                return False

            # TODO: Implement update logic based on your requirements
            logger.info(f"Book info update requested for ID {book_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating book info for {book_id}: {str(e)}")
            return False

    def update_metadata(self, book_id: str, metadata: Dict[str, Any]) -> bool:
        """Update book metadata fields."""
        return self.update_book_info(book_id, {'metadata': metadata})

    def update_status(self, book_id: str, status: str) -> bool:
        """Update book status."""
        return self.update_book_info(book_id, {'status': status})

    def update_tags(self, book_id: str, tags: list) -> bool:
        """Update book tags."""
        return self.update_book_info(book_id, {'tags': tags})