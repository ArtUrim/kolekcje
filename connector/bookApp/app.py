from flask import Flask, jsonify

from .api import register_blueprints
from .config import Config
from .core import db


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    register_blueprints(app)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
