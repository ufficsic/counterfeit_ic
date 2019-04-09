from functools import wraps
from flask import session, request, redirect, url_for, abort, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            flash('Login required to access the resouce!', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def approval_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (
            session.get('username') is None or 
            session.get('is_approved') is None or 
            session.get('is_approved') is False
        ):
            flash('Login Required to access this resource!', 'error')
            flash('Admin info is found in the Contact tab!', 'error')
            return redirect(url_for('login', next=request.url))
            # abort(403)
        return f(*args, **kwargs)
    return decorated_function


def contributor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (
            session.get('username') is None or 
            session.get('is_approved') is None or 
            session.get('x') is False or
            session.get('is_contributor') is None or 
            session.get('is_contributor') is False 
        ):
            flash('Contibutor Access restricted, contact admin!', 'error')
            flash('Admin info is found in the Contact tab!', 'error')
            return redirect(url_for('index'))
            # abort(403)
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (
            session.get('username') is None or 
            session.get('is_admin') is None or 
            session.get('is_admin') is False
        ):
            flash('Admin Access restricted, contact admin!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
