
class Widget(object):
    
    def render(self):
        raise NotImplementedError

    def __call__(self):
        return self.render()



class ModelWidget(Widget):
    _model = None
