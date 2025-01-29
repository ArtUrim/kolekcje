from flask import Flask, request, jsonify, Response
import mariadb
from typing import Optional, Dict, Any
import sys
import logging
import json
from typing import List, Dict

from addBook import BookDatabase

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
        try:
            # Process JSON data
            data = request.get_json()
            with open('data.json', 'w') as f: # temporary: for debug
                json.dump(data, f, indent=3)
            if data.get('title'): 
                logging.info(f"Receive new book, title: {data['title']}")
            conn = get_db_connection()
            if conn:
                db = BookDatabase( conn )
                db.insert_book( data )
                conn.close()
            else:
                logging.warn( f"Connection to DB not successful" )
        except Exception as e:
            logging.warn(f"Error processing addbook POST request: {e}")
            if data and data.get('title'):
                logging.warn( f"for the book {data['title']}")
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415
    return Response( status = 204 )

# In-memory storage for publishers (in a real app, this would be a database)
publishers: List[Dict[str, any]] = [
    {"title": "Penguin Random House", "value": "Penguin Random House"},
    {"title": "HarperCollins", "value": "HarperCollins"},
    {"title": "Simon & Schuster", "value": "Simon & Schuster"}
]

@app.route('/api/publishers', methods=['GET'])
def get_publishers():
    query = request.args.get('query', '').lower()

    if query:
        filtered_publishers = [
            publisher for publisher in publishers
            if query in publisher['title'].lower()
        ]
        return jsonify(filtered_publishers)

    return jsonify(publishers)

@app.route('/api/publisher/add', methods=['POST'])
def add_publisher():
    try:
        data = request.get_json()

        # Validate required fields
        if not all(key in data for key in ['value', 'title']):
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate data types
        if not isinstance(data['value'], str):
            return jsonify({'error': 'Value must be a string'}), 400
        if not isinstance(data['title'], str):
            return jsonify({'error': 'Title must be a string'}), 400

        # Check if publisher with same ID already exists
        if any(p['value'] == data['value'] for p in publishers):
            return jsonify({'error': 'Publisher with this title already exists'}), 409

        publishers.append( data )

        return jsonify({'message': 'Publisher added successfully'}), 201

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
