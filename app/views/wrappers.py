from functools import wraps
from flask import session, redirect


def login_page_first(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            return redirect('/login')
        else:
            return f(*args, **kwargs)
    return decorated_function

