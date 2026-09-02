import mariadb
from flask import current_app, g


def get_db_connection():
    try:
        return mariadb.connect(**current_app.config['DB_CONFIG'])
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None


def get_db():
    if 'db_connection' not in g:
        g.db_connection = get_db_connection()
    return g.db_connection


def close_db(exception=None):
    connection = g.pop('db_connection', None)
    if connection is not None:
        connection.close()


def init_app(app):
    app.teardown_appcontext(close_db)
