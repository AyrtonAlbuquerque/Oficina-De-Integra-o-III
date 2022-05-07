from flask import request, Response
from functools import wraps
import jwt
from src.utils.jwt import verify_token

def authenticated(route):
    @wraps(route)
    def decorated_route(*args, **kwargs):
        # verify Authorization header
        if not 'Authorization' in request.headers: return Response('No Authorization header', 401)
        if not request.headers['Authorization']: return Response('No Authorization header', 401)

        auth_split = request.headers['Authorization'].split(' ')
        if len(auth_split) != 2: return Response('Invalid Authorization header', 401)
        if auth_split[0] != 'Bearer': return Response('Invalid Authorization header', 401)

        token = auth_split[1]
        decoded = verify_token(token)
        if not decoded: return Response('Invalid token', 401)
        kwargs['user'] = decoded
        return route(*args, **kwargs)
    return decorated_route
