from wtforms import fields, widgets

class CKTextEditorWidget(widgets.TextArea):
    def __call__(self,field,**kwargs):
        if kwargs.get('class_',False):
            kwargs['class_'] += ' ckeditor'
        else:
            kwargs['class_'] = 'ckeditor'
        kwargs['rows'] = '8'
        return super(CKTextEditorWidget,self).__call__(field,**kwargs)

class CKTextEditorField(fields.TextAreaField):
    widget = CKTextEditorWidget()
