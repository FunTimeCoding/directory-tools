import logging
from sys import argv

from flask import Flask, request, json, render_template, flash, url_for, session
from flask import redirect

from directory_tools.change_email_form import ChangeEmailForm
from directory_tools.change_password_form import ChangePasswordForm
from directory_tools.directory_tools import Commands
from directory_tools.login_form import LoginForm
from directory_tools.profile_form import ProfileForm
from directory_tools.recover_form import RecoverForm
from directory_tools.register_form import RegisterForm
from directory_tools.yaml_config import YamlConfig


class WebService:
    app = Flask(__name__)
    token = None
    host = ''
    domain = ''
    top_level = ''
    manager_name = ''
    manager_password = ''

    def __init__(self, arguments: list) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        config = YamlConfig('~/.directory-tools.yaml')
        WebService.host = config.get('host')
        WebService.domain = config.get('domain')
        WebService.top_level = config.get('top_level')
        WebService.manager_name = config.get('manager-name')
        WebService.manager_password = config.get('manager-password')
        WebService.token = config.get('token')
        WebService.app.secret_key = config.get('secret_key')
        self.listen_address = config.get('listen_address')

    @staticmethod
    def main() -> int:
        return WebService(argv[1:]).run()

    def run(self) -> int:
        # Avoid triggering a reload. Otherwise stats gets loaded after a
        # restart, which leads to two competing updater instances.
        self.app.run(
            host=self.listen_address,
            use_reloader=False
        )

        return 0

    @staticmethod
    @app.route('/')
    def index():
        return render_template(
            template_name_or_list='index.html',
        )

    @staticmethod
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)

        if request.method == 'POST' and form.validate():
            # user = User(form.username.data, form.email.data,
            #             form.password.data)
            # db_session.add(user)
            flash('Registration complete.')

            return redirect(url_for('login'))

        return render_template('register.html', form=form)

    @staticmethod
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm(request.form)

        if request.method == 'POST' and form.validate():
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('Login successful.')

            return redirect(url_for('index'))

        return render_template('login.html', form=form)

    @staticmethod
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        session.pop('username', None)

        return redirect(url_for('index'))

    @staticmethod
    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        form = ProfileForm(request.form)

        if request.method == 'POST' and form.validate():
            flash('Profile updated.')

            return redirect(url_for('profile'))

        return render_template(template_name_or_list='profile.html', form=form)

    @staticmethod
    @app.route('/recover', methods=['GET', 'POST'])
    def recover():
        form = RecoverForm(request.form)

        if request.method == 'POST' and form.validate():
            flash('Email sent.')

            return redirect(url_for('recover'))

        return render_template(template_name_or_list='recover.html', form=form)

    @staticmethod
    @app.route('/change_email', methods=['GET', 'POST'])
    def change_email():
        form = ChangeEmailForm(request.form)

        if request.method == 'POST' and form.validate():
            flash('Email sent.')

            return redirect(url_for('change_email'))

        return render_template(
            template_name_or_list='change_email.html',
            form=form,
        )

    @staticmethod
    @app.route('/change_password', methods=['GET', 'POST'])
    def change_password():
        form = ChangePasswordForm(request.form)

        if request.method == 'POST' and form.validate():
            flash('Password changed.')

            return redirect(url_for('change_password'))

        return render_template(
            template_name_or_list='change_password.html',
            form=form,
        )

    @staticmethod
    def authorize():
        header = str(request.headers.get('Authorization'))
        authorization_type = ''
        token = ''

        if header != '':
            elements = header.split(' ')

            if len(elements) is 2:
                authorization_type = elements[0]
                token = elements[1]

        if token != WebService.token \
                or authorization_type != 'Token':
            return 'Authorization failed.'

        return ''

    @staticmethod
    @app.route('/group', methods=['GET', 'POST'])
    @app.route('/group/<name>', methods=['GET', 'DELETE'])
    def manage_groups(name: str = ''):
        authorization_result = WebService.authorize()

        if authorization_result != '':
            return authorization_result, 401

        commands = Commands(
            domain=WebService.domain,
            top_level=WebService.top_level,
            host=WebService.host,
            manager_name=WebService.manager_name,
            manager_password=WebService.manager_password,
        )

        if request.method == 'GET':
            if name == '':
                return json.dumps(commands.list_groups())
            else:
                return json.dumps(commands.show_group(name=name))
        elif request.method == 'POST':
            return json.dumps(commands.add_group(str(request.json.get('name'))))
        elif request.method == 'DELETE':
            return json.dumps(commands.remove_group(name))
        else:
            return 'Unexpected method: ' + request.method, 500

    @staticmethod
    @app.route('/user', methods=['GET', 'POST'])
    @app.route('/user/<name>', methods=['GET', 'DELETE'])
    def manage_users(name: str = ''):
        authorization_result = WebService.authorize()

        if authorization_result != '':
            return authorization_result, 401

        commands = Commands(
            domain=WebService.domain,
            top_level=WebService.top_level,
            host=WebService.host,
            manager_name=WebService.manager_name,
            manager_password=WebService.manager_password,
        )

        if request.method == 'GET':
            if name == '':
                return json.dumps(commands.list_users())
            else:
                return json.dumps(commands.show_user(name=name))
        elif request.method == 'POST':
            return json.dumps(commands.add_user(str(request.json.get('name'))))
        elif request.method == 'DELETE':
            return json.dumps(commands.remove_user(name))
        else:
            return 'Unexpected method: ' + request.method, 500
