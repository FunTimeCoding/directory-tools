from wtforms import Form, StringField


class RecoverForm(Form):
    username = StringField('Username')
    email = StringField('Email')
