import os
import json
from flask import current_app
from flask_admin import Admin, BaseView,expose,helpers,AdminIndexView
from flask_admin.contrib.sqla.view import ModelView
from .models import Page, Category
from .forms import ContactUsSettingsForm
from . import page




class IndexView(AdminIndexView):
    @expose()
    def index(self,*args,**kwargs):
        return self.render('admin/dashboard.html')

admin = Admin(name='Page Admin',index_view=IndexView(),template_mode='bootstrap3')

@page.before_app_first_request
def add_admin():
    current_app.test_request_context().push()
    admin.init_app(current_app)
    current_app.test_request_context().pop()

class PageAdmin(ModelView):
    column_list = ['title','slug','template_file','date_modified']

    def __init__(self,*args,**kwargs):
        ModelView.__init__(self,model=Page,session=Page._session,*args,**kwargs)

class ContactUsAdmin(BaseView):
    @expose('/',methods=['post','get'])
    def index(self):
        form = ContactUsSettingsForm(flask.request.form)
        if flask.request.method.lower() == 'post':
            data = dict(
                address=form.address.data,
                email=form.email.data,
                phone=form.phone.data,
                hours=form.hours.data,
                facebook_link=form.facebook_link.data,
                twitter_link=form.twitter_link.data,
                google_link=form.google_link.data,
            )
            with open(os.path.join(base,'contact_data.json'),'w') as f:
                f.write(json.dumps(data))
        data = json.loads(open(os.path.join(base,'contact_data.json'),'r').read())
        form = ContactUsSettingsForm(**data)
        return self.render('admin/settings.html',form=form)

class CategoryAdmin(ModelView):
    def __init__(self,*args,**kwargs):
        ModelView.__init__(self,model=Category,session=Category._session,*args,**kwargs)

for category,_admin in [
            ('settings',ContactUsAdmin),
            ('cms',PageAdmin),
            ('cms',CategoryAdmin),
    ]:
    admin.add_view(
        _admin(
            category = category
        )
    )
