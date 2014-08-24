from basewidgets import ModelWidget
from blog import models

class TagWidget(ModelWidget):
    _model = models.Tag

    def render(self,*args,**kwargs):
        rtn = '<ul>\n'
        for tag in self._model.query.all():
            rtn += '<li class=tag><a href="{}">{}</a></li>\n'.format(tag.link,tag.name)
        return rtn + '</ul>'



