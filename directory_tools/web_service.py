from os.path import expanduser

from flask import Flask

from python_utility.configuration import Configuration


class WebService:
    app = Flask(__name__)

    def __init__(self):
        configuration = Configuration('~/.directory-tools.yaml')
        self.port = configuration.get('port')
        self.app.config.from_pyfile(expanduser('~/.directory-tools.py'))

        from directory_tools.frontend import frontend
        self.app.register_blueprint(frontend)

    @staticmethod
    def main() -> int:
        return WebService().run()

    def run(self) -> int:
        # Avoid triggering a reload. Otherwise stats gets loaded after a
        # restart, which leads to two competing updater instances.
        self.app.run(port=self.port, use_reloader=False)

        return 0
