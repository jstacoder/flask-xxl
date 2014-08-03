from admin import admin
from importlib import import_module
from flask import current_app
from .models import Setting,Type
from flask.ext.wtf import Form


class BaseSettings(object):
    _settings = []
    _values = {}
    _form = None
    _defaults = {}
    _cfg = ''

    def __init__(self):
        self._cfg = current_app.config
        for itm in self._settings:
            if not itm in self._values:
                try:
                    self.set_setting(itm,self._defaults[itm])
                except KeyError:
                    raise ValueError('Need to be given a value or default for {}'.format(itm))
            self.set_setting(itm,self._cfg[itm])

    def _get_setting_field(self,setting,field_type=None):
        pass

    def _get_form(self):
        raise NotImplementedError

    @property
    def form(self):
        return self._get_form()

    def set_setting(self,setting,value):
        if setting in self._settings:
            self._values[setting] = value

    def get_setting(self,setting,default=None):
        if setting in self._settings:
            return self._values[setting]
        return default

    def apply_settings(self,**kwargs):
        if len(kwargs) > 0:
            for k in kwargs:
                self.set_setting(k,kwargs[k])
        for setting in self._settings:
            if not setting.startswith('_'):
                self._cfg[setting.upper()] = self.get_setting(setting)

    def _get_default_field(self,setting,fields):
        return fields.__dict__['StringField']

class SiteSettings(BaseSettings):
    _settings = [
            'RECAPTCHA_PUBLIC_KEY',
            'RECAPTCHA_PRIVATE_KEY',
            'ADMIN_PER_PAGE',
            'CODEMIRROR_LANGUAGES',
            'CODEMIRROR_THEME',
            'BLUEPRINTS',
            'EXTENSIONS',
            'TEMPLATE_FILTERS',
            'CONTEXT_PROCESSORS',
    ]
    _defaults = {
            'RECAPTCHA_PUBLIC_KEY':'',
            'RECAPTCHA_PRIVATE_KEY':'',
            'ADMIN_PER_PAGE':'',
            'CODEMIRROR_LANGUAGES':['python'],
            'CODEMIRROR_THEME':'3024-year',
            'BLUEPRINTS':'',
            'EXTENSIONS':'',
            'TEMPLATE_FILTERS':'',
            'CONTEXT_PROCESSORS':'',
    }
    def _get_setting_field(self,setting,field_type=None):
        fields = import_module('wtforms.fields')
        if field_type is not None:
            field = fields.__dict__[field_type]
        else:
            from .models import Setting
            s = Setting.query.filter(Setting.name==setting).first()
            if s is None:
                field = self._get_default_field(setting,fields)
            else:
                field = fields.__dict__[s.type.field_type]
        return field

    def _get_form(self):
        form_args = {}
        for itm in self._settings:
            form_args[itm] = self._get_setting_field(itm)()
        self._form = type(
            'EditSiteSettingsForm',(Form,),form_args
        )
        return self._form






@admin.before_app_request
def add_settings():
    from app import app
    settings = app.config.copy()
    CACHED_SETTINGS = [
            'RECAPTCHA_PUBLIC_KEY',
            'RECAPTCHA_PRIVATE_KEY',
            'ADMIN_PER_PAGE',
            'CODEMIRROR_LANGUAGES',
            'CODEMIRROR_THEME',
            'BLUEPRINTS',
            'EXTENSIONS',
            'TEMPLATE_FILTERS',
            'CONTEXT_PROCESSORS',
    ]
    for itm in CACHED_SETTINGS:
        setting = Setting.query.filter(Setting.name==itm).first()
        if setting is None:
            t = Type.query.filter(Type.name==type(settings[itm])).first()
            value = settings.get(itm,None)
            if value is None:
                value = ''
            if t is None:
                t = Type(type(settings[itm]))
                t.save()
            setting = Setting(
                    name=itm,type=t,value=value
            )
            setting.save()
