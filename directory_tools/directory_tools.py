from getpass import getpass

from sentry_sdk import init as initialize_sentry, capture_exception
from ldap3 import MODIFY_REPLACE

from python_utility.command_process import CommandProcess
from python_utility.configuration import Configuration
from yaml import dump
from sys import argv

from directory_tools.argument_parser import Parser
from directory_tools.client import Client


class Commands:
    posix_account = {
        'full_name': 'cn',  # must
        'username': 'uid',  # must
        'user_number': 'uidNumber',  # must
        'group_number': 'gidNumber',  # must
        'home': 'homeDirectory',  # must
        'password': 'userPassword',  # may
    }
    posix_group = {
        'name': 'cn',  # must
        'number': 'gidNumber',  # must
    }
    internet_organization_person = {
        'first_name': 'givenName',  # may
        'last_name': 'sn',  # may
        'email': 'mail',  # may
    }
    organizational_unit = {
        'name': 'ou',  # must
    }

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

    @staticmethod
    def encrypt_password(password: str) -> str:
        return CommandProcess(
            ['slappasswd', '-s', password]
        ).get_standard_output()

    def authenticate(self, username: str, password: str) -> None:
        self.lazy_get_client().authenticate(
            distinguished_name='uid=' + username + ',ou=users,' + self.suffix,
            password=password,
        )

    def add_group(self, group_name: str) -> None:
        connection = self.lazy_get_client().lazy_get_connection()
        group_number = -1

        for name, attributes in self.list_groups().items():
            number = attributes[self.posix_group['number']]

            if number > group_number:
                group_number = number

        if group_number is -1:
            group_number = 2000
        else:
            group_number += 1

        if not connection.add(
                dn='cn=' + group_name + ',ou=groups,' + self.suffix,
                object_class=[
                    'top',
                    'posixGroup',  # super: top
                ],
                attributes={
                    self.posix_group['name']: group_name,
                    self.posix_group['number']: group_number,
                }
        ):
            raise RuntimeError(connection.result['description'])

    def remove_group(self, name: str) -> None:
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.delete(
                dn='cn=' + name + ',ou=groups,' + self.suffix
        ):
            raise RuntimeError(connection.result['description'])

    def format_group_attributes(self, attributes: dict) -> dict:
        return {
            self.posix_group['number']: attributes[self.posix_group['number']]
        }

    def show_group(self, name: str) -> dict:
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.search(
                search_base='ou=groups,' + self.suffix,
                search_filter='(cn=' + name + ')',
                attributes=[
                    self.posix_group['name'],
                    self.posix_group['number'],
                ],
        ):
            if connection.result['description'] == 'success':
                return {}
            else:
                raise RuntimeError(connection.result['description'])

        return self.format_group_attributes(
            connection.response[0]['attributes']
        )

    def list_groups(self) -> dict:
        connection = self.lazy_get_client().lazy_get_connection()
        groups = {}

        if not connection.search(
                search_base=self.suffix,
                search_filter='(objectClass=posixGroup)',
                attributes=[
                    self.posix_group['name'],
                    self.posix_group['number'],
                ],
        ):
            if connection.result['description'] == 'success':
                return groups
            else:
                raise RuntimeError(connection.result['description'])

        for entry in connection.response:
            groups[
                entry['attributes'][self.posix_group['name']][0]
            ] = self.format_group_attributes(entry['attributes'])

        return groups

    def add_user(
            self,
            username: str,
            first_name: str,
            last_name: str,
            password: str,
            email: str
    ) -> None:
        connection = self.lazy_get_client().lazy_get_connection()
        self.add_group(group_name=username)
        group = self.show_group(name=username)
        group_number = group[self.posix_group['number']]

        if not connection.add(
                dn='uid=' + username + ',ou=users,' + self.suffix,
                object_class=[
                    'top',
                    'posixAccount',  # super: top
                    'person',  # super: top
                    'organizationalPerson',  # super: person
                    'inetOrgPerson',  # super: organizationalPerson
                    'shadowAccount',  # super: top
                ],
                attributes={
                    self.posix_account[
                        'full_name'
                    ]: first_name + ' ' + last_name,
                    self.posix_account['username']: username,
                    self.posix_account['user_number']: group_number,
                    self.posix_account['group_number']: group_number,
                    self.posix_account['home']: '/home/' + username,
                    self.posix_account[
                        'password'
                    ]: self.encrypt_password(password),
                    self.internet_organization_person[
                        'first_name'
                    ]: first_name,
                    self.internet_organization_person['last_name']: last_name,
                    self.internet_organization_person['email']: email,
                },
        ):
            raise RuntimeError(connection.result['description'])

    def set_password(self, username: str, password: str):
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.modify(
                dn='uid=' + username + ',ou=users,' + self.suffix,
                changes={
                    self.posix_account['password']: [
                        (MODIFY_REPLACE, self.encrypt_password(password))
                    ],
                },
        ):
            raise RuntimeError(connection.result['description'])

    def set_email(self, username: str, email: str):
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.modify(
                dn='uid=' + username + ',ou=users,' + self.suffix,
                changes={
                    self.internet_organization_person['email']: [
                        (MODIFY_REPLACE, email)
                    ],
                },
        ):
            raise RuntimeError(connection.result['description'])

    def set_first_name(self, username: str, first_name: str):
        connection = self.lazy_get_client().lazy_get_connection()
        user = self.show_user(username)

        if not connection.modify(
                dn='uid=' + username + ',ou=users,' + self.suffix,
                changes={
                    self.internet_organization_person['first_name']: [
                        (MODIFY_REPLACE, first_name)
                    ],
                    self.posix_account['full_name']: [
                        (MODIFY_REPLACE, first_name + ' ' + user[
                            self.internet_organization_person['last_name']
                        ])
                    ],
                },
        ):
            raise RuntimeError(connection.result['description'])

    def set_last_name(self, username: str, last_name: str):
        connection = self.lazy_get_client().lazy_get_connection()
        user = self.show_user(username)

        if not connection.modify(
                dn='uid=' + username + ',ou=users,' + self.suffix,
                changes={
                    self.internet_organization_person['first_name']: [
                        (MODIFY_REPLACE, last_name)
                    ],
                    self.posix_account['full_name']: [
                        (MODIFY_REPLACE, user[
                                             self.internet_organization_person[
                                                 'first_name']
                                         ] + ' ' + last_name)
                    ],
                },
        ):
            raise RuntimeError(connection.result['description'])

    def remove_user(self, name: str) -> None:
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.delete(
                dn='uid=' + name + ',ou=users,' + self.suffix
        ):
            raise RuntimeError(connection.result['description'])

        self.remove_group(name)

    def format_user_attributes(self, attributes: dict) -> dict:
        return {
            self.posix_account['full_name']: attributes[
                self.posix_account['full_name']
            ][0],
            self.posix_account['user_number']: attributes[
                self.posix_account['user_number']
            ],
            self.posix_account['group_number']: attributes[
                self.posix_account['group_number']
            ],
            self.posix_account['home']: attributes[
                self.posix_account['home']
            ],
            self.internet_organization_person['first_name']: attributes[
                self.internet_organization_person['first_name']
            ][0],
            self.internet_organization_person['last_name']: attributes[
                self.internet_organization_person['last_name']
            ][0],
            self.internet_organization_person['email']: attributes[
                self.internet_organization_person['email']
            ][0],
        }

    def show_user(self, name: str) -> dict:
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.search(
                search_base='ou=users,' + self.suffix,
                search_filter='(uid=' + name + ')',
                attributes=[
                    self.posix_account['username'],
                    self.posix_account['full_name'],
                    self.posix_account['user_number'],
                    self.posix_account['group_number'],
                    self.posix_account['home'],
                    self.internet_organization_person['first_name'],
                    self.internet_organization_person['last_name'],
                    self.internet_organization_person['email'],
                ],
        ):
            if connection.result['description'] == 'success':
                return {}
            else:
                raise RuntimeError(connection.result['description'])

        return self.format_user_attributes(
            attributes=connection.response[0]['attributes'],
        )

    def list_users(self) -> dict:
        connection = self.lazy_get_client().lazy_get_connection()
        users = {}

        if not connection.search(
                search_base=self.suffix,
                search_filter='(objectClass=inetOrgPerson)',
                attributes=[
                    self.posix_account['username'],
                    self.posix_account['full_name'],
                    self.posix_account['user_number'],
                    self.posix_account['group_number'],
                    self.posix_account['home'],
                    self.internet_organization_person['first_name'],
                    self.internet_organization_person['last_name'],
                    self.internet_organization_person['email'],
                ],
        ):
            if connection.result['description'] == 'success':
                return users
            else:
                raise RuntimeError(connection.result['description'])

        for entry in connection.response:
            users[
                entry['attributes'][self.posix_account['username']][0]
            ] = self.format_user_attributes(entry['attributes'])

        return users

    def add_unit(self, name: str):
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.add(
                dn='ou=' + name + ',' + self.suffix,
                object_class=['organizationalUnit'],
                attributes={self.organizational_unit['name']: name}
        ):
            raise RuntimeError(connection.result['description'])

    def remove_unit(self, name: str):
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.delete(dn='ou=' + name + ',' + self.suffix):
            raise RuntimeError(connection.result['description'])

    def show_unit(self, name: str):
        connection = self.lazy_get_client().lazy_get_connection()

        if not connection.search(
                search_base=self.suffix,
                search_filter='(ou=' + name + ')',
                attributes=[
                    self.organizational_unit['name']
                ],
        ):
            if connection.result['description'] == 'success':
                return ''
            else:
                raise RuntimeError(connection.result['description'])

        return str(connection.response[0]['attributes'])

    def list_units(self) -> list:
        connection = self.lazy_get_client().lazy_get_connection()
        units = []

        if not connection.search(
                search_base=self.suffix,
                search_filter='(objectClass=organizationalUnit)',
                attributes=[
                    self.organizational_unit['name']
                ],
        ):
            if connection.result['description'] == 'success':
                return units
            else:
                raise RuntimeError(connection.result['description'])

        for entry in connection.response:
            units += [entry['attributes'][self.organizational_unit['name']][0]]

        return units

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
        config = Configuration('~/.directory-tools.yaml')
        self.host = config.get('host')
        self.domain = config.get('domain')
        self.top_level = config.get('top_level')
        self.manager_name = config.get('manager-name')
        self.manager_password = config.get('manager-password')
        self.secure = bool(config.get('secure'))
        initialize_sentry(config.get('sentry_locator'))

    @staticmethod
    def main() -> int:
        return DirectoryTools(argv[1:]).run_and_capture_exceptions()

    def run_and_capture_exceptions(self) -> int:
        try:
            return self.run()
        except Exception as error:
            capture_exception(error)
            print(str(error))

            return 1

    def run(self) -> int:
        commands = Commands(
            domain=self.domain,
            top_level=self.top_level,
            host=self.host,
            manager_name=self.manager_name,
            manager_password=self.manager_password,
            secure=self.secure,
        )
        exit_code = 0

        if 'user' in self.parsed_arguments:
            if 'add' in self.parsed_arguments:
                commands.add_user(
                    username=self.parsed_arguments.name,
                    first_name=self.parsed_arguments.first_name,
                    last_name=self.parsed_arguments.last_name,
                    password=self.parsed_arguments.password,
                    email=self.parsed_arguments.email,
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
                commands.add_group(group_name=self.parsed_arguments.name)
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
        elif 'authenticate' in self.parsed_arguments:
            if self.parsed_arguments.password == '':
                password = getpass('Password: ')
            else:
                password = self.parsed_arguments.password

            commands.authenticate(
                username=self.parsed_arguments.name,
                password=password,
            )
        else:
            self.parser.print_help()

        return exit_code
