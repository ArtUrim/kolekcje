"""bookApp.api - presentation layer: HTTP routes split into blueprints."""

from .books import books_bp
from .catalog import catalog_bp
from .system import system_bp

ALL_BLUEPRINTS = (books_bp, catalog_bp, system_bp)


def register_blueprints(app):
    for blueprint in ALL_BLUEPRINTS:
        app.register_blueprint(blueprint)
