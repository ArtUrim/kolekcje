from typing import Any, Dict, List, Tuple

from .book_query_builder import BookQueryBuilder


class BookQueryRepository:
    def __init__(self, connection):
        self.connection = connection

    def search(self, params) -> Tuple[List[Dict[str, Any]], int]:
        book_query_builder = BookQueryBuilder(params)
        query, parameters, columns = book_query_builder.build()
        cur = self.connection.cursor()
        cur.execute(query, parameters)
        books = []
        for row in cur:
            book_dict = {}
            for i, column in enumerate(columns):
                book_dict[column] = row[i]
            books.append(book_dict)
        cur.execute("SELECT FOUND_ROWS()")
        count = cur.fetchall()[0][0] #@ TODO: error check!
        return books, count
