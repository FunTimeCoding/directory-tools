from wtforms import Form, PasswordField, validators


class ChangePasswordForm(Form):
    current_password = PasswordField('Current password')
    password = PasswordField('New password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Repeat password')
