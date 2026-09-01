from ..repositories.catalog_repository import CatalogRepository


class CatalogService:
    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name

    def list_items(self, query=''):
        return CatalogRepository(self.connection, self.table_name).list_items(query)

    def add_item(self, data):
        CatalogRepository(self.connection, self.table_name).add_item(data)
