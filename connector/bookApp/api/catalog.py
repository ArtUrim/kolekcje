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


@catalog_bp.route('/series/add', methods=['POST'])
def add_series():
    return _add_item('series', 'Series added successfully')


@catalog_bp.route('/publisher/add', methods=['POST'])
def add_publisher():
    return _add_item('publisher', 'Publisher added successfully')
