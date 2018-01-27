from wtforms import Form, StringField


class ChangeEmailForm(Form):
    email = StringField('Email')
