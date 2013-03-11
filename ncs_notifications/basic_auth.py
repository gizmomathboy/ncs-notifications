from flask import request, Response
from functools import wraps

# load the config directly so we can access it without the app object
from settings.config import Config as config


# auth functions
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    auth_username = config.AUTH_USERNAME
    auth_password = config.AUTH_PASSWORD
    return username == auth_username and password == auth_password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
