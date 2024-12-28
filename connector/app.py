from flask import Flask, request, jsonify
import mariadb
from typing import Optional, Dict, Any
import sys

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
        "user": "example",
        "password": "example",
        "host": "kolekcje-db-1",
        "port": 3306,
        "database": "katalog"
}

def get_db_connection():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

def build_query(params: Dict[str, Any]) -> tuple[str, list]:
    """
    Builds a dynamic SQL query based on provided parameters
    Returns tuple of (query_string, parameters_list)
    """
    base_query = """
        SELECT DISTINCT
            b.title,
            GROUP_CONCAT(DISTINCT a.name) as authors,
            p.name as publisher,
            b.release_date,
            s.name as series_name
        FROM Books b
        LEFT JOIN bookAuthors ba ON b.id = ba.book_id
        LEFT JOIN Authors a ON ba.author_id = a.id
        LEFT JOIN publisher p ON b.publisher_id = p.id
        LEFT JOIN series s ON b.series_id = s.id
    """

    conditions = []
    parameters = []

    if params.get('author'):
        conditions.append("a.name LIKE ?")
        parameters.append(f"%{params['author']}%")

    if params.get('title'):
        conditions.append("b.title LIKE ?")
        parameters.append(f"%{params['title']}%")

    if params.get('publisher'):
        conditions.append("p.name LIKE ?")
        parameters.append(f"%{params['publisher']}%")

    if params.get('serie'):
        conditions.append("s.name LIKE ?")
        parameters.append(f"%{params['serie']}%")

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    base_query += " GROUP BY b.id, b.title, p.name, b.release_date, s.name"

    return base_query, parameters

@app.route('/book', methods=['GET'])
def get_books():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Get query parameters
        params = {
            'author': request.args.get('author'),
            'title': request.args.get('title'),
            'publisher': request.args.get('publisher'),
            'serie': request.args.get('serie')
        }

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        if not params:
            return jsonify({"error": "No search parameters provided"}), 400

        query, parameters = build_query(params)

        cur = conn.cursor()
        cur.execute(query, parameters)

        # Fetch results
        columns = ['title', 'authors', 'publisher', 'release_date', 'series_name']
        results = []

        for row in cur:
            book_dict = {}
            for i, column in enumerate(columns):
                book_dict[column] = row[i]
            results.append(book_dict)

        return jsonify({
            "status": "success",
            "count": len(results),
            "books": results
        })

    except mariadb.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    finally:
        if conn:
            conn.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
