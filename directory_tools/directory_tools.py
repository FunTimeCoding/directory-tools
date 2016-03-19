from argparse import ArgumentDefaultsHelpFormatter
from os import path
from ssl import CERT_REQUIRED

from ldap3 import Server, Connection, Tls, AUTH_SIMPLE, STRATEGY_SYNC, \
    LDAPSocketOpenError
from python_utility.custom_argument_parser import CustomArgumentParser
from python_utility.yaml_config import YamlConfig


class DirectoryTools:
    def __init__(self, arguments: list):
        self.parser = self.create_parser()
        self.parsed_arguments = self.parser.parse_args(arguments)
        print(self.parsed_arguments)

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

    @staticmethod
    def create_parser() -> CustomArgumentParser:
        parser = CustomArgumentParser(
            description='directory administration tool',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers()
        DirectoryTools.add_user_child_parser(subparsers)
        DirectoryTools.add_status_child_parser(subparsers)

        return parser

    @staticmethod
    def add_user_child_parser(subparsers) -> None:
        user_parent = CustomArgumentParser(add_help=False)
        user_parser = subparsers.add_parser(
            'user',
            parents=[user_parent],
            help='manage users'
        )
        user_parser.add_argument('user', action='store_true')
        user_subparsers = user_parser.add_subparsers()

        add_parent = CustomArgumentParser(add_help=False)
        add_parent.add_argument('--user-name')
        add_parent.add_argument('--full-name', required=True)
        add_parent.add_argument('--password', required=True)
        add_parent.add_argument('--mail', required=True)
        add_parent.add_argument(
            '--groups',
            nargs='+',
            metavar='GROUP',
        )
        add_parser = user_subparsers.add_parser(
            'add',
            parents=[add_parent],
            help='add a user'
        )
        add_parser.add_argument('add', action='store_true')

        delete_parent = CustomArgumentParser(add_help=False)
        delete_parent.add_argument('--user-name', required=True)
        delete_parent.add_argument('--full-name', required=True)
        delete_parser = user_subparsers.add_parser(
            'delete',
            parents=[delete_parent],
            help='delete a user'
        )
        delete_parser.add_argument('delete', action='store_true')

        search_parent = CustomArgumentParser(add_help=False)
        search_parent.add_argument('--user-name')
        search_parent.add_argument('--full-name')
        search_parser = user_subparsers.add_parser(
            'search',
            parents=[search_parent],
            help='search for users'
        )
        search_parser.add_argument('search', action='store_true')

        list_parser = user_subparsers.add_parser('list', help='list all users')
        list_parser.add_argument('list', action='store_true')

    @staticmethod
    def add_status_child_parser(subparsers) -> None:
        status_parent = CustomArgumentParser(add_help=False)
        status_parser = subparsers.add_parser(
            'status',
            parents=[status_parent],
            help='show status information'
        )
        status_parser.add_argument('status', action='store_true')

    def create_server(self) -> Server:
        base_path = path.dirname(path.realpath(__file__))
        certificate_path = path.join(
            base_path, '..', 'ldap.shiin.org.node-certificate.crt'
        )

        tls = Tls(
            validate=CERT_REQUIRED,
            ca_certs_file=certificate_path
        )

        return Server(
            host=self.server_name,
            port=389,
            get_info=False,
            tls=tls
        )

    def create_connection(self) -> Connection:
        server = self.create_server()

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
    ) -> [any, object]:
        result = connection.search(
            search_base=self.suffix,
            search_filter=search_filter,
            attributes=attributes
        )

        # TODO: Distinguish better between result and response.

        if isinstance(result, bool):
            response = connection.response
            result = connection.result
        else:
            response, result = connection.get_response(result)

        print('response type: ' + str(type(response)))
        print('result type: ' + str(type(result)))

        return response, result

    def search_user(self, connection, search_filter) -> [any, object]:
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

    def run(self) -> int:
        result = 0

        try:
            connection = self.create_connection()
            if 'user' in self.parsed_arguments:

                if 'add' in self.parsed_arguments:
                    pass
                elif 'delete' in self.parsed_arguments:
                    pass
                elif 'search' in self.parsed_arguments:
                    search_filter = '(uid' + self.parsed_arguments.user_name + ')'
                    response, result = self.search_user(
                        connection, search_filter
                    )
                    print(result)
                    print(response)
                elif 'list' in self.parsed_arguments:
                    pass
                else:
                    self.parser.print_help()
            elif 'status' in self.parsed_arguments:
                connection = self.create_connection()
                response, result = self.search(
                    connection, '(cn=admin)', ['cn', 'description']
                )
                print(result)
                print(response)
            else:
                self.parser.print_help()
        except LDAPSocketOpenError as exception:
            print(str(exception))
            result = 1

        return result
