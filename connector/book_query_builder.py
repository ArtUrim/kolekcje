from typing import Dict, Any, Tuple, List

class BookQueryBuilder:
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.valid_fields = {
            'id': 'b.id',
            'isbn': 'b.isbn',
            'title': 'b.title',
            'release_date': 'b.release_date',
            'first_polish_release_date': 'b.first_polish_release_date',
            'format': 'b.format',
            'pages': 'b.pages',
            'description': 'b.description',
            'note': 'b.note',
            'original_title': 'b.original_title',
            'translator': 'b.translator',
            'language_id': 'b.language_id',
            'language': 'lang.name as language',
            'size': 'b.size',
            'author': 'GROUP_CONCAT(DISTINCT a.name SEPARATOR ", ") as author',
            'publisher': 'GROUP_CONCAT(DISTINCT p.name SEPARATOR ", ") as publisher',
            'series_name': 's.name as series_name',
            'genres': 'GROUP_CONCAT(DISTINCT g.name SEPARATOR ", ") as genres',
            'labels': 'GROUP_CONCAT(DISTINCT l.name SEPARATOR ", ") as labels'
        }

    def _get_selected_fields(self) -> List[str]:
        """Parses and validates the requested fields."""
        requested_fields_str = self.params.get('fields')
        if requested_fields_str:
            fields = [f.strip() for f in requested_fields_str.split(',') if f.strip() in self.valid_fields]
            if fields:
                return fields
        return ['id', 'title', 'author', 'publisher', 'release_date', 'series_name']

    def _build_select_clause(self, fields: List[str]) -> str:
        """Builds the SELECT portion of the query."""
        return "SELECT SQL_CALC_FOUND_ROWS DISTINCT " + ", ".join([self.valid_fields[f] for f in fields])

    def _build_from_and_joins(self, fields: List[str]) -> str:
        """Builds the FROM and JOIN portions dynamically."""
        from_clause = " FROM Books b"
        joins = []

        if 'author' in fields or self.params.get('author'):
            joins.extend(["LEFT JOIN bookAuthors ba ON b.id = ba.book_id",
                          "LEFT JOIN Authors a ON ba.author_id = a.id"])

        if 'publisher' in fields or self.params.get('publisher'):
            joins.extend(["LEFT JOIN bookPublishers bp ON b.id = bp.book_id",
                          "LEFT JOIN publisher p ON bp.publisher_id = p.id"])

        if 'series_name' in fields or self.params.get('serie'):
            joins.append("LEFT JOIN series s ON b.series_id = s.id")

        if 'genres' in fields or self.params.get('genres'):
            joins.extend(["LEFT JOIN bookGenres bg ON b.id = bg.book_id",
                          "LEFT JOIN genres g ON bg.genre_id = g.id"])

        if 'labels' in fields or self.params.get('label'):
            joins.extend(["LEFT JOIN bookLabel bl ON b.id = bl.book_id",
                          "LEFT JOIN labels l ON bl.label_id = l.id"])

        if 'language' in fields:
            joins.append("LEFT JOIN language lang ON b.language_id = lang.id")

        # Preserve order while removing duplicates
        unique_joins = []
        for j in joins:
            if j not in unique_joins:
                unique_joins.append(j)

        return from_clause + "\n" + "\n".join(unique_joins)

    def _build_where_clause(self) -> Tuple[List[str], List[Any]]:
        """Builds the WHERE conditions and their corresponding parameters."""
        conditions = []
        parameters = []

        if self.params.get('author'):
            conditions.append("EXISTS ( SELECT 1 FROM bookAuthors ba2 JOIN Authors a2 ON ba2.author_id = a2.id WHERE ba2.book_id = b.id AND a2.name LIKE ? )")
            parameters.append(f"%{self.params['author']}%")

        if self.params.get('title'):
            conditions.append("b.title LIKE ?")
            parameters.append(f"%{self.params['title']}%")

        if self.params.get('publisher'):
            conditions.append("EXISTS ( SELECT 1 FROM bookPublishers bp2 JOIN publisher p2 ON bp2.publisher_id = p2.id WHERE bp2.book_id = b.id AND p2.name LIKE ? )")
            parameters.append(f"%{self.params['publisher']}%")

        if self.params.get('serie'):
            conditions.append("s.name LIKE ?")
            parameters.append(f"%{self.params['serie']}%")

        if self.params.get('isbn'):
            conditions.append("b.isbn LIKE ?")
            parameters.append(f"%{self.params['isbn']}%")

        if self.params.get('genres'):
            conditions.append("EXISTS ( SELECT 1 FROM bookGenres bg2 JOIN genres g2 ON bg2.genre_id = g2.id WHERE bg2.book_id = b.id AND g2.name LIKE ? )")
            parameters.append(f"%{self.params['genres']}%")

        if self.params.get('label'):
            conditions.append("EXISTS ( SELECT 1 FROM bookLabel bl2 JOIN labels l2 ON bl2.label_id = l2.id WHERE bl2.book_id = b.id AND l2.name LIKE ? )")
            parameters.append(f"%{self.params['label']}%")

        if self.params.get('release_date'):
            conditions.append("b.release_date LIKE ?")
            parameters.append(f"%{self.params['release_date']}%")

        if self.params.get('first_polish_release_date'):
            conditions.append("b.first_polish_release_date LIKE ?")
            parameters.append(f"%{self.params['first_polish_release_date']}%")

        if self.params.get('format'):
            conditions.append("b.format LIKE ?")
            parameters.append(f"%{self.params['format']}%")

        if self.params.get('original_title'):
            conditions.append("b.original_title LIKE ?")
            parameters.append(f"%{self.params['original_title']}%")

        if self.params.get('translator'):
            conditions.append("b.translator LIKE ?")
            parameters.append(f"%{self.params['translator']}%")

        if self.params.get('language'):
            conditions.append("lang.name LIKE ?")
            parameters.append(f"%{self.params['language']}%")

        return conditions, parameters

    def _build_group_by(self, fields: List[str]) -> str:
        """Builds the GROUP BY clause for non-aggregated fields."""
        group_by_fields = []
        for f in fields:
            if f not in ['author', 'genres', 'labels', 'publisher']:
                if f == 'series_name':
                    group_by_fields.append('s.name')
                elif f == 'language':
                    group_by_fields.append('lang.name')
                else:
                    group_by_fields.append(f'b.{f}')

        if group_by_fields:
            return "\nGROUP BY " + ", ".join(group_by_fields)
        return ""

    def _build_sort_pagination(self) -> Tuple[List[str], List[Any]]:
        """Builds the ORDER BY, LIMIT, and OFFSET clauses."""
        conditions = []
        parameters = []

        otype = 'b.id'
        order = 'ASC'

        sort_order = None
        if self.params.get('sortDesc'):
            sort_order = self.params.get('sortDesc')
        elif self.params.get('orderDesc'):
            sort_order = self.params.get('orderDesc')
        if sort_order and sort_order.lower() == 'desc':
            order = 'DESC'

        if self.params.get('sortBy'):

            sort_by = self.params['sortBy'].lower()
            if sort_by == 'title':
                otype = 'b.title'
            elif sort_by in ('author', 'authors'):
                otype = 'author'
            elif sort_by == 'publisher':
                otype = 'publisher'
            elif sort_by in ('release', 'release_date'):
                otype = 'b.release_date'
            elif sort_by in ('serie', 'series', 'series_name'):
                otype = 's.name'
            elif sort_by == 'format':
                otype = 'b.format'
            elif sort_by == 'pages':
                otype = 'b.pages'
            elif sort_by == 'first_polish_release_date':
                otype = 'b.first_polish_release_date'
            elif sort_by == 'translator':
                otype = 'b.translator'
            elif sort_by == 'original_title':
                otype = 'b.original_title'
            elif sort_by == 'size':
                otype = 'b.size'
            elif sort_by == 'language':
                otype = 'lang.name'

        conditions.append(f"ORDER BY {otype} {order}")

        if self.params.get('itemsPerPage'):
            items_pp = int(self.params.get('itemsPerPage'))
            if items_pp > 0:
                page = int(self.params.get('page', 1))
                offset = items_pp * (page - 1)

                conditions.append("LIMIT ? OFFSET ?")
                parameters.extend([items_pp, offset])

        return conditions, parameters

    def build(self) -> Tuple[str, List[Any], List[str]]:
        """
        Orchestrates the utility methods to build the final SQL query.
        Returns tuple of (query_string, parameters_list, selected_columns_list)
        """
        # 1. Determine Fields
        fields = self._get_selected_fields()

        # 2. Build Base Query (SELECT + FROM + JOINS)
        query = self._build_select_clause(fields)
        query += self._build_from_and_joins(fields)

        # 3. Add WHERE clause
        where_conditions, parameters = self._build_where_clause()
        if where_conditions:
            query += "\nWHERE " + " AND ".join(where_conditions)

        # 4. Add GROUP BY clause
        query += self._build_group_by(fields)

        # 5. Add Sorting and Pagination
        sort_conditions, sort_params = self._build_sort_pagination()
        if sort_conditions:
            query += "\n" + "\n".join(sort_conditions)
        if sort_params:
            parameters.extend(sort_params)

        return query, parameters, fields
