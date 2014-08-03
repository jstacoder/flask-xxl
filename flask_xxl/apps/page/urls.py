from page import page
from .views import PagesView,AddPageView

routes = [
        ((page),
            ('/view',PagesView.as_view('page')),
            ('/view/<slug>',PagesView.as_view('pages')),
            ('/add_page',AddPageView.as_view('add_page')),
        )
    ]
