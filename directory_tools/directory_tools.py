from python_utility.yaml_config import YamlConfig

from directory_tools.argument_parser import Parser
from directory_tools.client import Client


class DirectoryTools:
    def __init__(self, arguments: list):
        self._parser = Parser(arguments)
        self._parsed_arguments = self._parser.parsed_arguments

        config = YamlConfig(path='~/.directory-tools.yml')
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

    def run(self) -> int:
        result = 0
        arguments = self._parsed_arguments
        parser = self._parser

        if 'user' in arguments:
            if 'add' in arguments:
                pass
            elif 'delete' in arguments:
                pass
            elif 'search' in arguments:
                query = '(uid' + arguments.user_name + ')'
                client = self._lazy_get_client()
                response, result = client.search_user(query)
                print(result)
                print(response)
            elif 'list' in arguments:
                pass
            else:
                parser.print_help()
        elif 'status' in arguments:
            client = self._lazy_get_client()
            response, result = client.search(
                query='(cn=admin)',
                attributes=['cn', 'description']
            )
            print(result)
            print(response)
        else:
            parser.print_help()

        return result
