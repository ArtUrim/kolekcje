from typing import List, Dict
import mariadb

class TableHandler:
    def __init__(self, table_name: str, name_field: str = 'name'):
        self.table_name = table_name
        self.name_field = name_field

    def get_items(self, conn, query: str = '') -> List[Dict[str, str]]:
        try:
            cur = conn.cursor()

            if query:
                sql = f"SELECT {self.name_field} as title, {self.name_field} as value FROM {self.table_name} WHERE LOWER({self.name_field}) LIKE ?"
                cur.execute(sql, [f'%{query.lower()}%'])
            else:
                sql = f"SELECT {self.name_field} as title, {self.name_field} as value FROM {self.table_name}"
                cur.execute(sql)

            items = []
            for row in cur:
                items.append({
                    "title": row[0],
                    "value": row[1]
                })
            return items

        except mariadb.Error as e:
            raise Exception(f"Database error: {str(e)}")

    def add_item(self, conn, data: Dict[str, str]) -> None:
        try:
            if not all(key in data for key in ['value', 'title']):
                raise ValueError('Missing required fields')

            cur = conn.cursor()

            # Check if item already exists
            cur.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE {self.name_field} = ?", [data['value']])
            if cur.fetchone()[0] > 0:
                raise ValueError(f'Item with name {data["value"]} already exists')

            # Insert new item
            cur.execute(f"INSERT INTO {self.table_name} ({self.name_field}) VALUES (?)", [data['value']])
            conn.commit()

        except mariadb.Error as e:
            raise Exception(f"Database error: {str(e)}")
