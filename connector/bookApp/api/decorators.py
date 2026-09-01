from functools import wraps

from flask import jsonify, request

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
