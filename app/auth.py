"""
Authentication module for Roblox Camera Server
"""

from functools import wraps
from flask import request, jsonify, current_app


def get_token_from_request():
    """Extract token from Authorization header"""
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    return auth_header[7:]  # Remove 'Bearer ' prefix


def require_token(token_type='frontend'):
    """Decorator to require authentication token"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_request()
            
            if not token:
                return jsonify({'error': 'Missing authorization token'}), 401
            
            if token_type == 'roblox':
                expected_token = current_app.config['ROBLOX_TOKEN']
            elif token_type == 'frontend':
                expected_token = current_app.config['FRONTEND_TOKEN']
            else:
                return jsonify({'error': 'Invalid token type'}), 400
            
            if token != expected_token:
                return jsonify({'error': 'Invalid token'}), 401
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_roblox_token(f):
    """Decorator to require Roblox token"""
    return require_token('roblox')(f)


def require_frontend_token(f):
    """Decorator to require Frontend token"""
    return require_token('frontend')(f)
