from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    first_name = StringField('First name', [validators.Length(min=4, max=25)])
    last_name = StringField('Last name', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Repeat password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
