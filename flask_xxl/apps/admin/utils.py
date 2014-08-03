from ext import db
from flask import url_for
from settings import BaseConfig

class Pagination(object):
    _model = None
    _query = None
    _page_num = 1
    _objs = []
    _obj_page = []
    _per_page = BaseConfig.ADMIN_PER_PAGE
    _page_count = _per_page

    def __init__(self,model,page_num=None,query=None):
        if query is None:
            self._query = model.query.order_by(db.desc(model.id))
        else:
            self._query = query
        self._model = model
        self._page_num = page_num or self._page_num
        self._objs = self._query.all()
        self.set_page(self._objs)

    def set_page(self,obj_list):
        s = ((self._per_page*self._page_num)-self._per_page)
        self._obj_page = []
        total = 0
        while total != self._per_page:
            for i in range(self._per_page):
                try:
                    self._obj_page.append(obj_list[s])
                except:
                    break
                finally:
                    s+=1 
                    total += 1
            break
        


    @property
    def has_next(self):
        return self._page_num != self._per_page*len(self._objs)

    @property
    def has_prev(self):
        return self._page_num != 1

    @property
    def next_link(self):
        if self.has_next:
            return url_for('admin.page_{}'.format(self._model.__name__.lower()),page_num=self.page_num+1)
        return '#'
        
    @property
    def prev_link(self):
        if self.has_prev:
            return url_for('admin.page_{}'.format(self._model.__name__.lower()),page_num=self._page_num-1)
        return '#'
        

def get_pk(obj):
    if 'id' in obj.__dict__:
        return obj.id
    raise IOError

