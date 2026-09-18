from flask import Blueprint, jsonify, request

from ..core.db import get_db
from ..services.catalog_service import CatalogService

catalog_bp = Blueprint('catalog', __name__)


def _list_items(table_name):
    conn = get_db()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        query = request.args.get('query', '')
        items = CatalogService(conn, table_name).list_items(query)
        return jsonify(items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _add_item(table_name, success_message):
    conn = get_db()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()
        CatalogService(conn, table_name).add_item(data)
        return jsonify({'message': success_message}), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def _get_stats(table_name):
    conn = get_db()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        stats = CatalogService(conn, table_name).get_stats()
        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _get_books_for_item(table_name, item_id):
    conn = get_db()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        books = CatalogService(conn, table_name).get_books_for_item(item_id)
        return jsonify(books)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@catalog_bp.route('/authors', methods=['GET'])
def get_authors():
    return _list_items('Authors')


@catalog_bp.route('/publishers', methods=['GET'])
def get_publishers():
    return _list_items('publisher')


@catalog_bp.route('/series', methods=['GET'])
def get_series():
    return _list_items('series')


@catalog_bp.route('/genres', methods=['GET'])
def get_genres():
    return _list_items('genres')


@catalog_bp.route('/labels', methods=['GET'])
def get_labels():
    return _list_items('labels')


@catalog_bp.route('/labels/stats', methods=['GET'])
def get_labels_stats():
    return _get_stats('labels')


@catalog_bp.route('/labels/<int:label_id>', methods=['GET'])
def get_label_books(label_id):
    return _get_books_for_item('labels', label_id)


@catalog_bp.route('/genres/stats', methods=['GET'])
def get_genres_stats():
    return _get_stats('genres')


@catalog_bp.route('/genres/<int:genre_id>', methods=['GET'])
def get_genre_books(genre_id):
    return _get_books_for_item('genres', genre_id)


@catalog_bp.route('/series/stats', methods=['GET'])
def get_series_stats():
    return _get_stats('series')


@catalog_bp.route('/series/<int:series_id>', methods=['GET'])
def get_series_books(series_id):
    return _get_books_for_item('series', series_id)


@catalog_bp.route('/languages/stats', methods=['GET'])
def get_languages_stats():
    return _get_stats('language')


@catalog_bp.route('/language/<language_id>', methods=['GET'])
def get_language_books(language_id):
    return _get_books_for_item('language', language_id)


@catalog_bp.route('/series', methods=['POST'])
def add_series():
    return _add_item('series', 'Series added successfully')


@catalog_bp.route('/publishers', methods=['POST'])
def add_publisher():
    return _add_item('publisher', 'Publisher added successfully')
