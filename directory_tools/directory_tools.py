from python_utility.yaml_config import YamlConfig
from yaml import dump

from directory_tools.argument_parser import Parser
from directory_tools.client import Client


class DirectoryTools:
    def __init__(self, arguments: list):
        self._parser = Parser(arguments)
        self._parsed_arguments = self._parser.parsed_arguments

        config = YamlConfig('~/.directory-tools.yml')
        host = config.get('host')
        domain = config.get('domain')
        top_level = config.get('top_level')
        manager_name = config.get('manager-name')

        self._suffix = 'dc=' + domain + ',dc=' + top_level
        self._server_name = host + '.' + domain + '.' + top_level
        self._manager_dn = 'cn=' + manager_name + ',' + self._suffix
        self._manager_password = config.get('manager-password')
        self._client = None

    def _lazy_get_client(self) -> Client:
        if self._client is None:
            self._client = Client(
                server_name=self._server_name,
                manager_dn=self._manager_dn,
                manager_password=self._manager_password,
                suffix=self._suffix
            )

        return self._client

    @staticmethod
    def print_response(response: list) -> None:
        for element in response:
            attributes = element['attributes']
            clean_attributes = {}

            for key, value in attributes.items():
                clean_attributes[key] = ','.join(value)

            markup_language = dump(clean_attributes, default_flow_style=False)
            print(markup_language.strip())

    def run(self) -> int:
        exit_code = 0
        arguments = self._parsed_arguments
        parser = self._parser

        if 'user' in arguments:
            if 'add' in arguments:
                pass
            elif 'delete' in arguments:
                pass
            elif 'search' in arguments:
                client = self._lazy_get_client()

                if arguments.user_name is not None:
                    query = '(uid=' + arguments.user_name + ')'
                else:
                    query = '(cn=' + arguments.full_name + ')'

                response = client.search_user(query)
                self.print_response(response)
            elif 'list' in arguments:
                client = self._lazy_get_client()
                response = client.search_user('ou=users,dc=shiin,dc=org')
                self.print_response(response)
            else:
                parser.print_help()
        elif 'status' in arguments:
            client = self._lazy_get_client()
            response = client.search(
                '(cn=admin)',
                ['cn', 'description']
            )
            self.print_response(response)
        else:
            parser.print_help()

        return exit_code
