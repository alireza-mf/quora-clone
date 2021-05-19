import functools
from flask import g, abort



def self_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('email', None):
            if g.user.email != kwargs['email']:
                abort(403)
        return func(*args, **kwargs)
    return wrapper