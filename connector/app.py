from flask import Flask, request, jsonify, Response
import mariadb
from typing import Optional, Dict, Any
import sys
import logging
import json
from typing import List, Dict

from addBook import BookDatabase
# Add to imports at the top
from table_handler import TableHandler

# Create handlers after app initialization
publisher_handler = TableHandler('publisher')
author_handler = TableHandler('Authors')
series_handler = TableHandler('series')
genres_handler = TableHandler('genres')

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
        LEFT JOIN bookPublishers bp ON b.id = bp.book_id
        LEFT JOIN publisher p ON bp.publisher_id = p.id
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
                #db.insert_book( data )
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
