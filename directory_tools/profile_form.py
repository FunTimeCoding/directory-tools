from wtforms import Form, StringField, PasswordField


class ProfileForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')
