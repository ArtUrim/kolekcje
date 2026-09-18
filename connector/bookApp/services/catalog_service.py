from ..repositories.catalog_repository import CatalogRepository


class CatalogService:
    # Maps catalog table name to the (relation_table, relation_fk, book_id_field)
    # used to count/lookup books linked to a given entry. Labels and genres link
    # to books through junction tables; series and language link directly
    # through Books.series_id / Books.language_id, so their relation table is
    # Books itself and the book id column is Books.id.
    RELATION_TABLES = {
        'labels': ('bookLabel', 'label_id', 'book_id'),
        'genres': ('bookGenres', 'genre_id', 'book_id'),
        'series': ('Books', 'series_id', 'id'),
        'language': ('Books', 'language_id', 'id'),
    }

    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name

    def list_items(self, query=''):
        return CatalogRepository(self.connection, self.table_name).list_items(query)

    def add_item(self, data):
        CatalogRepository(self.connection, self.table_name).add_item(data)

    def get_stats(self):
        relation_table, relation_fk, book_id_field = self._relation_config()
        return CatalogRepository(self.connection, self.table_name).get_stats(
            relation_table, relation_fk, book_id_field
        )

    def get_books_for_item(self, item_id):
        relation_table, relation_fk, book_id_field = self._relation_config()
        return CatalogRepository(self.connection, self.table_name).get_books_by_item(
            item_id, relation_table, relation_fk, book_id_field
        )

    def _relation_config(self):
        if self.table_name not in self.RELATION_TABLES:
            raise ValueError(f"No relation table configured for '{self.table_name}'")
        return self.RELATION_TABLES[self.table_name]
