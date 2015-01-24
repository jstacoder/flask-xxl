from . import auth 
from .views import AuthLogoutView,AuthLoginView,AuthSignupView

routes = [
        ((auth),
            ('/logout',AuthLogoutView.as_view('logout')),
            ('',AuthLoginView.as_view('admin_list')),
            ('/login',AuthLoginView.as_view('login')),
            ('/register',AuthSignupView.as_view('signup')),
        )
    ]
