from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC
from python_utility.custom_argument_parser import CustomArgumentParser
from python_utility.yaml_config import YamlConfig


class DirectoryTools:
    def __init__(self, arguments: list):
        self.parsed_arguments = self.parse_arguments(arguments)

        config = YamlConfig(path='~/.directory-tools.yml')
        host = config.get('host')
        domain = config.get('domain')
        top_level = config.get('top_level')
        self.suffix = 'dc=' + domain + ',dc=' + top_level
        manager_name = config.get('manager-name')
        manager_relative_dn = 'cn=' + manager_name
        self.manager_dn = manager_relative_dn + ',' + self.suffix
        self.manager_password = config.get('manager-password')
        self.server_name = host + '.' + domain + '.' + top_level

    def parse_arguments(self, arguments: list) -> list:
        parser = self.create_parser()
        parsed_arguments = parser.parse_args(arguments)
        print(parsed_arguments)

        return parsed_arguments

    def create_server(self) -> Server:
        return Server(
            host=self.server_name,
            port=389,
            get_info=False
        )

    def create_connection(self, server: Server) -> Connection:
        return Connection(
            server,
            auto_bind=True,
            version=3,
            client_strategy=STRATEGY_SYNC,
            user=self.manager_dn,
            password=self.manager_password,
            authentication=AUTH_SIMPLE,
            lazy=False,
            check_names=False
        )

    def search(
        self,
        connection: Connection,
        search_filter: str,
        attributes: list
    ):
        result = connection.search(
            search_base=self.suffix,
            search_filter=search_filter,
            attributes=attributes
        )

        if not isinstance(result, bool):
            response, result = connection.get_response(result)
        else:
            response = connection.response
            result = connection.result

        return response, result

    def search_user(self, connection, search_filter):
        attributes = [
            'uid',
            'displayName',
            'uidNumber',
            'gidNumber'
            'homeDirectory',
            'loginShell',
            'gecos',
            'mail'
        ]
        return self.search(connection, search_filter, attributes)

    def run(self):
        server = self.create_server()
        connection = self.create_connection(server)
        response, result = self.search(
            connection, '(cn=admin)', ['cn', 'description']
        )

        print(result)
        print(response)

        response, result = self.search_user(connection, '(uid=areitzel)')

        print(result)
        print(response)

        return 0

    @staticmethod
    def create_parser() -> CustomArgumentParser:
        description = 'Directory administration tool.'
        parser = CustomArgumentParser(description=description)

        return parser
