from flask import Blueprint, current_app, jsonify

from ..services.router_service import RouterService
from .decorators import require_role

system_bp = Blueprint('system', __name__)


@system_bp.route('/keepalive', methods=['GET', 'POST'])
def keepalive():
    return '', 204


@system_bp.route('/restart-router', methods=['POST'])
@require_role('admin')
def restart_router():
    try:
        trigger_filename = RouterService(current_app.config['SHARED_DIR']).create_restart_trigger()
        return jsonify({"status": "success", "message": f"Created {trigger_filename}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
