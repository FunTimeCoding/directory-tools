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
        full_name = first_name + ' ' + last_name
        self.lazy_get_client().lazy_get_connection().add(
            dn='uid=' + username + ',ou=users,' + self.suffix,
            object_class=['inetOrgPerson', 'posixAccount', 'shadowAccount'],
            # TODO: get uid increment
            # TODO: get gid
            # TODO: create ou if not exists?
            attributes={
                'cn': full_name,
                'sn': last_name,
                'uid': username,
                'uidNumber': 2000,
                'gidNumber': 2000,
                'homeDirectory': '',
                'loginShell': '/bin/bash',
                'gecos': full_name,
                'userPassword': self.encrypt_password(password),
                'displayName': username,
                'mail': email,
                'shadowLastChange': 0,
                'shadowMax': 0,
                'shadowWarning': 0,
            },
        )

    def remove_user(self, name: str) -> None:
        pass

    def list_groups(self) -> str:
        pass

    def show_group(self, name: str) -> str:
        pass

    def add_group(self, name: str) -> None:
        pass

    def remove_group(self, name: str) -> None:
        pass

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
        elif 'status' in self.parsed_arguments:
            commands.status()
        else:
            self.parser.print_help()

        return 0
