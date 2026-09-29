from functools import wraps
from flask import request, jsonify
from models import ApiKey

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        key = ApiKey.query.filter_by(key=api_key, active=True).first()
        if not key:
            return jsonify({'error': 'Invalid API key'}), 403
        request.user = key.user
        return f(*args, **kwargs)
    return decorated