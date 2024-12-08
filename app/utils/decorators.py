from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_identity = get_jwt_identity()

            try:
                user_id, role_name = user_identity.split('_', 1)
            except ValueError:
                return jsonify({'error': 'Invalid token data'}), 401

            if role_name not in roles:
                return jsonify({'error': 'Unauthorized'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator