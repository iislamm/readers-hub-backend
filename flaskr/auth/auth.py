from functools import wraps
from flask import request, abort, current_app
import re
import jwt


class AuthError(Exception):
    def __init__(self, error_message, status_code):
        self.error_message = error_message
        self.status_code = status_code


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    if len(header_parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    token = header_parts[1]
    return token


def verify_decode_jwt(token):
    payload = jwt.decode(
        token, current_app.config['TOKEN_SECRET'], algorithms=['HS256'])
    if payload['id'] is None:
        raise AuthError({
            'description': 'invalid token',
            'code': 400
        })
    return payload


def requires_auth():
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                return f(payload, *args, **kwargs)
            except AuthError as ex:
                code = ex.args[1]
                return abort(code)

        return wrapper
    return requires_auth_decorator


def generate_token(payload):
    token = jwt.encode(
        payload, current_app.config['TOKEN_SECRET'], algorithm='HS256')
    return token


def validate_user_data(data):
    if data['name'] is None:
        return False
    if data['email'] is None:
        return False

    if re.search(r'^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$', data['email']) is None:
        return False

    if len(data['password']) < 6:
        return False

    return True
