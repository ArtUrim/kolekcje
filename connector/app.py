from flask import Flask, request, jsonify, Response
import mariadb
from typing import Optional, Dict, Any
import sys
import logging
import json
from typing import List, Dict
import os
import uuid
from functools import wraps

from addBook import BookDatabase
from updateBook import BookUpdateDatabase
from bookinfo_handler import BookInfoHandler
from table_handler import TableHandler

# Create handlers after app initialization
publisher_handler = TableHandler('publisher')
author_handler = TableHandler('Authors')
series_handler = TableHandler('series')
genres_handler = TableHandler('genres')
labels_handler = TableHandler('labels')

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

SHARED_DIR = '/app/shared'

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
        sort_order = params.get('sortDesc') or params.get('orderDesc')
        if sort_order and sort_order.lower() == 'desc':
            order = 'DESC'

        sort_by = params['sortBy'].lower()
        otype = None
        if sort_by == 'title':
            otype = 'b.title'
        elif sort_by in ('author', 'authors'):
            otype = 'authors'
        elif sort_by == 'publisher':
            otype = 'p.name'
        elif sort_by in ('release', 'release_date'):
            otype = 'b.release_date'
        elif sort_by in ('serie', 'series', 'series_name'):
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


def build_query(params: Dict[str, Any]) -> tuple[str, list, list]:
    """
    Builds a dynamic SQL query based on provided parameters and requested fields.
    Returns tuple of (query_string, parameters_list, selected_columns_list)
    """
    # Define all allowable fields and their corresponding SQL mapping
    valid_fields = {
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
        'size': 'b.size',
        'authors': 'GROUP_CONCAT(DISTINCT a.name SEPARATOR ", ") as authors',
        'publisher': 'p.name as publisher',
        'series_name': 's.name as series_name',
        'genres': 'GROUP_CONCAT(DISTINCT g.name SEPARATOR ", ") as genres',
        'labels': 'GROUP_CONCAT(DISTINCT l.name SEPARATOR ", ") as labels'
    }

    # Determine which fields the client requested, defaulting to standard fields if none are provided
    requested_fields_str = params.get('fields')
    if requested_fields_str:
        fields = [f.strip() for f in requested_fields_str.split(',') if f.strip() in valid_fields]
        if not fields: # Fallback if they provided entirely invalid fields
            fields = ['id', 'title', 'authors', 'publisher', 'release_date', 'series_name']
    else:
        fields = ['id', 'title', 'authors', 'publisher', 'release_date', 'series_name']

    # Build SELECT clause
    select_clause = "SELECT SQL_CALC_FOUND_ROWS DISTINCT " + ", ".join([valid_fields[f] for f in fields])
    
    # Base FROM clause
    from_clause = " FROM Books b"
    joins = []

    # Dynamically append JOINs only if they are needed for SELECT or WHERE clauses
    if 'authors' in fields or params.get('author'):
        joins.append("LEFT JOIN bookAuthors ba ON b.id = ba.book_id")
        joins.append("LEFT JOIN Authors a ON ba.author_id = a.id")
        
    if 'publisher' in fields or params.get('publisher'):
        joins.append("LEFT JOIN bookPublishers bp ON b.id = bp.book_id")
        joins.append("LEFT JOIN publisher p ON bp.publisher_id = p.id")
        
    if 'series_name' in fields or params.get('serie'):
        joins.append("LEFT JOIN series s ON b.series_id = s.id")
        
    if 'genres' in fields:
        joins.append("LEFT JOIN bookGenres bg ON b.id = bg.book_id")
        joins.append("LEFT JOIN genres g ON bg.genre_id = g.id")
        
    if 'labels' in fields:
        joins.append("LEFT JOIN bookLabel bl ON b.id = bl.book_id")
        joins.append("LEFT JOIN labels l ON bl.label_id = l.id")

    # Ensure uniqueness of joins while preserving order
    unique_joins = []
    for j in joins:
        if j not in unique_joins:
            unique_joins.append(j)

    base_query = select_clause + from_clause + "\n" + "\n".join(unique_joins)

    # Build WHERE clause
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
        base_query += "\nWHERE " + " AND ".join(conditions)

    # Build GROUP BY clause dynamically based on non-aggregated selected fields
    group_by_fields = []
    for f in fields:
        if f not in ['authors', 'genres', 'labels']: # These fields use GROUP_CONCAT
            if f == 'publisher':
                group_by_fields.append('p.name')
            elif f == 'series_name':
                group_by_fields.append('s.name')
            else:
                group_by_fields.append(f'b.{f}')

    if group_by_fields:
        base_query += "\nGROUP BY " + ", ".join(group_by_fields)

    # Apply Sorting and Pagination
    (c, p) = sortPagination_query(params)
    if c:
        base_query += "\n" + "\n".join(c)
    if p:
        parameters.extend(p)

    return base_query, parameters, fields


@app.route('/keepalive', methods=['GET','POST'])
def kpalive():
    return '', 204

@app.route('/book', methods=['GET'])
def get_books():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Get query parameters
        params = { k: request.args.get(k) for k in request.args.keys() }

        # Unpack the dynamic columns list as well
        query, parameters, columns = build_query(params)

        print(query)
        print()
        print(parameters)

        cur = conn.cursor()
        cur.execute(query, parameters)

        # Fetch results
        results = []

        for row in cur:
            book_dict = {}
            # Map the dynamically requested columns to the fetched row indices
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
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        try:
            # Process JSON data
            data = request.get_json()
            with open('data.json', 'w') as f: # temporary: for debug
                json.dump(data, f, indent=3)
            if data.get('title'):
                logging.info(f"Receive new book, title: {data['title']}")
                print(f"Receive new book, title: {data['title']}")
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

# Modify the existing get_authors function
@app.route('/authors', methods=['GET'])
def get_authors():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        query = request.args.get('query', '')
        authors = author_handler.get_items(conn, query)
        return jsonify(authors)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

# Modify the existing get_publishers function
@app.route('/publishers', methods=['GET'])
def get_publishers():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        query = request.args.get('query', '')
        publishers = publisher_handler.get_items(conn, query)
        return jsonify(publishers)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

# Add new series endpoints
@app.route('/series', methods=['GET'])
def get_series():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        query = request.args.get('query', '')
        series = series_handler.get_items(conn, query)
        return jsonify(series)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

# Add new genres endpoints
@app.route('/genres', methods=['GET'])
def get_genres():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        query = request.args.get('query', '')
        genres = genres_handler.get_items(conn, query)
        return jsonify(genres)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

# Add new labels endpoints
@app.route('/labels', methods=['GET'])
def get_labels():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        query = request.args.get('query', '')
        labels = labels_handler.get_items(conn, query)
        return jsonify(labels)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


@app.route('/series/add', methods=['POST'])
def add_series():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()
        series_handler.add_item(conn, data)
        return jsonify({'message': 'Series added successfully'}), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if conn:
            conn.close()

# Modify the existing publisher/add endpoint
@app.route('/publisher/add', methods=['POST'])
def add_publisher():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()
        publisher_handler.add_item(conn, data)
        return jsonify({'message': 'Publisher added successfully'}), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if conn:
            conn.close()

@app.route('/bookinfo', methods=['GET', 'POST'])
def book_info():
    """Handle book information retrieval and updates"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        book_handler = BookInfoHandler(conn)

        if request.method == 'GET':
            # Get book information by ID
            book_id = request.args.get('id')
            if not book_id:
                return jsonify({"error": "Book ID parameter is required"}), 400

            try:
                book_id = int(book_id)
            except ValueError:
                return jsonify({"error": "Invalid book ID format"}), 400

            book_info = book_handler.get_book_info(book_id)
            if not book_info:
                return jsonify({"error": "Book not found"}), 404

            return jsonify({
                "status": "success",
                "book": book_info
            })

        # TODO
        elif request.method == 'POST':
            # Update book information
            book_id = request.args.get('id')
            if not book_id:
                return jsonify({"error": "Book ID parameter is required"}), 400

            try:
                book_id = int(book_id)
            except ValueError:
                return jsonify({"error": "Invalid book ID format"}), 400

            # Get JSON data from request
            if request.headers.get('Content-Type') != 'application/json':
                return jsonify({'error': 'Content-Type must be application/json'}), 415

            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON data provided"}), 400

            # Log the update operation
            logging.info(f"Updating book ID: {book_id}")

            # Update book information
            success = book_handler.update_book_info(book_id, data)

            if success:
                return jsonify({
                    "status": "success",
                    "message": "Book updated successfully"
                })
            else:
                return jsonify({"error": "Failed to update book"}), 500

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error in book_info endpoint: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    finally:
        if conn:
            conn.close()

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def update_book(book_id):
    """Handle book retrieval and updates by ID"""
    if request.method == 'GET':
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        try:
            book_handler = BookInfoHandler(conn)
            book_info = book_handler.get_book_info(book_id)

            if not book_info:
                return jsonify({"error": "Book not found"}), 404

            return jsonify(book_info)

        except Exception as e:
            logging.error(f"Error fetching book {book_id}: {e}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

        finally:
            if conn:
                conn.close()

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        db = BookUpdateDatabase(conn)

        if request.method == 'DELETE':
            logging.info(f"Deleting book ID: {book_id}")
            result = db.delete_book(book_id)

            if result.get("not_found"):
                return jsonify({"error": "Book not found"}), 404

            return jsonify({
                "status": "success",
                "book_id": book_id
            }), 200

        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({'error': 'Content-Type must be application/json'}), 415

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        logging.info(f"Updating book ID: {book_id} via PUT method")
        result = db.update_book(book_id, data)

        if result.get("not_found"):
            return jsonify({"error": "Book not found"}), 404

        return jsonify({
            "status": "success",
            "book_id": book_id
        }), 200

    except ValueError as e:
        logging.error(f"Validation error processing {request.method} request for book {book_id}: {e}")
        return jsonify({"error": str(e)}), 400
    except mariadb.Error as e:
        logging.error(f"Database error processing {request.method} request for book {book_id}: {e}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        logging.error(f"Error processing {request.method} request for book {book_id}: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    finally:
        conn.close()


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
    """Get single book information by ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        book_handler = BookInfoHandler(conn)
        book_info = book_handler.get_book_info(book_id)

        if not book_info:
            return jsonify({"error": "Book not found"}), 404

        return jsonify(book_info)

    except Exception as e:
        logging.error(f"Error fetching book {book_id}: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    finally:
        if conn:
            conn.close()

# Custom decorator to check Nginx injected headers
def require_role(allowed_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = request.headers.get('X-App-Role', 'standard')
            if user_role != allowed_role:
                return jsonify({
                    "error": "Unauthorized: Subnet access restricted",
                    "your_role": user_role
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/restart-router', methods=['POST'])
@require_role('admin')
def restart_router():
    # Ensure the directory exists inside the container just in case
    os.makedirs(SHARED_DIR, exist_ok=True)

    trigger_filename = f"task_{uuid.uuid4().hex}.trigger"
    trigger_filepath = os.path.join(SHARED_DIR, trigger_filename)

    try:
        with open(trigger_filepath, 'w') as f:
            f.write("run")
        return jsonify({"status": "success", "message": f"Created {trigger_filename}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
