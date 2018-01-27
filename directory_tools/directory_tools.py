from directory_tools.command_process import CommandProcess
from directory_tools.yaml_config import YamlConfig
from yaml import dump
from sys import argv

from directory_tools.argument_parser import Parser
from directory_tools.client import Client


class Commands:
    def __init__(
            self,
            domain: str,
            top_level: str,
            host: str,
            manager_name: str,
            manager_password: str,
            secure: bool = False
    ) -> None:
        self.suffix = 'dc=' + domain + ',dc=' + top_level
        self.server_name = host + '.' + domain + '.' + top_level
        self.manager = 'cn=' + manager_name + ',' + self.suffix
        self.manager_password = manager_password
        self.secure = secure
        self.client = None

    def lazy_get_client(self) -> Client:
        if self.client is None:
            self.client = Client(
                server_name=self.server_name,
                manager_distinguished_name=self.manager,
                manager_password=self.manager_password,
                suffix=self.suffix,
                secure=self.secure,
            )

        return self.client

    def list_users(self) -> str:
        return self.format_response(
            self.lazy_get_client().search_user('ou=users,' + self.suffix)
        )

    def search(self, query: str) -> list:
        return self.lazy_get_client().search_user(query)

    def show_user(self, name: str):
        return self.format_response(
            self.search('(uid=' + name + ')')
        )

    def show_user_by_full_name(self, name: str):
        return self.format_response(
            self.search('(cn=' + name + ')')
        )

    @staticmethod
    def encrypt_password(password: str) -> str:
        return CommandProcess(
            ['slappasswd', '-s', password]
        ).get_standard_output()

    def add_user(
            self,
            username: str,
            first_name: str,
            last_name: str,
            password: str,
            email: str,
            group: str
    ) -> None:
        posix_account = {
            'full_name': 'cn',  # must
            'username': 'uid',  # must
            'user_number': 'uidNumber',  # must
            'group_number': 'gidNumber',  # must
            'home': 'homeDirectory',  # must
            'password': 'userPassword',  # may
        }
        internet_organization_person = {
            'first_name': 'givenName',  # may
            'last_name': 'sn',  # may
            'email': 'mail',  # may
        }
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.add(
                dn='uid=' + username + ',ou=users,' + self.suffix,
                object_class=[
                    'top',
                    'posixAccount',  # super: top
                    'person',  # super: top
                    'organizationalPerson',  # super: person
                    'inetOrgPerson',  # super: organizationalPerson
                ],
                # TODO: get uid increment
                # TODO: get gid
                attributes={
                    posix_account['full_name']: first_name + ' ' + last_name,
                    posix_account['username']: username,
                    posix_account['user_number']: 2000,
                    posix_account['group_number']: 2000,
                    posix_account['home']: '/home/' + username,
                    posix_account['password']: self.encrypt_password(password),
                    internet_organization_person['first_name']: first_name,
                    internet_organization_person['last_name']: last_name,
                    internet_organization_person['email']: email,
                },
        ):
            raise RuntimeError(connection.result['description'])

    def remove_user(self, name: str) -> None:
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.delete(dn='uid=' + name + ',ou=users,' + self.suffix):
            raise RuntimeError(connection.result['description'])

    def add_group(self, name: str) -> None:
        posix_group = {
            'name': 'cn',  # must
            'number': 'gidNumber',  # must
        }
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.add(
                dn='cn=' + name + ',ou=groups,' + self.suffix,
                object_class=[
                    'top',
                    'posixGroup',  # super: top
                ],
                attributes={
                    posix_group['name']: name,
                    posix_group['number']: 2000,
                }
        ):
            raise RuntimeError(connection.result['description'])

    def remove_group(self, name: str) -> None:
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.delete(dn='cn=' + name + ',ou=groups,' + self.suffix):
            raise RuntimeError(connection.result['description'])

    def show_group(self, name: str) -> str:
        pass

    def list_groups(self) -> str:
        pass

    def add_unit(self, name: str):
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.add(
                dn='ou=' + name + ',' + self.suffix,
                object_class=['organizationalUnit'],
                attributes={'ou': name}
        ):
            raise RuntimeError(connection.result['description'])

    def remove_unit(self, name: str):
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.delete(dn='ou=' + name + ',' + self.suffix):
            raise RuntimeError(connection.result['description'])

    def show_unit(self, name: str):
        pass

    def list_units(self):
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.search(
                search_base=self.suffix,
                search_filter='(objectClass=organizationalUnit)',
        ):
            raise RuntimeError(connection.result['description'])

        for entry in connection.response:
            print(entry)

    def status(self) -> str:
        return self.format_response(
            self.lazy_get_client().search(
                '(cn=admin)',
                ['cn', 'description'],
            )
        )

    @staticmethod
    def format_response(response: list) -> str:
        result = ''

        for element in response:
            clean_attributes = {}

            for key, value in element['attributes'].items():
                clean_attributes[key] = ','.join(value)

            result += dump(
                clean_attributes,
                default_flow_style=False
            ).strip() + '\n'

        return result


class DirectoryTools:
    def __init__(self, arguments: list):
        self.parser = Parser(arguments)
        self.parsed_arguments = self.parser.parsed_arguments
        config = YamlConfig('~/.directory-tools.yaml')
        self.host = config.get('host')
        self.domain = config.get('domain')
        self.top_level = config.get('top_level')
        self.manager_name = config.get('manager-name')
        self.manager_password = config.get('manager-password')
        self.secure = config.get('secure')

    @staticmethod
    def main() -> int:
        return DirectoryTools(argv[1:]).run()

    def run(self) -> int:
        commands = Commands(
            domain=self.domain,
            top_level=self.top_level,
            host=self.host,
            manager_name=self.manager_name,
            manager_password=self.manager_password,
            secure=self.secure,
        )

        if 'user' in self.parsed_arguments:
            if 'add' in self.parsed_arguments:
                commands.add_user(
                    username=self.parsed_arguments.name,
                    first_name=self.parsed_arguments.first_name,
                    last_name=self.parsed_arguments.last_name,
                    password=self.parsed_arguments.password,
                    email=self.parsed_arguments.email,
                    group=self.parsed_arguments.group,
                )
            elif 'remove' in self.parsed_arguments:
                commands.remove_user(name=self.parsed_arguments.name)
            elif 'show' in self.parsed_arguments:
                print(commands.show_user(name=self.parsed_arguments.name))
            elif 'list' in self.parsed_arguments:
                print(commands.list_users())
            else:
                self.parser.print_help()
        elif 'group' in self.parsed_arguments:
            if 'add' in self.parsed_arguments:
                commands.add_group(name=self.parsed_arguments.name)
            elif 'remove' in self.parsed_arguments:
                commands.remove_group(name=self.parsed_arguments.name)
            elif 'show' in self.parsed_arguments:
                print(commands.show_group(name=self.parsed_arguments.name))
            elif 'list' in self.parsed_arguments:
                print(commands.list_groups())
            else:
                self.parser.print_help()
        elif 'unit' in self.parsed_arguments:
            if 'add' in self.parsed_arguments:
                commands.add_unit(name=self.parsed_arguments.name)
            elif 'remove' in self.parsed_arguments:
                commands.remove_unit(name=self.parsed_arguments.name)
            elif 'show' in self.parsed_arguments:
                print(commands.show_unit(name=self.parsed_arguments.name))
            elif 'list' in self.parsed_arguments:
                print(commands.list_units())
            else:
                self.parser.print_help()
        elif 'status' in self.parsed_arguments:
            commands.status()
        else:
            self.parser.print_help()

        return 0
