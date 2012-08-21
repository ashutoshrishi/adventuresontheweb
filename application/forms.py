from wtforms import Form, TextField, validators, TextAreaField, HiddenField

class CommentForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=50),
                              validators.Required()])
    email = TextField('Email')
    comment = TextAreaField('Comment',  [validators.Required()])
    slug = HiddenField('Slug', [validators.Required()])

