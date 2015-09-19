from . import auth 
from .views import AuthLogoutView,AuthLoginView,AuthSignupView

routes = [
        ((auth),
            ('/logout',AuthLogoutView.as_view('logout')),
            ('/','admin_list',AuthLoginView),
            ('/login','login',AuthLoginView),
            ('/register','signup',AuthSignupView),
        )
    ]
