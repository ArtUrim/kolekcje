from flask import Flask, request, jsonify, Response
import mariadb
from typing import Optional, Dict, Any
import sys
import logging
import json

app = Flask(__name__)
app.url_map.strict_slashes = False

# Database configuration
DB_CONFIG = {
        "user": "example",
        "password": "example",
        "host": "db",
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

def sortPagination_query(params: Dict[str, Any]) -> tuple[str, list]:
    """
    Builds a sort and limit part of dynamic SQL query based on provided parameters
    Returns tuple of (query_string, parameters_list)
    """

    conditions = []
    parameters = []

    if params.get('sortBy'):
        order = 'ASC'
        if params.get('orderDesc') and params['orderDesc'] == 'desc':
            order = 'DESC'
        otype = None
        if params['sortBy'] == 'title':
            otype = 'b.title'
        elif params['sortBy'] == 'author':
            otype = 'authors'
        elif params['sortBy'] == 'publisher':
            otype = 'p.name'
        elif params['sortBy'] == 'release':
            otype = 'b.release_date'
        elif params['sortBy'] == 'serie':
            otype = 's.name'

        if otype:
            conditions.append( f"ORDER BY {otype} {order}" )

    if params.get('itemsPerPage'):
        itemsPP = int(params.get('itemsPerPage'))
        page = 1
        if params.get('page'):
            page = int(params['page'])
        offset = itemsPP*(page-1)
        conditions.append( "LIMIT ? OFFSET ?" )
        parameters.extend( [itemsPP, offset] )

    return (conditions,parameters)
        

def build_query(params: Dict[str, Any]) -> tuple[str, list]:
    """
    Builds a dynamic SQL query based on provided parameters
    Returns tuple of (query_string, parameters_list)
    """
    base_query = """
        SELECT SQL_CALC_FOUND_ROWS DISTINCT
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

    (c,p) = sortPagination_query( params )
    if c:
        base_query += "\n" + "\n".join(c)
    if p:
        parameters.extend(p)

    return base_query, parameters

@app.route('/book', methods=['GET'])
def get_books():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Get query parameters
        params = { k: request.args.get(k) for k in request.args.keys() }

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

        cur.execute( "SELECT FOUND_ROWS()" )
        count = cur.fetchall()[0][0] #@ TODO: error check!

        return jsonify({
            "status": "success",
            "count": count,
            "books": results
        })

    except mariadb.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    finally:
        if conn:
            conn.close()

@app.route('/addbook', methods=['POST'])
def add_books():
    print("ok" )
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        import ipdb; ipdb.set_trace()
        # Process JSON data
        data = request.get_json()
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=3)
        if data.get('title'):
            print("ok")
        # ... your logic here ...
        return jsonify({'message': 'Data received successfully'})
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415
    return Response( status = 204 )

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
