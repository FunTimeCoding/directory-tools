from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC
from python_utility.yaml_config import YamlConfig

class DirectoryTools:
    @staticmethod
    def run():
        config = YamlConfig(path='~/.directory-tools.yml')
        password = config.get('password')

        server = Server(
            host='localhost',
            port=389,
            get_info=False
        )

        connection = Connection(
            server,
            auto_bind=True,
            version=3,
            client_strategy=STRATEGY_SYNC,
            user='cn=admin,dc=shiin,dc=org',
            password=password,
            authentication=AUTH_SIMPLE,
            lazy=False,
            check_names=False
        )

        result = connection.search(
            search_base='dc=shiin,dc=org',
            search_filter='(cn=admin)',
            attributes=['cn', 'description']
        )

        if not isinstance(result, bool):
            response, result = connection.get_response(result)
        else:
            response = connection.response
            result = connection.result

        print(result)
        print(response)

        return 0
