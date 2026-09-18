from typing import List, Dict
import mariadb

class CatalogRepository:
    def __init__(self, connection, table_name: str, name_field: str = 'name'):
        self.connection = connection
        self.table_name = table_name
        self.name_field = name_field

    def list_items(self, query: str = '') -> List[Dict[str, str]]:
        try:
            cur = self.connection.cursor()

            if query:
                sql = f"SELECT {self.name_field} as title, id FROM {self.table_name} WHERE LOWER({self.name_field}) LIKE ?"
                cur.execute(sql, [f'%{query.lower()}%'])
            else:
                sql = f"SELECT {self.name_field} as title, id  FROM {self.table_name}"
                cur.execute(sql)

            items = []
            for row in cur:
                items.append({
                    "title": row[0],
                    "value": row[0],
                    "id": row[1]
                })
            return items

        except mariadb.Error as e:
            raise Exception(f"Database error: {str(e)}")

    def get_stats(self, relation_table: str, relation_fk: str, book_id_field: str) -> List[Dict]:
        try:
            cur = self.connection.cursor()
            sql = (
                f"SELECT t.{self.name_field} as value, t.id, COUNT(r.{book_id_field}) as count "
                f"FROM {self.table_name} t "
                f"LEFT JOIN {relation_table} r ON r.{relation_fk} = t.id "
                f"GROUP BY t.id, t.{self.name_field} "
                f"ORDER BY count DESC, t.{self.name_field} ASC"
            )
            cur.execute(sql)

            return [{"id": row[1], "value": row[0], "count": row[2]} for row in cur]

        except mariadb.Error as e:
            raise Exception(f"Database error: {str(e)}")

    def get_books_by_item(
        self, item_id: int, relation_table: str, relation_fk: str, book_id_field: str
    ) -> List[Dict]:
        try:
            cur = self.connection.cursor()
            sql = (
                "SELECT b.id, b.title FROM Books b "
                f"JOIN {relation_table} r ON r.{book_id_field} = b.id "
                f"WHERE r.{relation_fk} = ?"
            )
            cur.execute(sql, [item_id])

            return [{"id": row[0], "title": row[1]} for row in cur]

        except mariadb.Error as e:
            raise Exception(f"Database error: {str(e)}")

    def add_item(self, data: Dict[str, str]) -> None:
        try:
            if not all(key in data for key in ['value', 'title']):
                raise ValueError('Missing required fields')

            cur = self.connection.cursor()

            # Check if item already exists
            cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE {self.name_field} = ?", [data['value']])
            if cur.fetchone()[0] > 0:
                raise ValueError(f'Item with name {data["value"]} already exists')

            # Insert new item
            cur.execute(f"INSERT INTO {self.table_name} ({self.name_field}) VALUES (?)", [data['value']])
            self.connection.commit()

        except mariadb.Error as e:
            raise Exception(f"Database error: {str(e)}")
