from app import app, db
from flask import flash, redirect, render_template, request, session, url_for
from functools import wraps
from app.forms import RegisterForm, LoginForm
from app.models import User
from sqlalchemy.exc import IntegrityError

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'error')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You are logged out. Bye. :(')
    return redirect (url_for('login'))

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method=='POST':
        u = User.query.filter_by(name=request.form['name'],
                          password=request.form['password']).first()
        if u is None:
            error = 'Invalid username or password.'
        else:
            session['logged_in'] = True
            session['user_id'] = u.id
            flash('You are logged in. Go Crazy.')
            return redirect(url_for('members'))

    return render_template("login.html",
                           form = LoginForm(request.form),
                           error = error)

@app.route('/members/')
@login_required
def members():
    return render_template('members.html')

@app.route('/register/', methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(
                    form.name.data,
                    form.email.data,
                    form.password.data,
                    )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please login.')
            return redirect(url_for('login'))
        except IntegrityError:
            error = 'Oh no! That username and/or email already exist. Please try again.'
    else:
        flash_errors(form)
    return render_template('register.html', form=form, error=error)

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404