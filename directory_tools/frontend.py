from logging import basicConfig as initializeLog, INFO

from directory_tools.email_sender import EmailSender
from directory_tools.directory_tools import Commands
from directory_tools.change_password_form import ChangePasswordForm
from directory_tools.change_email_form import ChangeEmailForm
from directory_tools.profile_form import ProfileForm
from directory_tools.client import AuthenticationError
from directory_tools.login_form import LoginForm
from directory_tools.recover_form import RecoverForm
from sentry_sdk import init as initialize_sentry, capture_exception
from directory_tools.register_form import RegisterForm
from flask import Blueprint, request, session, redirect, url_for, \
    render_template, flash
from python_utility.configuration import Configuration

initializeLog(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
configuration = Configuration('~/.directory-tools.yaml')
frontend = Blueprint('frontend', __name__, template_folder='templates')
host = configuration.get('host')
domain = configuration.get('domain')
top_level = configuration.get('top_level')
manager_name = configuration.get('manager-name')
manager_password = configuration.get('manager-password')
token = configuration.get('token')
email_sender = EmailSender(
    server=configuration.get('email_server'),
    sender=configuration.get('email_sender'),
)
initialize_sentry(configuration.get('sentry_locator'))
listen_address = configuration.get('listen_address')


@frontend.route('/')
def index():
    return render_template(template_name_or_list='index.html')


@frontend.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            create_commands().add_user(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data,
                email=form.email.data,
            )
            # TODO: Send confirmation email.
            email_sender.send(
                subject='Registration',
                recipient=form.email.data,
                body='Registration complete.'
            )
            flash('Registration complete.')

            return redirect(url_for('.login'))
        except RuntimeError as error:
            capture_exception(error)
            message = str(error)

            if message == 'entryAlreadyExists':
                flash('Username already exists.')
            else:
                flash('Unexpected error: ' + message)

    return render_template('register.html', form=form)


@frontend.route('/confirm', methods=['GET'])
def confirm():
    return render_template('confirm.html')


@frontend.route('/recover', methods=['GET', 'POST'])
def recover():
    form = RecoverForm(request.form)

    if request.method == 'POST' and form.validate():
        # TODO: look up form.email.data or form.username.data and send
        # recovery mail.
        # flash('Email sent.')
        flash('Not implemented yet.')

        return redirect(url_for('.recover'))

    return render_template(template_name_or_list='recover.html', form=form)


@frontend.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            create_commands().authenticate(
                username=form.username.data,
                password=form.password.data,
            )
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('Login successful.')

            return redirect(url_for('.index'))
        except AuthenticationError as error:
            capture_exception(error)
            flash('Login failed.')

            return redirect(url_for('.login'))

    return render_template('login.html', form=form)


@frontend.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        session.pop('username', None)
        flash('Logged out.')
    else:
        flash('Not logged in.')

    return redirect(url_for('.index'))


@frontend.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'logged_in' in session:
        form = ProfileForm(request.form)

        if request.method == 'POST' and form.validate():
            # TODO: Allow changing username if not used.
            # Log out afterwards.
            create_commands().set_first_name(
                username=session['username'],
                first_name=form.first_name.data,
            )
            create_commands().set_last_name(
                username=session['username'],
                last_name=form.last_name.data,
            )
            flash('Profile updated.')

            return redirect(url_for('.profile'))

        return render_template(
            template_name_or_list='profile.html',
            form=form,
        )
    else:
        flash('Not logged in.')

        return redirect(url_for('.login'))


@frontend.route('/change_email', methods=['GET', 'POST'])
def change_email():
    if 'logged_in' in session:
        form = ChangeEmailForm(request.form)

        if request.method == 'POST' and form.validate():
            create_commands().set_email(
                username=session['username'],
                email=form.email.data,
            )
            # TODO: Send confirmation email to form.email.data.
            # flash('Email sent.')
            flash('Email changed.')

            return redirect(url_for('.change_email'))

        return render_template(
            template_name_or_list='change_email.html',
            form=form,
        )
    else:
        flash('Not logged in.')

        return redirect(url_for('.login'))


@frontend.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'logged_in' in session:
        form = ChangePasswordForm(request.form)

        if request.method == 'POST' and form.validate():
            # TODO: Check form.current_password.data
            create_commands().set_password(
                username=session['username'],
                password=form.password.data,
            )
            flash('Password changed.')

            return redirect(url_for('.change_password'))

        return render_template(
            template_name_or_list='change_password.html',
            form=form,
        )
    else:
        flash('Not logged in.')

        return redirect(url_for('.login'))


def authorize():
    header = str(request.headers.get('Authorization'))
    authorization_type = ''
    passed_token = ''

    if header != '':
        elements = header.split(' ')

        if len(elements) is 2:
            authorization_type = elements[0]
            passed_token = elements[1]

    if passed_token != token or authorization_type != 'Token':
        return 'Authorization failed.'

    return ''


def create_commands() -> Commands:
    return Commands(
        domain=domain,
        top_level=top_level,
        host=host,
        manager_name=manager_name,
        manager_password=manager_password,
    )
