import json
import logging

from ..repositories.book_query_repository import BookQueryRepository
from ..repositories.book_repository import BookRepository
from ..repositories.book_update_repository import BookUpdateRepository


class BookService:
    def __init__(self, connection):
        self.connection = connection

    def add_book(self, book_data):
        with open('data.json', 'w') as f: # temporary: for debug
            json.dump(book_data, f, indent=3)
        if book_data.get('title'):
            logging.info(f"Receive new book, title: {book_data['title']}")
            print(f"Receive new book, title: {book_data['title']}")
        if self.connection is None:
            logging.warning(f"Connection to DB not successful")
            return None
        return BookRepository(self.connection).insert_book_from_dict(book_data)

    def search_books(self, params):
        return BookQueryRepository(self.connection).search(params)

    def update_book(self, book_id, book_data):
        return BookUpdateRepository(self.connection).update_book(book_id, book_data)

    def delete_book(self, book_id):
        return BookUpdateRepository(self.connection).delete_book(book_id)
