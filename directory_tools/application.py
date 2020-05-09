from flask import Flask
from os.path import expanduser


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(expanduser('~/.directory-tools.py'))

    from directory_tools.frontend import frontend
    app.register_blueprint(frontend)

    return app
