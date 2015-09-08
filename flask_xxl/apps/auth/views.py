from flask import session,redirect,request,render_template
from flask_xxl.baseviews import BaseView
from . import auth
from .forms import UserLoginForm, UserSignupForm
from .utils import login_user, logout_user, login_required, admin_required
from sqlalchemy.exc import IntegrityError


class AuthLoginView(BaseView):
    _template = 'auth_login.html'
    _form = UserLoginForm
    _context = {}

    def get(self):        
        return self.render()

    def post(self):
        form = self._form()
        from .models import User
        if form.validate():
            email = form.email.data
            pw = form.password.data
            remember = form.keep_me_logged_in.data
            u = User.get_by_email(email)
            if u is not None:
                if u.check_password(pw):
                    login_user(u)
                    if 'next' in request.args:
                        return redirect(request.args['next'])
                    else:
                        return self.redirect('core.index')
                else:
                    self.flash('incorrect password')
            else:
                self.flash('user does not exist')
                return self.redirect('auth.signup')
        return self.render()

class AuthSignupView(BaseView):
    _template = 'register.html'
    _form = UserSignupForm
    _context = {}
    
    def get(self):
        return self.render()

    def post(self):
        from auth.models import User
        form = self._form()
        if form.validate():
            email = form.email.data
            pw = form.password.data
            u = User(email=email)
            u.password = pw
            login_user(u)
            self.flash("Thank you for signing up {}".format(email))
            return self.redirect('core.index')
        return self.redirect('auth.signup')


class AuthLogoutView(BaseView):
 
    def get(self):
        from .models import User
        if 'user_id' in session:
            user = User.get_by_id(session['user_id'])
            logout_user(user)
        return self.redirect('core.index')


@auth.app_errorhandler(404)
def not_found(e):
    return render_template('error.html',error_code=404)

