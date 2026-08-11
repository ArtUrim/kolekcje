import pytest
from book_query_builder import BookQueryBuilder

class TestBookQueryBuilder:

    # --- Tests for _get_selected_fields ---

    def test_get_selected_fields_default(self):
        builder = BookQueryBuilder({})
        fields = builder._get_selected_fields()
        assert fields == ['id', 'title', 'author', 'publisher', 'release_date', 'series_name']

    def test_get_selected_fields_custom_valid(self):
        builder = BookQueryBuilder({'fields': 'id, isbn, title'})
        fields = builder._get_selected_fields()
        assert fields == ['id', 'isbn', 'title']

    def test_get_selected_fields_fallback_on_invalid(self):
        builder = BookQueryBuilder({'fields': 'invalid_field, another_bad_one'})
        fields = builder._get_selected_fields()
        # Should fallback to defaults if no valid fields are found
        assert fields == ['id', 'title', 'author', 'publisher', 'release_date', 'series_name']

    def test_get_selected_fields_mixed_valid_invalid(self):
        builder = BookQueryBuilder({'fields': 'id, invalid_field, title'})
        fields = builder._get_selected_fields()
        # Should extract only the valid ones
        assert fields == ['id', 'title']

    # --- Tests for _build_select_clause ---

    def test_build_select_clause(self):
        builder = BookQueryBuilder({})
        select_sql = builder._build_select_clause(['id', 'title', 'author'])
        
        assert "SELECT SQL_CALC_FOUND_ROWS DISTINCT" in select_sql
        assert "b.id" in select_sql
        assert "b.title" in select_sql
        assert "GROUP_CONCAT(DISTINCT a.name SEPARATOR \", \") as author" in select_sql

    # --- Tests for _build_from_and_joins ---

    def test_build_from_and_joins_triggered_by_fields(self):
        builder = BookQueryBuilder({})
        joins_sql = builder._build_from_and_joins(['genres', 'labels'])
        
        assert "FROM Books b" in joins_sql
        assert "LEFT JOIN bookGenres bg ON b.id = bg.book_id" in joins_sql
        assert "LEFT JOIN genres g ON bg.genre_id = g.id" in joins_sql
        assert "LEFT JOIN bookLabel bl ON b.id = bl.book_id" in joins_sql

    def test_build_from_and_joins_triggered_by_params(self):
        # Even if 'author' is not in fields, filtering by author should trigger the join
        builder = BookQueryBuilder({'author': 'Tolkien'})
        joins_sql = builder._build_from_and_joins(['id', 'title'])
        
        assert "LEFT JOIN bookAuthors ba" in joins_sql

    # --- Tests for _build_where_clause ---

    def test_build_where_clause_empty(self):
        builder = BookQueryBuilder({})
        conditions, parameters = builder._build_where_clause()
        
        assert len(conditions) == 0
        assert len(parameters) == 0

    def test_build_where_clause_with_filters(self):
        params = {
            'title': 'Hobbit',
            'isbn': '978',
            'release_date': '2023'
        }
        builder = BookQueryBuilder(params)
        conditions, parameters = builder._build_where_clause()
        
        assert len(conditions) == 3
        assert "b.title LIKE ?" in conditions
        assert "b.isbn LIKE ?" in conditions
        assert "b.release_date LIKE ?" in conditions
        assert "%Hobbit%" in parameters
        assert "%978%" in parameters
        assert "%2023%" in parameters

    def test_build_where_clause_complex_exists(self):
        builder = BookQueryBuilder({'author': 'Tolkien'})
        conditions, parameters = builder._build_where_clause()
        
        assert len(conditions) == 1
        assert "EXISTS" in conditions[0]
        assert "bookAuthors" in conditions[0]
        assert "%Tolkien%" in parameters

    # --- Tests for _build_group_by ---

    def test_build_group_by(self):
        builder = BookQueryBuilder({})
        fields = ['id', 'title', 'series_name', 'author', 'language']
        group_by_sql = builder._build_group_by(fields)
        
        # 'author' should be excluded from GROUP BY
        assert "GROUP BY" in group_by_sql
        assert "b.id" in group_by_sql
        assert "b.title" in group_by_sql
        assert "s.name" in group_by_sql
        assert "lang.name" in group_by_sql
        assert "author" not in group_by_sql

    # --- Tests for _build_sort_pagination ---

    def test_build_sort_pagination_empty(self):
        builder = BookQueryBuilder({})
        conditions, parameters = builder._build_sort_pagination()
        
        assert len(conditions) == 0
        assert len(parameters) == 0

    def test_build_sort_pagination_sorting_only(self):
        builder = BookQueryBuilder({'sortBy': 'title', 'sortDesc': 'desc'})
        conditions, parameters = builder._build_sort_pagination()
        
        assert len(conditions) == 1
        assert "ORDER BY b.title DESC" in conditions[0]
        assert len(parameters) == 0

    def test_build_sort_pagination_pagination_only(self):
        # 10 items per page, page 3 -> offset should be 20
        builder = BookQueryBuilder({'itemsPerPage': '10', 'page': '3'})
        conditions, parameters = builder._build_sort_pagination()
        
        assert len(conditions) == 1
        assert "LIMIT ? OFFSET ?" in conditions[0]
        assert parameters == [10, 20]

    def test_build_sort_pagination_combined(self):
        builder = BookQueryBuilder({
            'sortBy': 'release', 
            'orderDesc': 'desc', # Testing alternative desc param
            'itemsPerPage': '5', 
            'page': '1'
        })
        conditions, parameters = builder._build_sort_pagination()
        
        assert len(conditions) == 2
        assert "ORDER BY b.release_date DESC" in conditions[0]
        assert "LIMIT ? OFFSET ?" in conditions[1]
        assert parameters == [5, 0]

    # --- Tests for build() Orchestration ---

    def test_build_full_orchestration(self):
        params = {
            'fields': 'id, title, author',
            'title': 'Dune',
            'sortBy': 'title',
            'itemsPerPage': '10'
        }
        builder = BookQueryBuilder(params)
        query, parameters, fields = builder.build()

        # Check Fields Return
        assert fields == ['id', 'title', 'author']

        # Check Query Structure
        assert query.startswith("SELECT SQL_CALC_FOUND_ROWS DISTINCT b.id, b.title, GROUP_CONCAT")
        assert "FROM Books b" in query
        assert "LEFT JOIN bookAuthors" in query
        assert "WHERE b.title LIKE ?" in query
        assert "GROUP BY b.id, b.title" in query
        assert "ORDER BY b.title ASC" in query
        assert "LIMIT ? OFFSET ?" in query

        # Check Parameters bindings
        assert "%Dune%" in parameters
        assert 10 in parameters # Limit
        assert 0 in parameters  # Offset (Page 1 default)