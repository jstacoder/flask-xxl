from flask.views import MethodView
from flask.templating import render_template
from flask.helpers import url_for
from flask import redirect, flash
from wtforms.form import FormMeta

class BaseView(MethodView):
    _template = None
    _form = None
    _context = {}
    _form_obj = None
    _obj_id = None
    _form_args = {}

    def render(self,**kwargs):
        if self._template is None:
            return NotImplemented
        if kwargs:
            self._context.update(kwargs)
        if self._form is not None:

            if type(self._form) == FormMeta:
                if self._form_obj is not None:
                    self._context['form'] = self._form(obj=self._form_obj,**self._form_args)
                else:
                    self._context['form'] = self._form(**self._form_args)
                if self._obj_id is not None:
                    self._context['obj_id'] = self._obj_id
            else:
                self._context['form'] = self._form
            choices = self._context.get('choices')
            if choices:
                self._context['form'].template.template.choices = choices
            for f,v in self._form_args.items():
                self._form.__dict__[f].data = v
        return render_template(self._template,**self._context)

    def redirect(self,endpoint,**kwargs):
        if not kwargs.pop('raw',False):
            return redirect(url_for(endpoint,**kwargs))
        return redirect(endpoint,**kwargs)
        

    def flash(self,*args,**kwargs):
        if not 'category' in kwargs:
            kwargs['category'] = 'warning'
        flash(*args,**kwargs)

    def form_validated(self):
        if self._form:
            return self._form().validate()
        return False

    def get_form_data(self):
        result = {}
        for field in self._form():
            name = field.name
            if '_' in field.name:
                if not field.name.startswith('_'):
                    if not field.name.endswith('_'):
                        if field.name.split('_')[0] == field.name.split('_')[1]:
                            name = field.name.split('_')[0]
            result[name] = field.data
        return result
    
    def get_env(self):
        from flask import current_app
        return current_app.create_jinja_environment()


class ModelView(BaseView):
    _model = None

    def render(self,**kwargs):
        if self._model is not None:
            if 'model_id' in kwargs:
                model_id = kwargs.pop('model_id')
            elif self._model.__name__ + '_id' in kwargs:
                model_id = kwargs.pop(self._model.__name__+'_id')
            else:
                model_id = None
            if model_id is not None:
                self._context['object'] = self.get_by_id(model_id)
            else:
                self._context['object'] = self._model()
            self.context['model'] = self._model
        return super(ModelView,self).render(**kwargs)

    def add(self,**kwargs):
        tmp = self._model(**kwargs)
        tmp.save()

    def update(self,model_id,**kwargs):
        tmp = self._model.query.filter_by(self._model.id==model_id).first()
        if 'return' in kwargs:
            if kwargs.pop('return',None):
                rtn = True
            else:
                rtn = False
        for k in kwargs.keys():
            tmp.__dict__[k] = kwargs[k]
        tmp.save()
        if rtn: return tmp

    def get_by_id(self,model_id):
        tmp = self._model.get_by_id(model_id)
        return tmp
