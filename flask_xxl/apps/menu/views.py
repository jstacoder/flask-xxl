from ...baseviews import BaseView


class MenuView(BaseView):
    
    _template = ''
    _form = ''
    _context = {}

    def get(self):
        return self.render()


    def post(self):
        return self.render()



