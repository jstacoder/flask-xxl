from flask.ext.xxl.baseviews import BaseView
'''
  Example view class
'''
class ExampleIndexView(BaseView):
    _template = 'index.html'
    
    def get(self):
        return self.render()

