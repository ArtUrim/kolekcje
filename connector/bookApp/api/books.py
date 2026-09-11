import logging

import mariadb
from flask import Blueprint, Response, jsonify, request

from ..core.db import get_db
from ..services.book_service import BookService
from ..services.bookinfo_service import BookInfoService, isbn_validation_error

books_bp = Blueprint('books', __name__)


@books_bp.route('/books', methods=['GET'])
def get_books():
    conn = get_db()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Get query parameters
        params = { k: request.args.get(k) for k in request.args.keys() }

        books, count = BookService(conn).search_books(params)

        return jsonify({
            "status": "success",
            "count": count,
            "books": books
        })

    except mariadb.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@books_bp.route('/books', methods=['POST'])
def add_books():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = None
        try:
            # Process JSON data
            data = request.get_json(silent=True)
            if data is None:
                return jsonify( {'error': 'Bad Request: Invalid JSON data' } ), 400
            BookService(get_db()).add_book(data)
        except Exception as e:
            logging.warning(f"Error processing addbook POST request: {e}")
            errJson =  { 'error': f"Error processing addbook POST request: {e}" }
            if data and data.get('title'):
                logging.warning( f"for the book {data['title']}")
                errJson['book'] = data['title']
            return jsonify(errJson), 415
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415
    return Response( status = 204 )

@books_bp.route('/books/validate', methods=['GET'])
def validate_book():
    if len(request.args) == 0:
        return jsonify( {"result": "empty hint list" } ), 403

    if 'isbn' in request.args:
        isbn_result = isbn_validation_error(request.args.get('isbn'))
        if isbn_result:
            return jsonify(isbn_result), 400

    conn = get_db()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        book_info = BookInfoService(conn).find_matches(request.args)

        if not book_info:
            return '', 204

        return jsonify(book_info[0]), 409

    except Exception as e:
        logging.error(f"Error validate book: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@books_bp.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def update_book(book_id):
    """Handle book retrieval and updates by ID"""
    if request.method == 'GET':
        conn = get_db()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        try:
            book_info = BookInfoService(conn).get_book_info(book_id)

            if not book_info:
                return jsonify({"error": "Book not found"}), 404

            return jsonify(book_info)

        except Exception as e:
            logging.error(f"Error fetching book {book_id}: {e}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    conn = get_db()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        book_service = BookService(conn)

        if request.method == 'DELETE':
            logging.info(f"Deleting book ID: {book_id}")
            result = book_service.delete_book(book_id)

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
        result = book_service.update_book(book_id, data)

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
