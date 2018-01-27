from wtforms import Form, StringField, PasswordField


class ProfileForm(Form):
    username = StringField('Username')
    first_name = StringField('First name')
    last_name = StringField('Last name')
