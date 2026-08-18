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

from book_query_builder import BookQueryBuilder

from isbn  import normalize_isbn, validate_isbn

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

        # Instantiate builder and unpack the results
        builder = BookQueryBuilder(params)
        query, parameters, columns = builder.build()

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
            errJson =  { 'error': f"Error processing addbook POST request: {e}" }
            if data and data.get('title'):
                logging.warn( f"for the book {data['title']}")
                errJson['book'] = data['title']
            return jsonify(errJson), 415
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

@app.route('/books/validate', methods=['GET'])
def validate_book():

    if len(request.args) == 0:
        return jsonify( {"result": "empty hint list" } ), 403

    isbn_valid = None
    if 'isbn' in request.args:
        isbn_norm = normalize_isbn( request.args.get('isbn') )
        if isbn_norm:
            isbn_valid = validate_isbn( isbn_norm )

        if isbn_valid is not True:
            isbn_result = { "title": "Invalid ISBN" }
            if not isbn_norm:
                isbn_result['detail'] = f"Provided ISBN {request.args.get('isbn')} cannot be normalized"
            else:
                isbn_result['detail'] = f"Provided ISBN {request.args.get('isbn')} has no valid checksum"

            return jsonify(isbn_result), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        book_handler = BookInfoHandler(conn)
        book_info = book_handler.get_basic_book_info( request.args )

        if not book_info:
            return '', 204

        return jsonify(book_info[0]), 409

    except Exception as e:
        logging.error(f"Error validate book: {e}")
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
