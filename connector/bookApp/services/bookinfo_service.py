from ..core.isbn import normalize_isbn, validate_isbn
from ..repositories.bookinfo_repository import BookInfoRepository


class BookInfoService:
    def __init__(self, connection):
        self.connection = connection

    def get_book_info(self, book_id):
        return BookInfoRepository(self.connection).get_book_info(book_id)

    def update_book_info(self, book_id, updates):
        return BookInfoRepository(self.connection).update_book_info(book_id, updates)

    def find_matches(self, search_params):
        return BookInfoRepository(self.connection).get_basic_book_info(search_params)


def isbn_validation_error(isbn_value):
    isbn_norm = normalize_isbn(isbn_value)
    isbn_valid = validate_isbn(isbn_norm) if isbn_norm else None
    if isbn_valid is not True:
        result = {"title": "Invalid ISBN"}
        if not isbn_norm:
            result['detail'] = f"Provided ISBN {isbn_value} cannot be normalized"
        else:
            result['detail'] = f"Provided ISBN {isbn_value} has no valid checksum"
        return result
    return None
