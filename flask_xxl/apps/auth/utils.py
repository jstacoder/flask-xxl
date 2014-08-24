from flask import session, g, flash, redirect, url_for, request
from functools import wraps


def login_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['email'] = user.email

def logout_user(user):
    session.pop('logged_in',None)
    session.pop('user_id',None)
    session.pop('email',None)

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return view(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('auth.login',next=request.url))
    return wrapper

def admin_required(view):
    @wraps(view)
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            if User.get_by_id(session.get('user_id')).is_admin:
                return view(*args,**kwargs)
        flash('You need to login as an administrator to access that page.')
        return redirect(url_for('auth.login',next=request.url))
    return wrapper

