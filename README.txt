##Flask-XXL 
####- A best practices approach to creating larger web apps with Flask, in an attempt to make Flask feel like it is as capable, if not more, than __Django__.



<script data-codementor="jstacoder" data-style="badge" data-theme="dark" src="https://cdn.codementor.io/assets/badge.js"></script>

_to see this in a real world example take a look at my other project_ [Flask-Cms](https://github.com/jstacoder/flask-cms)

##What this provides:

-   basemodels.py 
    -   with a BaseMixin class that provides many useful CRUD operations, IE: model.save(), model.delete()

-   baseviews.py
    -   with a BaseView class that is subclassed from Flask.views.MethodView to allow easy definition of view responses to get and post requests.
    -   BaseView also has many builtin helpers/imports to speed development, ie: 
        -   BaseView.render() calls render_template(BaseView._template,**BaseView._context) easily define either or both in the class variable
            section of the class and then add,change/ w/e based on logic that happens during request processing. 
            example:
            
            ```python 
            class ExampleView(BaseView):
                _context = {
                    'some_flag':True,
                }

                def get(self,new_flag=False):
                    if new_flag:
                        self._context['new_flag'] = new_flag
                        self._context['some_flag'] = False
                    return self.render()
            ```
        -   <kbd>BaseView.redirect(endpoint)</kbd>
        is a reimplementation of <code>flask.helpers.redirect</code> which allows you to directly enter the
        endpoint, so you dont have to run it through <code>url_for()</code> first. 
        
        -   <pre>BaseView.get_env()</pre> returns the current jinja2_env
        
        
        - <pre>BaseView.form_validated()</pre> returns true if all forms validate
        
        -   __namespaces imported into BaseView__:
            BaseView.flash == flask.flash
            
        
            

-   many builtin template globals(context_processors) to use.
    ie: 

        -   get_block(block_id) <-- requires use of flask.ext.xxl.apps.blog 
            *   add blocks of html/jinja2/template helpers into the db and access from within templates
                great for things like header navs or sidebar widgets
                
        -   get_icon(icon_name,icon_lib) <-- requires use of flask.ext.xxl.apps.blog
            * flask.ext.xxl.apps.blog comes with 8 icon librarys!!! 
                -   Glyphicon
                -   Font Awesome
                -   Mfg_Labs
                -   Elusive icons
                -   Genericons
                -  and more ... 
                access any icon anywhere in your templates! even from cms blocks!!!
                
        -   get_model(model_name,blueprint_name)
            * access any model class from any template (currently only supports sqlalchemy models)
            
        -   get_button(name) 
            * create buttons in the cms and access from within templates


-   AppFactory class with many hooks into settings file (makes use of settings file similar to django)
    -   settings like:
        -   CONTEXT_PROCESSORS
        -   TEMPLATE_FILTERS
        -   URL_ROUTE_MODULES
        -   INSTALLED_BLUEPRINTS etc..

-   new revamped url routing scheme, use a urls.py file in each blueprint to 
    define the url routes for the blueprint. reference the blueprint and the url
    route module in the settings file to registar onto the app upon instantiation.

    define routes like this:

    file: urls.py
    ```python
        from blueprint import blueprint
        from .views import ViewName,SecondView

        routes = [
            ((blueprint_name,)
                ('/url',ViewName.as_View('view_name')),
                ('/another',SecondView.as_view('second_view')),
            )
        ]
    ```
    it basicly is like using app.add_url_rule() method, you
    just dont have to add <code>view_func=ViewName.as_view(endpoint)</code> or at least the
    <code>view_func=</code> part.


-   easily start a new project or extend an old one with the flaskxxl-manage.py command line helper tool
    -   to start a project from scratch
        <kbd>$ flaskxxl-manage.py start-project</kbd>
        
    -   to add to an existing project 
        <kbd>$ flaskxxl-manage.py start-blueprint</kbd>
