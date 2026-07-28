import mariadb
from typing import Dict, Any, List, Optional, Tuple


class BookUpdateDatabase:
    def __init__(self, connection: mariadb.connections.Connection):
        self.connection = connection

    def _safe_int_conversion(self, value: Any, field_name: str) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return None
            try:
                return int(raw)
            except ValueError:
                raise ValueError(f"Invalid integer value for {field_name}: {value}")
        raise ValueError(f"Cannot convert {type(value)} to integer for {field_name}")

    def _extract_year(self, value: Any, field_name: str) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return None
            try:
                return int(raw[:4])
            except ValueError:
                raise ValueError(f"Invalid year value for {field_name}: {value}")
        raise ValueError(f"Invalid year value for {field_name}: {value}")

    def _normalize_format(self, value: Any) -> str:
        if value is None:
            return "unknown"
        mapped = {
            "papier": "paperback",
            "paperback": "paperback",
            "hardcover": "hardback",
            "hardback": "hardback",
            "ebook": "ebook",
            "e-book": "ebook",
            "unknown": "unknown",
            'notebook': 'notebook',
            'jacket': 'jacket'

        }
        normalized = str(value).strip().lower()
        if not normalized:
            return "unknown"
        if normalized in mapped:
            return mapped[normalized]
        raise ValueError(f"Invalid format value: {value}")

    def _normalize_size(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        normalized = str(value).strip().lower()
        if not normalized:
            return None
        allowed = {"none", "mini", "normal", "scientific", "comics", "huge", "small", "unusual"}
        if normalized not in allowed:
            raise ValueError(f"Invalid size value: {value}")
        return normalized

    def _normalize_language(self, value: Any) -> str:
        if value is None:
            return "pl_"
        normalized = str(value).strip()
        if not normalized:
            return "pl_"
        if len(normalized) == 2:
            normalized = f"{normalized}_"
        if len(normalized) != 3:
            raise ValueError(f"Invalid language code: {value}")
        return normalized

    def _ensure_row_exists(self, table: str, row_id: int) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT 1 FROM {table} WHERE id = ?", (row_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def _language_exists(self, language_id: str) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT 1 FROM language WHERE id = ?", (language_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def _get_or_create_named(self, table: str, name: str, create_sql: Optional[Tuple[str, tuple]] = None) -> int:
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return row[0]
            if create_sql is None:
                cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
            else:
                query, params = create_sql
                cursor.execute(query, params)
            return cursor.lastrowid
        finally:
            cursor.close()

    def _normalize_relation_items(self, value: Any) -> List[Any]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def _resolve_entity_id(self, item: Any, table: str, allow_create: bool = True) -> int:
        if isinstance(item, int):
            if not self._ensure_row_exists(table, item):
                raise ValueError(f"Referenced {table} id not found: {item}")
            return item

        if isinstance(item, str):
            name = item.strip()
            if not name:
                raise ValueError(f"Invalid empty value for {table}")
            if not allow_create:
                raise ValueError(f"Name lookup not allowed for {table}")
            if table == "Authors":
                return self._get_or_create_named(table, name, ("INSERT INTO Authors (name, nationality_id) VALUES (?, ?)", (name, "pl_")))
            return self._get_or_create_named(table, name)

        if isinstance(item, dict):
            raw_id = item.get("id")
            is_custom = item.get("isCustom", True)
            if raw_id is not None and is_custom is False:
                entity_id = self._safe_int_conversion(raw_id, f"{table}.id")
                if entity_id is None or not self._ensure_row_exists(table, entity_id):
                    raise ValueError(f"Referenced {table} id not found: {raw_id}")
                return entity_id

            name = item.get("title") or item.get("name")
            if name is None:
                raise ValueError(f"Missing name/title for {table}")
            normalized_name = str(name).strip()
            if not normalized_name:
                raise ValueError(f"Invalid empty name for {table}")
            if not allow_create:
                raise ValueError(f"Name lookup not allowed for {table}")
            if table == "Authors":
                return self._get_or_create_named(table, normalized_name, ("INSERT INTO Authors (name, nationality_id) VALUES (?, ?)", (normalized_name, "pl_")))
            return self._get_or_create_named(table, normalized_name)

        raise ValueError(f"Invalid value format for {table}")

    def _replace_relations(self, book_id: int, table: str, entity_column: str, entity_ids: List[int]) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {table} WHERE book_id = ?", (book_id,))
            seen = set()
            for entity_id in entity_ids:
                if entity_id in seen:
                    continue
                seen.add(entity_id)
                cursor.execute(
                    f"INSERT INTO {table} (book_id, {entity_column}) VALUES (?, ?)",
                    (book_id, entity_id)
                )
        finally:
            cursor.close()

    def _get_value(self, payload: Dict[str, Any], *keys: str) -> Tuple[bool, Any]:
        for key in keys:
            if key in payload:
                return True, payload[key]
        return False, None

    def delete_book(self, book_id: int) -> Dict[str, Any]:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT 1 FROM Books WHERE id = ?", (book_id,))
            if cursor.fetchone() is None:
                return {"not_found": True}

            cursor.execute("DELETE FROM bookAuthors WHERE book_id = ?", (book_id,))
            cursor.execute("DELETE FROM bookPublishers WHERE book_id = ?", (book_id,))
            cursor.execute("DELETE FROM bookGenres WHERE book_id = ?", (book_id,))
            cursor.execute("DELETE FROM bookLabel WHERE book_id = ?", (book_id,))
            cursor.execute("DELETE FROM Books WHERE id = ?", (book_id,))

            self.connection.commit()
            return {"deleted": True, "book_id": book_id}
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def update_book(self, book_id: int, book_data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(book_data, dict):
            raise ValueError("JSON payload must be an object")

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT 1 FROM Books WHERE id = ?", (book_id,))
            if cursor.fetchone() is None:
                return {"not_found": True}

            updates: List[str] = []
            params: List[Any] = []

            has_title, title = self._get_value(book_data, "title")
            if has_title:
                if title is None or not str(title).strip():
                    raise ValueError("Title cannot be empty")
                updates.append("title = ?")
                params.append(str(title).strip())

            has_original_title, original_title = self._get_value(book_data, "originalTitle", "original_title")
            if has_original_title:
                normalized_original_title = None if original_title is None or not str(original_title).strip() else str(original_title).strip()
                updates.append("original_title = ?")
                params.append(normalized_original_title)

            has_release_date, release_date = self._get_value(book_data, "publishYear", "release_date")
            if has_release_date:
                updates.append("release_date = ?")
                params.append(self._extract_year(release_date, "release_date"))

            has_first_polish_date, first_polish_date = self._get_value(book_data, "firstPublishYear", "first_polish_release_date")
            if has_first_polish_date:
                updates.append("first_polish_release_date = ?")
                params.append(self._extract_year(first_polish_date, "first_polish_release_date"))

            has_format, format_value = self._get_value(book_data, "format")
            if has_format:
                updates.append("format = ?")
                params.append(self._normalize_format(format_value))

            has_note, note = self._get_value(book_data, "notes", "note")
            if has_note:
                normalized_note = None if note is None else str(note)
                updates.append("note = ?")
                params.append(normalized_note)

            has_pages, pages = self._get_value(book_data, "pages")
            if has_pages:
                updates.append("pages = ?")
                params.append(self._safe_int_conversion(pages, "pages"))

            has_description, description = self._get_value(book_data, "description")
            if has_description:
                normalized_description = None if description is None else str(description)
                updates.append("description = ?")
                params.append(normalized_description)

            has_translator, translator = self._get_value(book_data, "translator")
            if has_translator:
                normalized_translator = None if translator is None or not str(translator).strip() else str(translator).strip()
                updates.append("translator = ?")
                params.append(normalized_translator)

            has_isbn, isbn = self._get_value(book_data, "isbn")
            if has_isbn:
                normalized_isbn = None if isbn is None or not str(isbn).strip() else str(isbn).strip()
                updates.append("isbn = ?")
                params.append(normalized_isbn)

            has_size, size = self._get_value(book_data, "size")
            if has_size:
                updates.append("size = ?")
                params.append(self._normalize_size(size))

            has_language, language = self._get_value(book_data, "language", "language_id")
            if has_language:
                language_id = self._normalize_language(language)
                if not self._language_exists(language_id):
                    raise ValueError(f"Language not found: {language_id}")
                updates.append("language_id = ?")
                params.append(language_id)

            has_series, series_value = self._get_value(book_data, "series", "series_id")
            if has_series:
                series_id = None
                if isinstance(series_value, int):
                    series_id = series_value
                    if not self._ensure_row_exists("series", series_id):
                        raise ValueError(f"Series not found: {series_id}")
                elif isinstance(series_value, str):
                    normalized_series = series_value.strip()
                    series_id = self._get_or_create_named("series", normalized_series) if normalized_series else None
                elif isinstance(series_value, dict):
                    series_id = self._resolve_entity_id(series_value, "series", allow_create=True)
                elif series_value is None:
                    series_id = None
                else:
                    raise ValueError("Invalid series value")
                updates.append("series_id = ?")
                params.append(series_id)

            if updates:
                query = f"UPDATE Books SET {', '.join(updates)} WHERE id = ?"
                params.append(book_id)
                cursor.execute(query, tuple(params))

            has_authors, authors_value = self._get_value(book_data, "author", "authors")
            if has_authors:
                author_ids = [self._resolve_entity_id(item, "Authors", allow_create=True) for item in self._normalize_relation_items(authors_value)]
                self._replace_relations(book_id, "bookAuthors", "author_id", author_ids)

            has_publishers, publishers_value = self._get_value(book_data, "publisher", "publishers")
            if has_publishers:
                publisher_ids = [self._resolve_entity_id(item, "publisher", allow_create=True) for item in self._normalize_relation_items(publishers_value)]
                self._replace_relations(book_id, "bookPublishers", "publisher_id", publisher_ids)

            has_genres, genres_value = self._get_value(book_data, "genre", "genres")
            if has_genres:
                genre_ids = [self._resolve_entity_id(item, "genres", allow_create=True) for item in self._normalize_relation_items(genres_value)]
                self._replace_relations(book_id, "bookGenres", "genre_id", genre_ids)

            has_labels, labels_value = self._get_value(book_data, "label", "labels")
            if has_labels:
                label_ids = [self._resolve_entity_id(item, "labels", allow_create=True) for item in self._normalize_relation_items(labels_value)]
                self._replace_relations(book_id, "bookLabel", "label_id", label_ids)

            self.connection.commit()
            return {"updated": True, "book_id": book_id}
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()
